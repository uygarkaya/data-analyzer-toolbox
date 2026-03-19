from configuration.configuration import Configuration
from typing import Optional
import pandas as pd
import requests, io

class DatasetAPI:
    def __init__(self) -> None:
        pass

    def fetch_dataset_list() -> list[dict]:
        return Configuration().dataset_registry
    
    def download_dataset(dataset_id: str) -> tuple[Optional[pd.DataFrame], Optional[dict], Optional[str]]:
        entry = next((d for d in Configuration().dataset_registry if d["id"] == dataset_id), None)
        if entry is None:
            return None, None, f"Dataset '{dataset_id}' not found in registry."

        try:
            resp = requests.get(entry["url"], timeout=30)
            resp.raise_for_status()
        except requests.RequestException as exc:
            return None, entry, f"Download failed: {exc}"

        try:
            if entry["format"] == "csv":
                sep = ";" if "winequality" in (entry["url"] or "") else ","
                df = pd.read_csv(io.StringIO(resp.text), sep=sep)
                # Limit to 2000 rows for speed
                if len(df) > 2000:
                    df = df.sample(2000, random_state=42).reset_index(drop=True)
                return df, entry, None
        except Exception as exc:
            return None, entry, f"Parsing failed: {exc}"

        return None, entry, "Unsupported format."

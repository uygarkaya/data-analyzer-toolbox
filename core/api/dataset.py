from configuration.configuration import Configuration
from typing import Optional
import pandas as pd
import requests, io

class DatasetAPI:
    def __init__(self) -> None:
        pass

    @staticmethod
    def fetch_dataset_list() -> list[dict]:
        return Configuration().sample_datasets
    
    @staticmethod
    def download_dataset(dataset_id: str) -> tuple[Optional[pd.DataFrame], Optional[dict], Optional[str]]:
        entry = next((d for d in Configuration().sample_datasets if d["id"] == dataset_id), None)
        if entry is None:
            return None, None, f"Dataset '{dataset_id}' Not Found in Registry!"

        try:
            resp = requests.get(entry["url"], timeout=30)
            resp.raise_for_status()
        except requests.RequestException as exc:
            return None, entry, f"Download Failed: {exc}"

        try:
            if entry["format"] == "csv":
                sep = ";" if "winequality" in (entry["url"] or "") else ","
                df = pd.read_csv(io.StringIO(resp.text), sep=sep)
                if len(df) > 2000:
                    df = df.sample(2000, random_state=42).reset_index(drop=True)
                return df, entry, None
        except Exception as exc:
            return None, entry, f"Parsing Failed: {exc}"

        return None, entry, "Unsupported Format!"

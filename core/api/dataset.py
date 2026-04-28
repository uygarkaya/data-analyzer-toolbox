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
            resp = requests.get(entry["url"], timeout=60)
            resp.raise_for_status()
        except requests.RequestException as exc:
            return None, entry, f"Download Failed: {exc}"

        try:
            if entry["format"] == "csv":
                read_kwargs = {
                    "sep": entry.get("sep", ","),
                    "skiprows": entry.get("skiprows", 0),
                    "compression": entry.get("compression", "infer"),
                }
                if "columns" in entry:
                    read_kwargs["names"] = entry["columns"]
                    read_kwargs["header"] = None

                df = pd.read_csv(io.BytesIO(resp.content) if read_kwargs["compression"] not in (None, "infer") or entry["url"].endswith((".gz", ".zip", ".bz2", ".xz")) else io.StringIO(resp.text), **read_kwargs)
                if entry.get("target_col") and entry.get("target_col") not in df.columns:
                    return None, entry, f"Expected Target Column '{entry.get('target_col')}' Not Found in Downloaded Data!"

                if len(df) > 2000:
                    df = df.sample(2000, random_state=42).reset_index(drop=True)
                return df, entry, None
        except Exception as exc:
            return None, entry, f"Parsing Failed: {exc}"

        return None, entry, "Unsupported Format!"

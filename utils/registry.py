from configuration.environment import Environment
import json, importlib

def import_class(dotted: str):
    module_name, _, class_name = dotted.rpartition(".")
    return getattr(importlib.import_module(module_name), class_name)

def load_model_registry() -> dict:
    with open(Environment.get_instance()["MODELS_URL"], "r", encoding="utf-8") as f:
        return json.load(f)

def families_for(registry: dict, task: str) -> list:
    return [
        {"label": fam["label"], "value": fam["value"]}
        for fam in registry["families"]
        if any(a["task"] == task for a in fam["algorithms"])
    ]

def algorithms_for(registry: dict, family_value: str, task: str) -> list:
    for fam in registry["families"]:
        if fam["value"] == family_value:
            return [
                {"label": a["label"], "value": a["value"]}
                for a in fam["algorithms"] if a["task"] == task
            ]
    return []

def find_algorithm(registry: dict, family_value: str, algo_value: str):
    for fam in registry["families"]:
        if fam["value"] != family_value:
            continue
        for algo in fam["algorithms"]:
            if algo["value"] == algo_value:
                return fam, algo
    return None, None

def build_params(registry: dict, algo: dict, hp_ids, hp_values) -> dict:
    field_specs = {f["id"]: f for f in registry["hyperparameter_fields"]}
    kinds = {
        ui["param"]: field_specs[ui["field"]].get("kind", "float")
        for ui in algo.get("ui_fields", []) if ui["field"] in field_specs
    }
    params = dict(algo.get("params", {}))
    for hid, val in zip(hp_ids or [], hp_values or []):
        if val is None:
            continue
        params[hid["param"]] = int(val) if kinds.get(hid["param"]) == "int" else float(val)
    return params
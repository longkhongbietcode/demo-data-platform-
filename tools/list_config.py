import json
from pathlib import Path
from typing import Dict, List

CONFIG_PATH = Path(__file__).resolve().parents[1] / 'config' / 'datasources.json'

def load_config() -> List[dict]:
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def group_by_namespace(sources: List[dict]) -> Dict[str, List[dict]]:
    grouped: Dict[str, List[dict]] = {}
    for s in sources:
        ns = s.get('namespace_name', 'Unknown')
        grouped.setdefault(ns, []).append(s)
    return grouped

def tech_of(oddrn: str) -> str:
    # very light oddrn parser: //tech/... e.g. //postgresql/host/...
    if oddrn.startswith('//'):
        parts = oddrn.strip('/').split('/')
        return parts[0]
    return 'unknown'

def main():
    cfg = load_config()
    grouped = group_by_namespace(cfg)
    for ns, items in grouped.items():
        print(f'\n# Namespace: {ns}')
        for it in items:
            print(f"- {it.get('name')} | tech={tech_of(it.get('oddrn',''))} | oddrn={it.get('oddrn')}")

if __name__ == '__main__':
    main()

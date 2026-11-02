
import csv
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CATALOG_PATH = (
    PROJECT_ROOT / "data" / "training" / "intent_catalog.json"
)

OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "training" / "expansion_template.csv"
)

STYLES = [
    "direct",
    "conversational",
    "scenario",
    "procedural",
    "indirect"
]


def main():
    with open(CATALOG_PATH, encoding="utf-8") as file:
        catalog = json.load(file)

    rows = []

    for category in catalog["categories"]:
        for intent in category["intents"]:
            for style in STYLES:
                rows.append({
                    "label": category["label"],
                    "category": category["name"],
                    "intent_group": intent["id"],
                    "style": style,
                    "new_query": ""
                })

    with open(
        OUTPUT_PATH,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "label",
                "category",
                "intent_group",
                "style",
                "new_query"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Expansion rows created: {len(rows)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

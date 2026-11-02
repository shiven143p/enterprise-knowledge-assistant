
import csv
import json
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CATALOG_PATH = (
    PROJECT_ROOT / "data" / "training" / "intent_catalog.json"
)

OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "training" / "employee_queries.csv"
)


def generate_dataset():
    with open(CATALOG_PATH, "r", encoding="utf-8") as file:
        catalog = json.load(file)

    records = []
    seen_queries = set()
    seen_intents = set()

    for category in catalog["categories"]:
        label = category["label"]

        for intent in category["intents"]:
            intent_id = intent["id"]

            if intent_id in seen_intents:
                raise ValueError(
                    f"Duplicate intent ID: {intent_id}"
                )

            seen_intents.add(intent_id)

            for query in intent["queries"]:
                query = " ".join(query.strip().split())

                if not query:
                    raise ValueError(
                        f"Empty query in intent {intent_id}"
                    )

                normalized = query.casefold()

                if normalized in seen_queries:
                    raise ValueError(
                        f"Duplicate query: {query}"
                    )

                seen_queries.add(normalized)

                records.append({
                    "text": query,
                    "label": label,
                    "intent_group": intent_id
                })

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "text",
                "label",
                "intent_group"
            ]
        )

        writer.writeheader()
        writer.writerows(records)

    print("Dataset generated successfully!")
    print(f"Total queries: {len(records)}")
    print(f"Total intents: {len(seen_intents)}")

    counts = Counter(
        record["label"]
        for record in records
    )

    print("\nClass distribution:")

    for label, count in sorted(counts.items()):
        print(f"Label {label}: {count} queries")

    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_dataset()


from pathlib import Path
from collections import Counter

import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "training"

INPUT_FILE = DATA_DIR / "employee_queries.csv"

RANDOM_SEED = 42

LABEL_NAMES = {
    0: "HR & Leave",
    1: "IT Support",
    2: "Finance & Expenses",
    3: "Travel & Operations"
}


def validate_dataset(df):
    """Validate dataset structure and quality."""

    print("\n=== DATASET VALIDATION ===")

    required_columns = {
        "text",
        "label",
        "intent_group"
    }

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "Missing required dataset columns."
        )

    if df[list(required_columns)].isnull().any().any():
        raise ValueError(
            "Dataset contains missing values."
        )

    if df["text"].astype(str).str.strip().eq("").any():
        raise ValueError(
            "Dataset contains empty queries."
        )

    if df["text"].str.casefold().duplicated().any():
        raise ValueError(
            "Duplicate queries detected."
        )

    if not set(df["label"]).issubset(LABEL_NAMES):
        raise ValueError(
            "Unknown classification labels detected."
        )

    # Every intent must belong to exactly one label.
    intent_labels = df.groupby(
        "intent_group"
    )["label"].nunique()

    if (intent_labels > 1).any():
        raise ValueError(
            "Some intent groups have multiple labels."
        )

    print("Required columns: PASS")
    print("Missing values: PASS")
    print("Duplicate queries: PASS")
    print("Label consistency: PASS")

    print("\nCategory distribution:")

    for label, count in df["label"].value_counts().sort_index().items():
        print(
            f"{LABEL_NAMES[label]}: {count}"
        )


def split_dataset(df):
    """Split data while keeping intent groups together."""

    rng = np.random.default_rng(RANDOM_SEED)

    train_parts = []
    val_parts = []
    test_parts = []

    for label in sorted(LABEL_NAMES):

        category_df = df[
            df["label"] == label
        ].copy()

        intents = category_df[
            "intent_group"
        ].unique()

        if len(intents) != 10:
            raise ValueError(
                f"Expected 10 intents for label {label}, "
                f"found {len(intents)}."
            )

        intents = rng.permutation(intents)

        train_intents = intents[:6]
        val_intents = intents[6:8]
        test_intents = intents[8:10]

        train_parts.append(
            category_df[
                category_df["intent_group"].isin(
                    train_intents
                )
            ]
        )

        val_parts.append(
            category_df[
                category_df["intent_group"].isin(
                    val_intents
                )
            ]
        )

        test_parts.append(
            category_df[
                category_df["intent_group"].isin(
                    test_intents
                )
            ]
        )

    train_df = pd.concat(
        train_parts,
        ignore_index=True
    )

    val_df = pd.concat(
        val_parts,
        ignore_index=True
    )

    test_df = pd.concat(
        test_parts,
        ignore_index=True
    )

    # Shuffle records inside each split.
    train_df = train_df.sample(
        frac=1,
        random_state=RANDOM_SEED
    ).reset_index(drop=True)

    val_df = val_df.sample(
        frac=1,
        random_state=RANDOM_SEED
    ).reset_index(drop=True)

    test_df = test_df.sample(
        frac=1,
        random_state=RANDOM_SEED
    ).reset_index(drop=True)

    return train_df, val_df, test_df


def verify_no_leakage(train_df, val_df, test_df):
    """Verify intent groups do not overlap."""

    train_intents = set(train_df["intent_group"])
    val_intents = set(val_df["intent_group"])
    test_intents = set(test_df["intent_group"])

    assert train_intents.isdisjoint(val_intents)
    assert train_intents.isdisjoint(test_intents)
    assert val_intents.isdisjoint(test_intents)

    print("\nIntent group leakage check: PASS")


def main():

    df = pd.read_csv(INPUT_FILE)

    validate_dataset(df)

    train_df, val_df, test_df = split_dataset(df)

    verify_no_leakage(
        train_df,
        val_df,
        test_df
    )

    train_df.to_csv(
        DATA_DIR / "train.csv",
        index=False
    )

    val_df.to_csv(
        DATA_DIR / "validation.csv",
        index=False
    )

    test_df.to_csv(
        DATA_DIR / "test.csv",
        index=False
    )

    print("\n=== FINAL DATASET SPLIT ===")

    print(f"Training: {len(train_df)}")
    print(f"Validation: {len(val_df)}")
    print(f"Testing: {len(test_df)}")

    print("\nDataset files saved successfully.")


if __name__ == "__main__":
    main()


from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT / "data" / "training" / "employee_queries.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "training"

LABEL_NAMES = {
    0: "HR & Leave",
    1: "IT Support",
    2: "Finance & Expenses",
    3: "Travel & Operations"
}


def main():
    # Step 1: Load dataset
    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully.")
    print(f"Total records: {len(df)}")

    # Step 2: Validate required columns
    required_columns = {"text", "label"}

    if not required_columns.issubset(df.columns):
        raise ValueError("Missing required dataset columns.")

    # Step 3: Remove missing and duplicate records
    df = df.dropna(subset=["text", "label"]).copy()

    df["text"] = df["text"].astype(str).str.strip()

    df = df[df["text"] != ""].copy()

    df = df.drop_duplicates(
        subset=["text"],
        keep="first"
    )

    # Step 4: Validate labels
    df["label"] = df["label"].astype(int)

    if not set(df["label"]).issubset(LABEL_NAMES):
        raise ValueError("Dataset contains unknown labels.")

    print("\nClass distribution:")

    for label, count in df["label"].value_counts().sort_index().items():
        print(f"{LABEL_NAMES[label]}: {count}")

    # Step 5: Split into training and test sets
    train_df, test_df = train_test_split(
        df,
        test_size=0.20,
        random_state=42,
        stratify=df["label"]
    )

    # Step 6: Split training into train and validation
    train_df, val_df = train_test_split(
        train_df,
        test_size=0.25,
        random_state=42,
        stratify=train_df["label"]
    )

    # Final split: 60% training, 20% validation,
    # and 20% testing.

    # Step 7: Save datasets
    train_df.to_csv(
        OUTPUT_DIR / "train.csv",
        index=False
    )

    val_df.to_csv(
        OUTPUT_DIR / "validation.csv",
        index=False
    )

    test_df.to_csv(
        OUTPUT_DIR / "test.csv",
        index=False
    )

    print("\nDataset split completed.")
    print(f"Training samples: {len(train_df)}")
    print(f"Validation samples: {len(val_df)}")
    print(f"Testing samples: {len(test_df)}")


if __name__ == "__main__":
    main()

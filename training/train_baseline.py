
from pathlib import Path
import json
import time

import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "training"
MODEL_DIR = PROJECT_ROOT / "models" / "baseline"

LABEL_NAMES = [
    "HR & Leave",
    "IT Support",
    "Finance & Expenses",
    "Travel & Operations"
]


def evaluate(model, df):
    """Evaluate classifier on a labeled dataset."""

    predictions = model.predict(df["text"])

    return {
        "accuracy": float(
            accuracy_score(df["label"], predictions)
        ),
        "f1_macro": float(
            f1_score(
                df["label"],
                predictions,
                average="macro",
                zero_division=0
            )
        )
    }


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # Load fixed dataset splits.
    train_df = pd.read_csv(DATA_DIR / "train.csv")
    val_df = pd.read_csv(DATA_DIR / "validation.csv")
    test_df = pd.read_csv(DATA_DIR / "test.csv")

    print("Training records:", len(train_df))
    print("Validation records:", len(val_df))
    print("Testing records:", len(test_df))

    # Candidate regularization strengths.
    candidate_c_values = [0.1, 1.0, 10.0]

    best_model = None
    best_c = None
    best_f1 = -1.0

    print("\n=== VALIDATION MODEL SELECTION ===")

    for c_value in candidate_c_values:

        pipeline = Pipeline([
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    min_df=1,
                    sublinear_tf=True
                )
            ),
            (
                "classifier",
                LogisticRegression(
                    C=c_value,
                    max_iter=1000,
                    random_state=42
                )
            )
        ])

        pipeline.fit(
            train_df["text"],
            train_df["label"]
        )

        metrics = evaluate(pipeline, val_df)

        print(
            f"C={c_value}: "
            f"Accuracy={metrics['accuracy']:.4f}, "
            f"Macro F1={metrics['f1_macro']:.4f}"
        )

        if metrics["f1_macro"] > best_f1:
            best_f1 = metrics["f1_macro"]
            best_c = c_value
            best_model = pipeline

    print(f"\nSelected C: {best_c}")

    # Final evaluation on untouched test data.
    print("\n=== FINAL TEST EVALUATION ===")

    start = time.perf_counter()

    predictions = best_model.predict(
        test_df["text"]
    )

    elapsed = time.perf_counter() - start

    test_accuracy = accuracy_score(
        test_df["label"],
        predictions
    )

    test_f1 = f1_score(
        test_df["label"],
        predictions,
        average="macro",
        zero_division=0
    )

    print(f"Test accuracy: {test_accuracy:.4f}")
    print(f"Test macro F1: {test_f1:.4f}")

    print("\nClassification report:")

    print(
        classification_report(
            test_df["label"],
            predictions,
            labels=[0, 1, 2, 3],
            target_names=LABEL_NAMES,
            zero_division=0
        )
    )

    matrix = confusion_matrix(
        test_df["label"],
        predictions,
        labels=[0, 1, 2, 3]
    )

    print("\nConfusion matrix:")
    print(matrix)

    # Save trained model.
    joblib.dump(
        best_model,
        MODEL_DIR / "tfidf_logreg.joblib"
    )

    results = {
        "model": "TF-IDF + Logistic Regression",
        "selected_c": best_c,
        "test_accuracy": float(test_accuracy),
        "test_f1_macro": float(test_f1),
        "total_test_samples": len(test_df),
        "inference_seconds_total": elapsed,
        "confusion_matrix": matrix.tolist()
    }

    with open(
        MODEL_DIR / "evaluation.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(results, file, indent=2)

    print("\nModel and results saved to:")
    print(MODEL_DIR)


if __name__ == "__main__":
    main()

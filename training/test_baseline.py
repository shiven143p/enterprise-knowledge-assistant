
from pathlib import Path
import joblib

ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    ROOT / "models" / "baseline" / "tfidf_logreg.joblib"
)

LABEL_NAMES = {
    0: "HR & Leave",
    1: "IT Support",
    2: "Finance & Expenses",
    3: "Travel & Operations"
}

model = joblib.load(MODEL_PATH)

queries = [
    "I need to take a few days off next month.",
    "My work laptop cannot connect to the network.",
    "Can I claim the cost of a client dinner?",
    "I need to change my business flight reservation."
]

predictions = model.predict(queries)
probabilities = model.predict_proba(queries)

for query, label, probs in zip(
    queries,
    predictions,
    probabilities
):
    confidence = max(probs)

    print("\nQuery:", query)
    print("Predicted category:", LABEL_NAMES[int(label)])
    print("Confidence:", round(float(confidence), 4))

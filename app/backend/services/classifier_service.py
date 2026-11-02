from pathlib import Path

import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    PROJECT_ROOT / "models" / "eka-distilbert-model"
)

tokenizer = None
model = None


def load_classifier():
    global tokenizer, model

    if model is not None:
        return

    tokenizer = AutoTokenizer.from_pretrained(
        str(MODEL_PATH),
        local_files_only=True
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        str(MODEL_PATH),
        local_files_only=True
    )

    model.eval()


def classify_query(query: str):
    load_classifier()

    inputs = tokenizer(
        query,
        return_tensors="pt",
        truncation=True,
        max_length=128
    )

    with torch.inference_mode():
        outputs = model(**inputs)

    probabilities = torch.softmax(
        outputs.logits,
        dim=-1
    )[0]

    predicted_id = int(
        torch.argmax(probabilities).item()
    )

    confidence = float(
        probabilities[predicted_id].item()
    )

    return {
        "query": query,
        "label": predicted_id,
        "category": model.config.id2label[predicted_id],
        "confidence": round(confidence, 4)
    }

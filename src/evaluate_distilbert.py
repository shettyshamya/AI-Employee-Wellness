from pathlib import Path
import json

import numpy as np
import pandas as pd
import torch

from datasets import Dataset
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
)


DATA_DIR = Path("data/processed")
MODEL_DIR = Path("models/distilbert")

EMOTIONS = [
    "joy",
    "sadness",
    "anger",
    "fear",
    "surprise",
    "disgust",
]


def load_test_data():
    df = pd.read_csv(DATA_DIR / "go_emotions_test.csv")

    df["labels"] = df[EMOTIONS].astype(float).values.tolist()

    return Dataset.from_pandas(
        df[["text", "labels"]],
        preserve_index=False,
    )


def compute_metrics(eval_pred):
    predictions, labels = eval_pred

    probabilities = torch.sigmoid(
        torch.tensor(predictions)
    ).numpy()

    predicted_labels = (probabilities >= 0.5).astype(int)

    return {
        "accuracy": accuracy_score(labels, predicted_labels),
        "precision": precision_score(
            labels,
            predicted_labels,
            average="macro",
            zero_division=0,
        ),
        "recall": recall_score(
            labels,
            predicted_labels,
            average="macro",
            zero_division=0,
        ),
        "macro_f1": f1_score(
            labels,
            predicted_labels,
            average="macro",
            zero_division=0,
        ),
    }


def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_DIR
    )

    test_dataset = load_test_data()

    test_dataset = test_dataset.map(
        lambda batch: tokenizer(
            batch["text"],
            truncation=True,
            padding="max_length",
            max_length=128,
        ),
        batched=True,
    )

    trainer = Trainer(
        model=model,
        processing_class=tokenizer,
        compute_metrics=compute_metrics,
    )

    results = trainer.evaluate(test_dataset)

    print("\nDISTILBERT TEST RESULTS")
    print(json.dumps(results, indent=4, default=float))


if __name__ == "__main__":
    main()
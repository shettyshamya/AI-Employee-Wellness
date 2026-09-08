from pathlib import Path
import json

import numpy as np
import pandas as pd
import torch

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)

from datasets import Dataset


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATA_DIR = Path("data/processed")
MODEL_DIR = Path("models")

EMOTIONS = [
    "joy",
    "sadness",
    "anger",
    "fear",
    "surprise",
    "disgust",
]

# CPU-friendly models
MODELS = {
    "bert": "bert-base-uncased",
}



# --------------------------------------------------
# Dataset preparation
# --------------------------------------------------

def load_data(filename):
    df = pd.read_csv(DATA_DIR / filename)

    # Convert labels into a single list
    df["labels"] = df[EMOTIONS].astype(float).values.tolist()

    return Dataset.from_pandas(
        df[["text", "labels"]],
        preserve_index=False,
    )


def tokenize_dataset(dataset, tokenizer):
    return dataset.map(
        lambda batch: tokenizer(
            batch["text"],
            truncation=True,
            padding="max_length",
            max_length=128,
        ),
        batched=True,
    )


# --------------------------------------------------
# Metrics
# --------------------------------------------------

def compute_metrics(eval_pred):
    predictions, labels = eval_pred

    probabilities = torch.sigmoid(
        torch.tensor(predictions)
    ).numpy()

    predicted_labels = (probabilities >= 0.5).astype(int)

    return {
        "accuracy": accuracy_score(
            labels,
            predicted_labels,
        ),
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


# --------------------------------------------------
# Model training
# --------------------------------------------------

def train_model(model_name, model_checkpoint):
    print(f"\n{'=' * 60}")
    print(f"Training {model_name.upper()}")
    print(f"{'=' * 60}")

    tokenizer = AutoTokenizer.from_pretrained(
        model_checkpoint
    )

    train_dataset = load_data(
        "go_emotions_train.csv"
    )

    validation_dataset = load_data(
        "go_emotions_validation.csv"
    )

    test_dataset = load_data(
        "go_emotions_test.csv"
    )

    train_dataset = tokenize_dataset(
        train_dataset,
        tokenizer,
    )

    validation_dataset = tokenize_dataset(
        validation_dataset,
        tokenizer,
    )

    test_dataset = tokenize_dataset(
        test_dataset,
        tokenizer,
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        model_checkpoint,
        num_labels=len(EMOTIONS),
        problem_type="multi_label_classification",
    )

    output_dir = MODEL_DIR / model_name

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=1,
        weight_decay=0.01,
        logging_steps=50,
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        report_to="none",
        fp16=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=validation_dataset,
        processing_class=tokenizer,
        compute_metrics=compute_metrics,
    )

    trainer.train()

    test_results = trainer.evaluate(
        test_dataset
    )

    print(f"\n{model_name.upper()} TEST RESULTS")
    print(test_results)

    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    return test_results


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    results = {}

    for model_name, checkpoint in MODELS.items():
        results[model_name] = train_model(
            model_name,
            checkpoint,
        )

    with open(
        "reports/emotion_model_results.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            results,
            file,
            indent=4,
            default=float,
        )

    print("\nTraining completed successfully.")


if __name__ == "__main__":
    main()
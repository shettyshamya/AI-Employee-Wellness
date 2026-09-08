from pathlib import Path
import ast
import pandas as pd


RAW_DIR = Path("data/raw/go_emotions/simplified")
OUTPUT_DIR = Path("data/processed")

EMOTION_MAP = {
    17: "joy",
    25: "sadness",
    2: "anger",
    14: "fear",
    26: "surprise",
    11: "disgust",
}

TARGET_EMOTIONS = list(EMOTION_MAP.values())


def load_split(filename):
    path = RAW_DIR / filename
    df = pd.read_parquet(path)

    rows = []

    for _, row in df.iterrows():
        labels = row["labels"]

        if isinstance(labels, str):
            labels = ast.literal_eval(labels)

        selected_emotions = [
            EMOTION_MAP[label]
            for label in labels
            if label in EMOTION_MAP
        ]

        if not selected_emotions:
            continue

        result = {
            "text": str(row["text"]).strip(),
        }

        for emotion in TARGET_EMOTIONS:
            result[emotion] = int(emotion in selected_emotions)

        rows.append(result)

    return pd.DataFrame(rows)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    train_df = load_split("train-00000-of-00001.parquet")
    validation_df = load_split("validation-00000-of-00001.parquet")
    test_df = load_split("test-00000-of-00001.parquet")

    train_df.to_csv(
        OUTPUT_DIR / "go_emotions_train.csv",
        index=False,
    )

    validation_df.to_csv(
        OUTPUT_DIR / "go_emotions_validation.csv",
        index=False,
    )

    test_df.to_csv(
        OUTPUT_DIR / "go_emotions_test.csv",
        index=False,
    )

    print("GoEmotions preprocessing completed")
    print("Train shape:", train_df.shape)
    print("Validation shape:", validation_df.shape)
    print("Test shape:", test_df.shape)

    print("\nEmotion counts in training data:")
    print(train_df[TARGET_EMOTIONS].sum())


if __name__ == "__main__":
    main()
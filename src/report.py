import pandas as pd

from src.preprocessing import preprocess_text
from src.sentiment import analyze_sentiment


def generate_sentiment_report(csv_path):
    """
    Generate a sentiment report from employee feedback CSV.
    """

    # Read employee feedback
    df = pd.read_csv(csv_path)

    # Validate required columns
    required_columns = {"employee_id", "feedback"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "CSV must contain 'employee_id' and 'feedback' columns."
        )

    results = []

    for _, row in df.iterrows():

        employee_id = row["employee_id"]
        original_text = str(row["feedback"])

        # Preprocess text
        processed_text = preprocess_text(original_text)

        # Analyze original text using VADER
        sentiment_result = analyze_sentiment(original_text)

        if sentiment_result is None:
            continue

        results.append({
            "employee_id": employee_id,
            "original_text": original_text,
            "processed_text": processed_text,
            "sentiment": sentiment_result["sentiment"],
            "positive_score": sentiment_result["positive"],
            "negative_score": sentiment_result["negative"],
            "neutral_score": sentiment_result["neutral"],
            "compound_score": sentiment_result["compound"]
        })

    return pd.DataFrame(results)
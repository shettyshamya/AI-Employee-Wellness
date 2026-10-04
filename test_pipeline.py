import pandas as pd

from src.ingestion import read_csv_file
from src.preprocessing import preprocess_text
from src.sentiment import analyze_sentiment


CSV_PATH = "data/raw/employee_feedback.csv"


def test_complete_pipeline():
    # Step 1: Ingestion
    texts, message = read_csv_file(
        CSV_PATH,
        text_column="feedback",
    )

    assert message is not None
    assert texts is not None
    assert len(texts) > 0

    # Step 2: Preprocessing
    processed_texts = []

    for text in texts:
        processed = preprocess_text(text)
        processed_texts.append(processed)

    assert len(processed_texts) == len(texts)

    # Step 3: Sentiment analysis
    sentiments = []

    for text in texts:
        result = analyze_sentiment(text)
        sentiments.append(result)

    assert len(sentiments) == len(texts)

    for result in sentiments:
        assert result is not None
        assert "sentiment" in result
        assert "compound" in result

    # Step 4: Combine results
    results = []

    for i in range(len(texts)):
        results.append(
            {
                "original_text": texts[i],
                "processed_text": processed_texts[i],
                "sentiment": sentiments[i]["sentiment"],
                "compound_score": sentiments[i]["compound"],
            }
        )

    df = pd.DataFrame(results)

    # Step 5: Validation
    assert len(df) == len(texts)
    assert len(texts) == len(processed_texts)
    assert len(texts) == len(sentiments)

    assert "original_text" in df.columns
    assert "processed_text" in df.columns
    assert "sentiment" in df.columns
    assert "compound_score" in df.columns
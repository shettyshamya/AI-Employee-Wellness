import pandas as pd

from src.ingestion import read_csv_file
from src.preprocessing import preprocess_text
from src.sentiment import analyze_sentiment


CSV_PATH = "data/raw/employee_feedback.csv"


print("=" * 60)
print("MILESTONE 1 - COMPLETE PIPELINE TEST")
print("=" * 60)


# Step 1: Ingestion
print("\nSTEP 1: TEXT INGESTION")

texts, message = read_csv_file(
    CSV_PATH,
    text_column="feedback"
)

print(message)

if texts is None:
    print("Pipeline stopped: ingestion failed.")
    exit()

print("Number of inputs received:", len(texts))


# Step 2: Preprocessing
print("\nSTEP 2: PREPROCESSING")

processed_texts = []

for text in texts:
    processed = preprocess_text(text)
    processed_texts.append(processed)

print("Preprocessing completed.")
print("First processed text:", processed_texts[0])


# Step 3: Sentiment analysis
print("\nSTEP 3: VADER SENTIMENT ANALYSIS")

sentiments = []

for text in texts:
    result = analyze_sentiment(text)
    sentiments.append(result)

print("Sentiment analysis completed.")
print("First sentiment result:", sentiments[0])


# Step 4: Combine results
print("\nSTEP 4: PIPELINE OUTPUT")

results = []

for i in range(len(texts)):

    results.append({
        "original_text": texts[i],
        "processed_text": processed_texts[i],
        "sentiment": sentiments[i]["sentiment"],
        "compound_score": sentiments[i]["compound"]
    })


df = pd.DataFrame(results)

print(df.to_string(index=False))


# Step 5: Validation
print("\nSTEP 5: VALIDATION")

print("Input records:", len(texts))
print("Processed records:", len(processed_texts))
print("Sentiment records:", len(sentiments))

if (
    len(texts)
    == len(processed_texts)
    == len(sentiments)
):
    print("PASS: All modules processed the same number of records.")
else:
    print("FAIL: Record count mismatch.")


print("\n" + "=" * 60)
print("COMPLETE PIPELINE TEST FINISHED")
print("=" * 60)
import pandas as pd

from src.preprocessing import preprocess_text
from src.sentiment import analyze_sentiment


# ============================================================
# REAL DATASET - MILESTONE 1 VALIDATION
# ============================================================

INPUT_FILE = "data/raw/stress_dataset.csv"
OUTPUT_FILE = "reports/milestone1_real_dataset_report.csv"


print("=" * 70)
print("MILESTONE 1 - REAL DATASET SENTIMENT VALIDATION")
print("=" * 70)


# ------------------------------------------------------------
# STEP 1: LOAD DATASET
# ------------------------------------------------------------

print("\nSTEP 1: DATASET LOADING")

df = pd.read_csv(INPUT_FILE)

print("Dataset successfully loaded.")
print("Total records:", len(df))
print("Columns:", df.columns.tolist())


# ------------------------------------------------------------
# STEP 2: VALIDATE REQUIRED COLUMN
# ------------------------------------------------------------

print("\nSTEP 2: INPUT VALIDATION")

if "Message" not in df.columns:
    print("ERROR: 'Message' column not found.")
    exit()

print("Required 'Message' column found.")


# ------------------------------------------------------------
# STEP 3: CHECK EMPTY VALUES
# ------------------------------------------------------------

print("\nSTEP 3: EMPTY INPUT VALIDATION")

empty_messages = df["Message"].isna().sum()

print("Empty messages found:", empty_messages)

# Remove empty messages
df = df.dropna(subset=["Message"])

# Remove whitespace-only messages
df = df[df["Message"].astype(str).str.strip() != ""]

print("Valid text records:", len(df))


# ------------------------------------------------------------
# STEP 4: PREPROCESSING
# ------------------------------------------------------------

print("\nSTEP 4: PREPROCESSING")

df["processed_text"] = df["Message"].apply(preprocess_text)

print("Preprocessing completed.")

print("\nExample:")
print("Original :", df.iloc[0]["Message"])
print("Processed:", df.iloc[0]["processed_text"])


# ------------------------------------------------------------
# STEP 5: VADER SENTIMENT
# ------------------------------------------------------------

print("\nSTEP 5: VADER SENTIMENT ANALYSIS")

sentiment_results = df["Message"].apply(analyze_sentiment)

df["sentiment"] = sentiment_results.apply(
    lambda x: x["sentiment"] if x else None
)

df["positive_score"] = sentiment_results.apply(
    lambda x: x["positive"] if x else None
)

df["negative_score"] = sentiment_results.apply(
    lambda x: x["negative"] if x else None
)

df["neutral_score"] = sentiment_results.apply(
    lambda x: x["neutral"] if x else None
)

df["compound_score"] = sentiment_results.apply(
    lambda x: x["compound"] if x else None
)

print("VADER analysis completed.")


# ------------------------------------------------------------
# STEP 6: SENTIMENT DISTRIBUTION
# ------------------------------------------------------------

print("\nSTEP 6: SENTIMENT DISTRIBUTION")

sentiment_counts = df["sentiment"].value_counts()

print(sentiment_counts)


# ------------------------------------------------------------
# STEP 7: SAVE REPORT
# ------------------------------------------------------------

print("\nSTEP 7: REPORT GENERATION")

df.to_csv(OUTPUT_FILE, index=False)

print("Report successfully generated.")
print("Saved to:", OUTPUT_FILE)


# ------------------------------------------------------------
# STEP 8: FINAL VALIDATION
# ------------------------------------------------------------

print("\nSTEP 8: FINAL VALIDATION")

print("Original dataset records:", len(pd.read_csv(INPUT_FILE)))
print("Valid text records:", len(df))
print("Processed records:", df["processed_text"].notna().sum())
print("Sentiment records:", df["sentiment"].notna().sum())

if (
    len(df)
    == df["processed_text"].notna().sum()
    == df["sentiment"].notna().sum()
):
    print("\nPASS: Complete real-dataset pipeline executed successfully.")
else:
    print("\nFAIL: Record mismatch detected.")


print("\n" + "=" * 70)
print("REAL DATASET MILESTONE 1 TEST COMPLETE")
print("=" * 70)
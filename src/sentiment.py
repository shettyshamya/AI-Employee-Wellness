from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Create VADER analyzer
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    """
    Analyze the sentiment of employee feedback using VADER.
    Returns positive, negative, neutral and compound scores.
    """

    if text is None or not text.strip():
        return None

    scores = analyzer.polarity_scores(text)

    # Determine sentiment classification
    if scores["compound"] >= 0.05:
        sentiment = "Positive"
    elif scores["compound"] <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "positive": scores["pos"],
        "negative": scores["neg"],
        "neutral": scores["neu"],
        "compound": scores["compound"]
    }
from src.sentiment import analyze_sentiment


def test_positive_sentiment():
    text = (
        "I really enjoy my work "
        "and feel happy with my team 😊"
    )

    result = analyze_sentiment(text)

    assert result is not None
    assert "sentiment" in result
    assert "positive" in result
    assert "negative" in result
    assert "neutral" in result
    assert "compound" in result


def test_negative_sentiment():
    text = (
        "I am feeling very stressed "
        "because of my workload 😔"
    )

    result = analyze_sentiment(text)

    assert result is not None
    assert "sentiment" in result
    assert "positive" in result
    assert "negative" in result
    assert "neutral" in result
    assert "compound" in result


def test_neutral_sentiment():
    text = (
        "I attended the employee meeting today."
    )

    result = analyze_sentiment(text)

    assert result is not None
    assert "sentiment" in result
    assert "compound" in result


def test_strong_positive_sentiment():
    text = (
        "I am extremely excited and happy "
        "about the amazing new project! 🎉"
    )

    result = analyze_sentiment(text)

    assert result is not None
    assert result["sentiment"] == "Positive"


def test_strong_negative_sentiment():
    text = (
        "I am extremely frustrated, exhausted "
        "and unhappy with my workload."
    )

    result = analyze_sentiment(text)

    assert result is not None
    assert result["sentiment"] == "Negative"


def test_empty_input():
    text = ""

    result = analyze_sentiment(text)

    assert result is None


def test_negation():
    text = (
        "I am not happy with my workload."
    )

    result = analyze_sentiment(text)

    assert result is not None
    assert "sentiment" in result
    assert "compound" in result
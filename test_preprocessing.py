from src.preprocessing import preprocess_text


def test_basic_preprocessing():
    text = (
        "I am feeling very stressed because of my workload!!!"
    )

    processed = preprocess_text(text)

    assert processed is not None
    assert isinstance(processed, str)
    assert processed.strip() != ""


def test_positive_employee_feedback():
    text = (
        "I really enjoy working with my team "
        "and I feel happy 😊"
    )

    processed = preprocess_text(text)

    assert processed is not None
    assert isinstance(processed, str)
    assert processed.strip() != ""


def test_negative_employee_feedback():
    text = (
        "I am extremely frustrated and tired "
        "because of my workload 😔"
    )

    processed = preprocess_text(text)

    assert processed is not None
    assert isinstance(processed, str)
    assert processed.strip() != ""


def test_neutral_employee_feedback():
    text = (
        "I attended the employee meeting today."
    )

    processed = preprocess_text(text)

    assert processed is not None
    assert isinstance(processed, str)
    assert processed.strip() != ""


def test_empty_text():
    text = ""

    processed = preprocess_text(text)

    assert processed is None


def test_repeated_spaces():
    text = (
        "I    feel     very     happy     today 😊"
    )

    processed = preprocess_text(text)

    assert processed is not None
    assert isinstance(processed, str)
    assert processed.strip() != ""


def test_special_characters_and_emojis():
    text = (
        "I am VERY happy!!! 😊🎉 #great @team"
    )

    processed = preprocess_text(text)

    assert processed is not None
    assert isinstance(processed, str)
    assert processed.strip() != ""


def test_lemmatization():
    text = (
        "Employees are working harder "
        "and feeling exhausted."
    )

    processed = preprocess_text(text)

    assert processed is not None
    assert isinstance(processed, str)
    assert processed.strip() != ""


def test_negation():
    text = (
        "I am not happy with my workload."
    )

    processed = preprocess_text(text)

    assert processed is not None
    assert isinstance(processed, str)
    assert processed.strip() != ""


def test_very_short_emotional_text():
    text = "Sad."

    processed = preprocess_text(text)

    assert processed is not None
    assert isinstance(processed, str)


def test_long_employee_feedback():
    text = """
    I have been feeling extremely stressed and anxious because
    my workload has increased significantly over the past few
    weeks. I am finding it difficult to maintain a healthy
    work-life balance, and I often feel exhausted after work.
    However, I still enjoy working with my team and I am excited
    about the upcoming project.
    """

    processed = preprocess_text(text)

    assert processed is not None
    assert isinstance(processed, str)
    assert processed.strip() != ""
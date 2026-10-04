from pathlib import Path

from src.ingestion import (
    read_text_input,
    read_txt_file,
    read_csv_file,
    read_pdf_file,
    read_docx_file,
)


def test_positive_employee_feedback():
    text, message = read_text_input(
        "I really enjoy my work and feel happy with my team 😊"
    )

    assert text is not None
    assert text.strip() != ""
    assert message is not None


def test_negative_employee_feedback():
    text, message = read_text_input(
        "I am feeling very stressed because of my workload 😔"
    )

    assert text is not None
    assert text.strip() != ""
    assert message is not None


def test_neutral_employee_feedback():
    text, message = read_text_input(
        "I attended the employee meeting today."
    )

    assert text is not None
    assert text.strip() != ""
    assert message is not None


def test_empty_input():
    text, message = read_text_input("")

    assert text is None or text == ""
    assert message is not None


def test_whitespace_only_input():
    text, message = read_text_input("     ")

    assert text is None or text == ""
    assert message is not None


def test_very_short_input():
    text, message = read_text_input("Good")

    assert text is not None
    assert text.strip() != ""
    assert message is not None


def test_special_characters_and_emojis():
    text, message = read_text_input(
        "I am VERY happy!!! 😊🎉 #great @team"
    )

    assert text is not None
    assert text.strip() != ""
    assert message is not None


def test_txt_file():
    file_path = Path(
        "data/raw/employee_feedback.txt"
    )

    if not file_path.exists():
        return

    text, message = read_txt_file(
        str(file_path)
    )

    assert message is not None
    assert text is not None


def test_csv_file():
    file_path = Path(
        "data/raw/employee_feedback.csv"
    )

    if not file_path.exists():
        return

    texts, message = read_csv_file(
        str(file_path),
        text_column="feedback",
    )

    assert message is not None
    assert texts is not None


def test_empty_txt_file():
    file_path = Path(
        "data/raw/employee_empty.txt"
    )

    if not file_path.exists():
        return

    text, message = read_txt_file(
        str(file_path)
    )

    assert message is not None


def test_empty_csv_file():
    file_path = Path(
        "data/raw/employee_empty.csv"
    )

    if not file_path.exists():
        return

    texts, message = read_csv_file(
        str(file_path),
        text_column="feedback",
    )

    assert message is not None


def test_csv_missing_feedback_column():
    file_path = Path(
        "data/raw/employee_invalid.csv"
    )

    if not file_path.exists():
        return

    texts, message = read_csv_file(
        str(file_path),
        text_column="feedback",
    )

    assert message is not None


def test_unsupported_file_type():
    file_path = Path(
        "data/raw/employee_feedback.jpg"
    )

    assert file_path.suffix.lower() == ".jpg"

    supported_extensions = [
        ".txt",
        ".csv",
        ".pdf",
        ".docx",
    ]

    assert (
        file_path.suffix.lower()
        not in supported_extensions
    )
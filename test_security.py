from pathlib import Path

import pandas as pd

from src.ingestion import (
    read_csv_file,
    read_docx_file,
    read_pdf_file,
    read_txt_file,
)
from src.report import (
    generate_sentiment_report,
    generate_wellness_report,
    wellness_report_to_csv,
)


def test_wellness_csv_excludes_private_message():
    analysis_records = [
        {
            "timestamp": "2026-10-04T10:00:00",
            "message": "PRIVATE EMPLOYEE WELLNESS MESSAGE",
            "emotion": "stress",
            "intensity": 0.8,
            "negative_intensity": 0.7,
            "polarity": "negative",
            "severity": "high",
        }
    ]

    report = generate_wellness_report(
        analysis_records,
        [],
    )

    csv_data = wellness_report_to_csv(report).decode("utf-8")

    assert "PRIVATE EMPLOYEE WELLNESS MESSAGE" not in csv_data
    assert "message" not in csv_data
    assert "emotion" in csv_data
    assert "intensity" in csv_data


def test_sentiment_report_excludes_employee_identity_and_raw_text(tmp_path):
    csv_path = tmp_path / "feedback.csv"

    pd.DataFrame(
        {
            "employee_id": ["EMP-001"],
            "feedback": ["PRIVATE EMPLOYEE FEEDBACK"],
        }
    ).to_csv(csv_path, index=False)

    report = generate_sentiment_report(csv_path)

    assert "employee_id" not in report.columns
    assert "original_text" not in report.columns
    assert "processed_text" not in report.columns
    assert "PRIVATE EMPLOYEE FEEDBACK" not in report.to_string()


def test_txt_error_does_not_expose_path():
    private_path = Path("definitely_missing_private_file.txt")

    result, message = read_txt_file(private_path)

    assert result is None
    assert "definitely_missing_private_file.txt" not in message
    assert "Error reading" in message or "Unable to read" in message


def test_csv_error_does_not_expose_path():
    private_path = Path("definitely_missing_private_file.csv")

    result, message = read_csv_file(private_path)

    assert result is None
    assert "definitely_missing_private_file.csv" not in message


def test_pdf_error_does_not_expose_path():
    private_path = Path("definitely_missing_private_file.pdf")

    result, message = read_pdf_file(private_path)

    assert result is None
    assert "definitely_missing_private_file.pdf" not in message


def test_docx_error_does_not_expose_path():
    private_path = Path("definitely_missing_private_file.docx")

    result, message = read_docx_file(private_path)

    assert result is None
    assert "definitely_missing_private_file.docx" not in message


def test_sensitive_feedback_file_is_gitignored():
    gitignore = Path(".gitignore").read_text(
        encoding="utf-8"
    )

    assert (
        gitignore.count(
            "data/processed/recommendation_feedback.json"
        )
        == 1
    )
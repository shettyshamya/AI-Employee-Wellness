import pandas as pd
import pymupdf
from docx import Document


def validate_text(text):
    """Validate employee wellness text."""

    if text is None:
        return False, "No text provided."

    if not isinstance(text, str):
        return False, "Invalid text format."

    if not text.strip():
        return False, "The input text is empty."

    return True, "Valid text."


def read_text_input(text):
    """Read text entered directly by an employee."""

    is_valid, message = validate_text(text)

    if not is_valid:
        return None, message

    return text.strip(), "Text input successfully received."


def read_txt_file(file_path):
    """Read employee feedback from a TXT file."""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        is_valid, message = validate_text(text)

        if not is_valid:
            return None, message

        return text.strip(), "TXT file successfully read."

    except Exception as e:
        return None, f"Error reading TXT file: {e}"


def read_csv_file(file_path, text_column=None):
    """Read employee feedback from a CSV file."""

    try:
        df = pd.read_csv(file_path)

        if df.empty:
            return None, "CSV file is empty."

        if text_column:
            if text_column not in df.columns:
                return None, f"Column '{text_column}' not found."

            texts = df[text_column].dropna().astype(str).tolist()
        else:
            texts = df.iloc[:, 0].dropna().astype(str).tolist()

        texts = [text.strip() for text in texts if text.strip()]

        if not texts:
            return None, "No valid text found in CSV."

        return texts, "CSV file successfully read."

    except Exception as e:
        return None, f"Error reading CSV file: {e}"


def read_pdf_file(file_path):
    """Extract text from a PDF file."""

    try:
        document = pymupdf.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        is_valid, message = validate_text(text)

        if not is_valid:
            return None, message

        return text.strip(), "PDF file successfully read."

    except Exception as e:
        return None, f"Error reading PDF file: {e}"


def read_docx_file(file_path):
    """Extract text from a Word document."""

    try:
        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text.strip())

        text = "\n".join(paragraphs)

        is_valid, message = validate_text(text)

        if not is_valid:
            return None, message

        return text, "Word document successfully read."

    except Exception as e:
        return None, f"Error reading DOCX file: {e}"
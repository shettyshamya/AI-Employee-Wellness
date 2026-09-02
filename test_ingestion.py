from src.ingestion import read_text_input


# Test 1: Positive employee feedback
text, message = read_text_input(
    "I really enjoy my work and feel happy with my team 😊"
)

print("Test 1:")
print(message)
print("Text:", text)
print()


# Test 2: Negative employee feedback
text, message = read_text_input(
    "I am feeling very stressed because of my workload 😔"
)

print("Test 2:")
print(message)
print("Text:", text)
print()


# Test 3: Neutral employee feedback
text, message = read_text_input(
    "I attended the employee meeting today."
)

print("Test 3:")
print(message)
print("Text:", text)
print()


# Test 4: Empty input
text, message = read_text_input("")

print("Test 4:")
print(message)
print("Text:", text)

from src.ingestion import read_txt_file

print("Test 5: TXT File")

text, message = read_txt_file(
    "data/raw/employee_feedback.txt"
)

print(message)
print("Text:", text)

from src.ingestion import read_csv_file

print("\nTest 6: CSV File")

texts, message = read_csv_file(
    "data/raw/employee_feedback.csv",
    text_column="feedback"
)

print(message)

if texts:
    for i, text in enumerate(texts, start=1):
        print(f"Employee {i}: {text}")

        from src.ingestion import read_pdf_file

print("\nTest 7: PDF File")

text, message = read_pdf_file(
    "data/raw/employee_feedback.pdf"
)

print(message)
print("Extracted Text:")
print(text)

from src.ingestion import read_docx_file

print("\nTest 8: DOCX File")

text, message = read_docx_file(
    "data/raw/employee_feedback.docx"
)

print(message)
print("Extracted Text:")
print(text)

print("\nTest 9: Whitespace-only Input")

text, message = read_text_input("     ")

print(message)
print("Text:", text)

print("\nTest 10: Very Short Input")

text, message = read_text_input("Good")

print(message)
print("Text:", text)

print("\nTest 11: Special Characters and Emojis")

text, message = read_text_input(
    "I am VERY happy!!! 😊🎉 #great @team"
)

print(message)
print("Text:", text)

from src.ingestion import read_txt_file

print("\nTest 12: Empty TXT File")

text, message = read_txt_file(
    "data/raw/employee_empty.txt"
)

print(message)
print("Text:", text)

from src.ingestion import read_txt_file

print("\nTest 12: Empty TXT File")

text, message = read_txt_file(
    "data/raw/employee_empty.txt"
)

print(message)
print("Text:", text)

print("\nTest 13: Empty CSV File")

texts, message = read_csv_file(
    "data/raw/employee_empty.csv",
    text_column="feedback"
)

print(message)
print("Texts:", texts)

print("\nTest 14: CSV Missing Feedback Column")

texts, message = read_csv_file(
    "data/raw/employee_invalid.csv",
    text_column="feedback"
)

print(message)
print("Texts:", texts)

print("\nTest 15: Unsupported File Type")

file_path = "data/raw/employee_feedback.jpg"

supported_extensions = [".txt", ".csv", ".pdf", ".docx"]

import os

extension = os.path.splitext(file_path)[1].lower()

if extension not in supported_extensions:
    print("Unsupported file type.")
    print("Text: None")
from src.report import generate_sentiment_report


csv_path = "data/raw/employee_feedback.csv"


print("Generating Milestone 1 Sentiment Report...\n")

report = generate_sentiment_report(csv_path)


print("Report generated successfully!\n")

print(report.to_string(index=False))


print("\nNumber of analyzed samples:", len(report))


# Save report
output_path = "reports/milestone1_sentiment_report.csv"

report.to_csv(output_path, index=False)

print("\nReport saved to:", output_path)
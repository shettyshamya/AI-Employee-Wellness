import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from src.preprocessing import preprocess_text
from src.sentiment import analyze_sentiment

SAFE_ANALYSIS_COLUMNS = [
    "timestamp",
    "emotion",
    "intensity",
    "negative_intensity",
    "polarity",
    "severity",
]


def _privacy_safe_analysis_dataframe(analysis_df):
    """Return only non-identifying wellness analysis fields."""
    if analysis_df.empty:
        return pd.DataFrame(columns=SAFE_ANALYSIS_COLUMNS)

    safe_df = analysis_df.reindex(
        columns=[
            column
            for column in SAFE_ANALYSIS_COLUMNS
            if column in analysis_df.columns
        ]
    )

    return safe_df.copy()
def wellness_report_to_csv(report):
    """Export a privacy-safe wellness analysis CSV."""

    analysis_df = _privacy_safe_analysis_dataframe(
        report["analysis"]
    )

    return analysis_df.to_csv(index=False).encode("utf-8")


def generate_sentiment_report(csv_path):
    """
    Generate a privacy-safe sentiment report from employee feedback CSV.
    """

    # Read employee feedback
    df = pd.read_csv(csv_path)

    # Validate required columns
    required_columns = {"employee_id", "feedback"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "CSV must contain 'employee_id' and 'feedback' columns."
        )

    results = []

    for _, row in df.iterrows():

        employee_id = row["employee_id"]
        original_text = str(row["feedback"])

        # Preprocess text
        processed_text = preprocess_text(original_text)

        # Analyze original text using VADER
        sentiment_result = analyze_sentiment(original_text)

        if sentiment_result is None:
            continue

        results.append({
            "sentiment": sentiment_result["sentiment"],
            "positive_score": sentiment_result["positive"],
            "negative_score": sentiment_result["negative"],
            "neutral_score": sentiment_result["neutral"],
            "compound_score": sentiment_result["compound"],
        })

    return pd.DataFrame(results)

def generate_wellness_report(
    analysis_records,
    feedback_records,
):
    """
    Generate a wellness report from dashboard session data.

    Returns a dictionary containing:
    - emotional analysis records
    - recommendation feedback records
    - summary statistics
    """

    analysis_df = pd.DataFrame(analysis_records)
    feedback_df = pd.DataFrame(feedback_records)

    summary = {
        "total_emotional_entries": len(analysis_df),
        "total_feedback_entries": len(feedback_df),
        "average_intensity": 0.0,
        "average_negative_intensity": 0.0,
        "most_common_emotion": "N/A",
        "feedback_acceptance_rate": None,
        "average_recommendation_rating": 0.0,
    }

    if not analysis_df.empty:

        if "intensity" in analysis_df.columns:
            summary["average_intensity"] = round(
                pd.to_numeric(
                    analysis_df["intensity"],
                    errors="coerce",
                ).mean(),
                2,
            )

        if "negative_intensity" in analysis_df.columns:
            summary["average_negative_intensity"] = round(
                pd.to_numeric(
                    analysis_df["negative_intensity"],
                    errors="coerce",
                ).mean(),
                2,
            )

        if "emotion" in analysis_df.columns:
            emotions = (
                analysis_df["emotion"]
                .dropna()
                .astype(str)
            )

            if not emotions.empty:
                summary["most_common_emotion"] = (
                    emotions.value_counts().idxmax()
                )

    if not feedback_df.empty:

        if "accepted" in feedback_df.columns:

            decisions = feedback_df[
                feedback_df["accepted"].notna()
            ]["accepted"]

            if not decisions.empty:
                summary["feedback_acceptance_rate"] = round(
                    decisions.eq(True).mean(),
                    2,
                )

        if "rating" in feedback_df.columns:

            ratings = pd.to_numeric(
                feedback_df["rating"],
                errors="coerce",
            ).dropna()

            if not ratings.empty:
                summary["average_recommendation_rating"] = round(
                    ratings.mean(),
                    2,
                )

    return {
        "analysis": analysis_df,
        "feedback": feedback_df,
        "summary": summary,
    }


def wellness_report_to_pdf(report):
    """
    Convert wellness report data to a PDF document.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=letter,
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Employee Wellness Report",
            styles["Title"],
        )
    )

    story.append(
        Spacer(1, 12)
    )

    summary = report["summary"]

    summary_data = [
        ["Metric", "Value"],
        [
            "Total Emotional Entries",
            str(summary["total_emotional_entries"]),
        ],
        [
            "Total Feedback Entries",
            str(summary["total_feedback_entries"]),
        ],
        [
            "Average Intensity",
            str(summary["average_intensity"]),
        ],
        [
            "Average Negative Intensity",
            str(summary["average_negative_intensity"]),
        ],
        [
            "Most Common Emotion",
            str(summary["most_common_emotion"]),
        ],
        [
            "Feedback Acceptance Rate",
            str(summary["feedback_acceptance_rate"]),
        ],
        [
            "Average Recommendation Rating",
            str(summary["average_recommendation_rating"]),
        ],
    ]

    summary_table = Table(summary_data)

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.grey,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(summary_table)

    story.append(
        Spacer(1, 20)
    )

    analysis_df = report["analysis"]

    if not analysis_df.empty:

        story.append(
            Paragraph(
                "Emotional Analysis",
                styles["Heading2"],
            )
        )

        columns = [
            "timestamp",
            "emotion",
            "intensity",
            "negative_intensity",
            "severity",
        ]

        available_columns = [
            column
            for column in columns
            if column in analysis_df.columns
        ]

        table_data = [
            available_columns
        ]

        for _, row in analysis_df.iterrows():

            table_data.append(
                [
                    str(row.get(column, ""))
                    for column in available_columns
                ]
            )

        analysis_table = Table(
            table_data,
            repeatRows=1,
        )

        analysis_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.grey,
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.black,
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                ]
            )
        )

        story.append(analysis_table)

    document.build(story)

    return buffer.getvalue()
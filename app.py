import streamlit as st
import pandas as pd
from datetime import datetime

from src.wellness_pipeline import WellnessPipeline
from src.recommendation_feedback import RecommendationFeedback
from src.report import (
    generate_wellness_report,
    wellness_report_to_csv,
    wellness_report_to_pdf,
)

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="MoodMentor - Employee Wellness",
    page_icon="🧠",
    layout="wide",
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "pipeline" not in st.session_state:
    st.session_state.pipeline = WellnessPipeline(
        user_preferences={
            "preferred_categories": [
                "breathing",
                "mindfulness",
                "short_break",
            ]
        }
    )

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "recommendation_feedback" not in st.session_state:
    st.session_state.recommendation_feedback = (
        RecommendationFeedback()
    )

pipeline = st.session_state.pipeline


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def safe_float(value, default=0.0):
    """Safely convert a value to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def display_metric(label, value):
    """Display a dashboard metric."""
    st.metric(label, value)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🧠 MoodMentor")
st.subheader("AI Employee Wellness Dashboard")

st.write(
    "Analyze emotional states and receive personalized wellness "
    "recommendations based on the existing MoodMentor ML pipeline."
)

st.divider()


# ---------------------------------------------------------
# User input
# ---------------------------------------------------------

st.header("💬 Analyze Your Current State")

message = st.text_area(
    "How are you feeling?",
    placeholder=(
        "For example: I am feeling stressed about my workload "
        "and worried about tomorrow's deadline."
    ),
    height=130,
)

analyze_button = st.button(
    "🔍 Analyze & Recommend",
    type="primary",
)


# ---------------------------------------------------------
# Run pipeline
# ---------------------------------------------------------

if analyze_button:

    if not message.strip():
        st.warning("Please enter some text before running the analysis.")

    else:
        try:
            with st.spinner("Analyzing your emotional state..."):

                result = pipeline.process_message(message.strip())

                st.session_state.last_result = result

                st.session_state.analysis_history.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "message": message.strip(),
                        "emotion": result.get("current_emotion"),
                        "intensity": safe_float(
                            result.get("emotional_intensity")
                        ),
                        "negative_intensity": safe_float(
                            result.get("negative_emotion_intensity")
                        ),
                        "polarity": result.get("polarity"),
                        "severity": result.get("severity"),
                    }
                )

            st.success("Analysis completed successfully.")

        except Exception:
            st.error(
                "An error occurred while processing your message. "
                "Please try again."
            )


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

result = st.session_state.last_result

if result:

    st.divider()
    st.header("📊 Emotional Insights")

    # -----------------------------------------------------
    # Main emotional metrics
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        display_metric(
            "Dominant Emotion",
            str(result.get("current_emotion", "Unknown")).title(),
        )

    with col2:
        display_metric(
            "Emotional Intensity",
            f"{safe_float(result.get('emotional_intensity')):.2f}",
        )

    with col3:
        display_metric(
            "Negative Intensity",
            f"{safe_float(result.get('negative_emotion_intensity')):.2f}",
        )

    with col4:
        display_metric(
            "Severity",
            str(result.get("severity", "Unknown")).title(),
        )

    # -----------------------------------------------------
    # Emotional details
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Detected Emotions")

        detected_emotions = result.get(
            "detected_emotions",
            {},
        )

        if isinstance(detected_emotions, dict) and detected_emotions:

            emotion_df = pd.DataFrame(
                {
                    "Emotion": [
                        str(key).title()
                        for key in detected_emotions.keys()
                    ],
                    "Score": [
                        safe_float(value)
                        for value in detected_emotions.values()
                    ],
                }
            )

            emotion_df = emotion_df.sort_values(
                "Score",
                ascending=False,
            )

            st.bar_chart(
                emotion_df.set_index("Emotion")
            )

            st.dataframe(
                emotion_df,
                use_container_width=True,
                hide_index=True,
            )

        elif isinstance(detected_emotions, list):
            for emotion in detected_emotions:
                st.write(f"• {emotion}")

        else:
            st.info("No detailed emotion scores available.")

    with col2:
        st.subheader("Emotional State")

        polarity = result.get("polarity", "Unknown")

        st.metric(
            "Polarity",
            str(polarity).title(),
        )

        st.write(
            f"**Dominant emotion:** "
            f"{str(result.get('current_emotion', 'Unknown')).title()}"
        )

        st.write(
            f"**Intensity:** "
            f"{safe_float(result.get('emotional_intensity')):.2f}"
        )

        st.write(
            f"**Negative intensity:** "
            f"{safe_float(result.get('negative_emotion_intensity')):.2f}"
        )

        st.write(
            f"**Severity:** "
            f"{str(result.get('severity', 'Unknown')).title()}"
        )

    # -----------------------------------------------------
    # Recommendations
    # -----------------------------------------------------

    st.divider()
    st.header("🌱 Personalized Wellness Recommendations")

    recommendations = result.get(
        "recommendations",
        [],
    )

    if recommendations:

        for index, recommendation in enumerate(
            recommendations,
            start=1,
        ):

            title = recommendation.get(
                "title",
                "Wellness Recommendation",
            )

            score = safe_float(
                recommendation.get("score")
            )

            reasons = recommendation.get(
                "reasons",
                [],
            )

            with st.container(border=True):

                st.subheader(
                    f"{index}. {title}"
                )

                st.write(
                    f"**Recommendation score:** "
                    f"{score:.3f}"
                )

                if reasons:

                    st.write("**Why this was recommended:**")

                    for reason in reasons:
                        st.write(f"• {reason}")
                        st.write("**Your feedback:**")

                    recommendation_id = (
                        recommendation.get(
                            "id",
                            recommendation.get(
                                "title",
                                f"recommendation_{index}"
                            ),
                        )
                    )

                    feedback_col1, feedback_col2 = st.columns(2)

                    with feedback_col1:
                        accepted = st.radio(
                            "Was this recommendation useful?",
                            ["Not answered", "Yes", "No"],
                            key=f"accepted_{recommendation_id}_{index}",
                        )

                    with feedback_col2:
                        rating = st.selectbox(
                            "Rating",
                            [0, 1, 2, 3, 4, 5],
                            key=f"rating_{recommendation_id}_{index}",
                        )

                    if st.button(
                        "Submit Feedback",
                        key=f"feedback_button_{recommendation_id}_{index}",
                    ):
                        accepted_value = None

                        if accepted == "Yes":
                            accepted_value = True
                        elif accepted == "No":
                            accepted_value = False

                        rating_value = (
                            rating if rating > 0 else None
                        )

                        feedback_record = (
                            st.session_state
                            .recommendation_feedback
                            .record_feedback(
                                recommendation_id=str(
                                    recommendation_id
                                ),
                                viewed=True,
                                accepted=accepted_value,
                                rating=rating_value,
                                recommendation_category=recommendation.get(
                                    "category"
                                ),
                            )
                        )

                        st.success(
                            "Feedback saved successfully."
                        )
    else:
        st.info(
            "No recommendations were returned by the recommendation engine."
        )
        # -----------------------------------------------------
    # Recommendation history and feedback
    # -----------------------------------------------------

    st.divider()
    st.header("📝 Recommendation History")

    feedback_history = (
        st.session_state
        .recommendation_feedback
        .feedback_history
    )

    if feedback_history:
        feedback_df = pd.DataFrame(
            feedback_history
        )

        display_columns = [
            "recommendation_id",
            "viewed",
            "accepted",
            "rating",
            "timestamp",
        ]

        available_columns = [
            column
            for column in display_columns
            if column in feedback_df.columns
        ]

        st.dataframe(
            feedback_df[available_columns],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Feedback Summary")

        feedback_summary = (
            st.session_state
            .recommendation_feedback
            .get_feedback_summary()
        )

        if feedback_summary:
            summary_rows = []

            for recommendation_id, summary in (
                feedback_summary.items()
            ):
                summary_rows.append(
                    {
                        "Recommendation": recommendation_id,
                        "Interactions": summary[
                            "total_interactions"
                        ],
                        "Acceptance Rate": summary[
                            "acceptance_rate"
                        ],
                        "Average Rating": summary[
                            "average_rating"
                        ],
                    }
                )

            summary_df = pd.DataFrame(
                summary_rows
            )

            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True,
            )

    else:
        st.info(
            "No recommendation feedback has been "
            "submitted yet."
        )
    # -----------------------------------------------------
    # Trend summary
    # -----------------------------------------------------

    st.divider()
    st.header("📈 Wellness Trend Summary")

    trend_summary = result.get(
        "trend_summary",
        {},
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        display_metric(
            "Emotional Records",
            trend_summary.get(
                "total_emotional_records",
                0,
            ),
        )

    with col2:
        display_metric(
            "Average Intensity",
            f"{safe_float(trend_summary.get('average_emotional_intensity')):.2f}",
        )

    with col3:
        display_metric(
            "Average Negative Intensity",
            f"{safe_float(trend_summary.get('average_negative_emotion_intensity')):.2f}",
        )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Emotion Frequency")

        emotion_frequency = trend_summary.get(
            "emotion_frequency",
            {},
        )

        if emotion_frequency:
            frequency_df = pd.DataFrame(
                {
                    "Emotion": [
                        str(key).title()
                        for key in emotion_frequency.keys()
                    ],
                    "Count": list(
                        emotion_frequency.values()
                    ),
                }
            )

            st.bar_chart(
                frequency_df.set_index("Emotion")
            )

        else:
            st.info("No emotion frequency data available.")

    with col2:
        st.subheader("Polarity Distribution")

        polarity_distribution = trend_summary.get(
            "polarity_distribution",
            {},
        )

        if polarity_distribution:
            polarity_df = pd.DataFrame(
                {
                    "Polarity": [
                        str(key).title()
                        for key in polarity_distribution.keys()
                    ],
                    "Count": list(
                        polarity_distribution.values()
                    ),
                }
            )

            st.bar_chart(
                polarity_df.set_index("Polarity")
            )

        else:
            st.info("No polarity distribution available.")

st.subheader("Emotional Trends Over Time")

trend_period = st.selectbox(
    "Trend Period",
    ["Daily", "Weekly", "Monthly"]
)

if trend_period == "Daily":
    trend_data = (
        st.session_state.pipeline
        .trend_analyzer
        .get_daily_trends()
    )
elif trend_period == "Weekly":
    trend_data = (
        st.session_state.pipeline
        .trend_analyzer
        .get_weekly_trends()
    )
else:
    trend_data = (
        st.session_state.pipeline
        .trend_analyzer
        .get_monthly_trends()
    )

if trend_data:
    trend_df = pd.DataFrame(trend_data)

    st.line_chart(
        trend_df.set_index("period")[
            [
                "average_intensity",
                "average_negative_intensity"
            ]
        ]
    )

    st.dataframe(
        trend_df,
        use_container_width=True
    )

else:
    st.info(
        "No historical trend data is available yet. "
        "Analyze some messages to build your emotional history."
    )
# ---------------------------------------------------------
# Advanced Search and Filtering
# ---------------------------------------------------------

st.divider()
st.header("🔎 Advanced Search & Filtering")

analysis_records = st.session_state.analysis_history

feedback_records = (
    st.session_state
    .recommendation_feedback
    .feedback_history
)

if analysis_records or feedback_records:

    # -----------------------------------------------------
    # Filter controls
    # -----------------------------------------------------

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    # -----------------------------------------------------
    # Emotion filter
    # -----------------------------------------------------

    with filter_col1:

        available_emotions = sorted(
            {
                str(record.get("emotion"))
                for record in analysis_records
                if record.get("emotion")
            }
        )

        selected_emotion = st.selectbox(
            "Emotion",
            ["All"] + available_emotions,
        )

    # -----------------------------------------------------
    # Intensity filter
    # -----------------------------------------------------

    with filter_col2:

        intensity_range = st.slider(
            "Emotional Intensity",
            min_value=0.0,
            max_value=100.0,
            value=(0.0, 100.0),
            step=1.0,
        )

    # -----------------------------------------------------
    # Feedback status filter
    # -----------------------------------------------------

    with filter_col3:

        feedback_status = st.selectbox(
            "Feedback Status",
            [
                "All",
                "Accepted",
                "Rejected",
                "Not Rated",
            ],
        )
        # -----------------------------------------------------
    # Recommendation type filter
    # -----------------------------------------------------

    with filter_col4:

        available_categories = sorted(
            {
                str(record.get("category"))
                for record in feedback_records
                if record.get("category")
            }
        )

        selected_category = st.selectbox(
            "Recommendation Type",
            ["All"] + available_categories,
        )
    # -----------------------------------------------------
    # Date range filter
    # -----------------------------------------------------

    st.subheader("📅 Date Range")

    if analysis_records:

        timestamps = []

        for record in analysis_records:

            timestamp = record.get("timestamp")

            if timestamp:

                try:
                    timestamps.append(
                        pd.to_datetime(timestamp)
                    )

                except Exception:
                    pass

        if timestamps:

            min_date = min(
                timestamps
            ).date()

            max_date = max(
                timestamps
            ).date()

            selected_dates = st.date_input(
                "Select date range",
                value=(
                    min_date,
                    max_date,
                ),
                min_value=min_date,
                max_value=max_date,
            )

        else:
            selected_dates = None

    else:
        selected_dates = None

    # -----------------------------------------------------
    # Filter emotional records
    # -----------------------------------------------------

    filtered_analysis = []

    for record in analysis_records:

        include_record = True

        # Emotion filter
        if (
            selected_emotion != "All"
            and str(record.get("emotion"))
            != selected_emotion
        ):
            include_record = False

        # Intensity filter
        intensity = safe_float(
            record.get("intensity")
        )

        if not (
            intensity_range[0]
            <= intensity
            <= intensity_range[1]
        ):
            include_record = False

        # Date filter
        if (
            selected_dates
            and record.get("timestamp")
        ):

            try:

                record_date = pd.to_datetime(
                    record["timestamp"]
                ).date()

                if (
                    isinstance(
                        selected_dates,
                        tuple,
                    )
                    and len(selected_dates) == 2
                ):

                    start_date, end_date = (
                        selected_dates
                    )

                    if not (
                        start_date
                        <= record_date
                        <= end_date
                    ):
                        include_record = False

            except Exception:
                pass

        if include_record:
            filtered_analysis.append(
                record
            )

    # -----------------------------------------------------
    # Display filtered emotional records
    # -----------------------------------------------------

    st.subheader(
        "🧠 Filtered Emotional Records"
    )

    if filtered_analysis:

        filtered_analysis_df = pd.DataFrame(
            filtered_analysis
        )

        st.dataframe(
            filtered_analysis_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No emotional records match "
            "the selected filters."
        )

    # -----------------------------------------------------
    # Filter recommendation feedback
    # -----------------------------------------------------

    filtered_feedback = []

    for record in feedback_records:

        include_feedback = True

        accepted = record.get(
            "accepted"
        )

        rating = record.get(
            "rating"
        )
        category = record.get(
            "recommendation_category"
        )

        if (
            selected_category != "All"
            and category != selected_category
        ):
            include_feedback = False

        if feedback_status == "Accepted":

            if accepted is not True:
                include_feedback = False

        elif feedback_status == "Rejected":

            if accepted is not False:
                include_feedback = False

        elif feedback_status == "Not Rated":

            if rating is not None:
                include_feedback = False

        if include_feedback:
            filtered_feedback.append(
                record
            )

    # -----------------------------------------------------
    # Display filtered recommendations
    # -----------------------------------------------------

    st.subheader(
        "🌱 Filtered Recommendation History"
    )

    if filtered_feedback:

        feedback_filter_df = pd.DataFrame(
            filtered_feedback
        )

        st.dataframe(
            feedback_filter_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No recommendation records match "
            "the selected feedback filter."
        )

else:

    st.info(
        "Analyze messages and submit recommendation "
        "feedback to use advanced filtering."
    )

# ---------------------------------------------------------
# Report Generation and Export
# ---------------------------------------------------------

st.divider()
st.header("📄 Report Generation & Export")

report_analysis_records = (
    st.session_state.analysis_history
)

report_feedback_records = (
    st.session_state
    .recommendation_feedback
    .feedback_history
)

if (
    report_analysis_records
    or report_feedback_records
):

    report_start_date = st.date_input(
        "Report Start Date",
        value=(
            datetime.now().date()
        ),
        key="report_start_date",
    )

    report_end_date = st.date_input(
        "Report End Date",
        value=(
            datetime.now().date()
        ),
        key="report_end_date",
    )

    if report_start_date > report_end_date:

        st.error(
            "Report start date must be before "
            "or equal to the end date."
        )

    else:

        filtered_analysis = []

        for record in report_analysis_records:

            timestamp = record.get("timestamp")

            if not timestamp:
                continue

            try:
                record_date = (
                    datetime.fromisoformat(
                        timestamp
                    ).date()
                )
            except ValueError:
                continue

            if (
                report_start_date
                <= record_date
                <= report_end_date
            ):
                filtered_analysis.append(record)

        filtered_feedback = []

        for record in report_feedback_records:

            timestamp = record.get("timestamp")

            if not timestamp:
                continue

            try:
                record_date = (
                    datetime.fromisoformat(
                        timestamp
                    ).date()
                )
            except ValueError:
                continue

            if (
                report_start_date
                <= record_date
                <= report_end_date
            ):
                filtered_feedback.append(record)

        report = generate_wellness_report(
            filtered_analysis,
            filtered_feedback,
        )

        summary = report["summary"]

        st.subheader("Report Summary")

        summary_col1, summary_col2, summary_col3 = (
            st.columns(3)
        )

        with summary_col1:
            st.metric(
                "Emotional Entries",
                summary[
                    "total_emotional_entries"
                ],
            )

        with summary_col2:
            st.metric(
                "Feedback Entries",
                summary[
                    "total_feedback_entries"
                ],
            )

        with summary_col3:
            st.metric(
                "Most Common Emotion",
                summary[
                    "most_common_emotion"
                ],
            )

        st.write(
            "Average Intensity:",
            summary[
                "average_intensity"
            ],
        )

        st.write(
            "Average Negative Intensity:",
            summary[
                "average_negative_intensity"
            ],
        )

        st.write(
            "Feedback Acceptance Rate:",
            summary[
                "feedback_acceptance_rate"
            ],
        )

        st.write(
            "Average Recommendation Rating:",
            summary[
                "average_recommendation_rating"
            ],
        )

        csv_data = wellness_report_to_csv(
            report
        )

        pdf_data = wellness_report_to_pdf(
            report
        )

        download_col1, download_col2 = (
            st.columns(2)
        )

        with download_col1:

            st.download_button(
                label="⬇️ Download CSV Report",
                data=csv_data,
                file_name=(
                    "wellness_report.csv"
                ),
                mime="text/csv",
            )

        with download_col2:

            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_data,
                file_name=(
                    "wellness_report.pdf"
                ),
                mime="application/pdf",
            )

        if filtered_analysis:

            st.subheader(
                "Report Emotional Data"
            )

            st.dataframe(
                pd.DataFrame(
                    filtered_analysis
                ),
                use_container_width=True,
            )

        if filtered_feedback:

            st.subheader(
                "Report Recommendation Feedback"
            )

            st.dataframe(
                pd.DataFrame(
                    filtered_feedback
                ),
                use_container_width=True,
            )

else:

    st.info(
        "No wellness data is available yet. "
        "Analyze some messages and submit "
        "recommendation feedback to generate "
        "a report."
    )
# ---------------------------------------------------------
# Session history
# ---------------------------------------------------------

st.divider()
st.header("🕘 Current Session History")

history = st.session_state.analysis_history

if history:

    history_df = pd.DataFrame(history)

    history_df.index = history_df.index + 1

    st.dataframe(
        history_df,
        use_container_width=True,
    )

else:
    st.info(
        "No analyses have been performed in this session yet."
    )


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.title("MoodMentor")

    st.caption(
        "AI-powered employee wellness and emotional insights."
    )

    st.divider()

    st.subheader("Dashboard")

    st.write(
        "Use the text box to analyze an emotional state and "
        "receive personalized wellness recommendations."
    )

    st.divider()

    st.subheader("Current Session")

    st.write(
        f"Analyses performed: "
        f"**{len(st.session_state.analysis_history)}**"
    )

    if st.button("Clear Session History"):

        st.session_state.analysis_history = []
        st.session_state.last_result = None

        # Recreate the pipeline so its internal trend history
        # is also reset.
        st.session_state.pipeline = WellnessPipeline(
            user_preferences={
                "preferred_categories": [
                    "breathing",
                    "mindfulness",
                    "short_break",
                ]
            }
        )

        st.rerun()
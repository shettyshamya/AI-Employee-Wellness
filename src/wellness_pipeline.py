import argparse
from pathlib import Path

from src.ingestion import (
    read_txt_file,
    read_csv_file,
    read_pdf_file,
    read_docx_file,
)
from datetime import datetime, timezone
try:
    from src.emotion_analyzer import EmotionAnalyzer
    from src.personalized_recommender import PersonalizedRecommender
    from src.wellness_trend_analyzer import WellnessTrendAnalyzer
except ModuleNotFoundError:
    from emotion_analyzer import EmotionAnalyzer
    from personalized_recommender import PersonalizedRecommender
    from wellness_trend_analyzer import WellnessTrendAnalyzer

class WellnessPipeline:
    def __init__(self, user_preferences=None):
        self.emotion_analyzer = EmotionAnalyzer()

        self.recommender = PersonalizedRecommender(
            user_preferences=user_preferences or {}
        )

        self.trend_analyzer = WellnessTrendAnalyzer()

    def process_message(self, message):
        # Step 1: Analyze the employee's emotion
        emotional_state = self.emotion_analyzer.analyze(message)

        # Add a real timestamp for emotional trend analysis
        emotional_state["timestamp"] = datetime.now(
            timezone.utc
        ).isoformat()

        # Step 2: Update emotional trend history
        self.trend_analyzer.add_emotional_state(
            emotional_state
        )

        # Step 3: Update emotional trend used by recommender
        self.recommender.update_emotional_trend(
            emotional_state
        )

        # Step 4: Generate personalized recommendations
        result = self.recommender.personalize(
            emotional_state
        )

        # Step 5: Generate wellness trend summary
        trend_summary = self.trend_analyzer.generate_summary()

        # Add trend analysis to the pipeline result
        result["trend_summary"] = trend_summary

        return result


def print_pipeline_result(result):
    """Print a privacy-safe wellness analysis result."""

    print("\n" + "=" * 60)
    print("EMPLOYEE MESSAGE RECEIVED")
    print("=" * 60)

    print("\nEMOTIONAL ANALYSIS")
    print(f"Dominant emotion: {result['current_emotion']}")
    print(f"Detected emotions: {result['detected_emotions']}")
    print(f"Intensity: {result['emotional_intensity']}")
    print(
        f"Negative intensity: "
        f"{result['negative_emotion_intensity']}"
    )
    print(f"Polarity: {result['polarity']}")
    print(f"Severity: {result['severity']}")

    print("\nRECOMMENDATIONS")

    for recommendation in result["recommendations"]:
        print(
            f"- {recommendation['title']} "
            f"(score: {recommendation['score']})"
        )
        print(
            f"  Reasons: {recommendation.get('reasons', [])}"
        )

    print("\nWELLNESS TREND SUMMARY")
    print(
        f"Total records: "
        f"{result['trend_summary']['total_emotional_records']}"
    )
    print(
        f"Emotion frequency: "
        f"{result['trend_summary']['emotion_frequency']}"
    )
    print(
        f"Average intensity: "
        f"{result['trend_summary']['average_emotional_intensity']}"
    )
    print(
        f"Average negative intensity: "
        f"{result['trend_summary']['average_negative_emotion_intensity']}"
    )
    print(
        f"Polarity distribution: "
        f"{result['trend_summary']['polarity_distribution']}"
    )
    print(
        f"Severity distribution: "
        f"{result['trend_summary']['severity_distribution']}"
    )

def read_cli_input(file_path):
    """Read supported wellness feedback file types."""

    path = Path(file_path)

    if not path.exists():
        return None, "Input file could not be found."

    suffix = path.suffix.lower()

    readers = {
        ".txt": read_txt_file,
        ".csv": read_csv_file,
        ".pdf": read_pdf_file,
        ".docx": read_docx_file,
    }

    reader = readers.get(suffix)

    if reader is None:
        return (
            None,
            "Unsupported file type. "
            "Use TXT, CSV, PDF, or DOCX.",
        )

    return reader(str(path))

def main():

    parser = argparse.ArgumentParser(
        description="AI Employee Wellness Analysis"
    )

    input_group = parser.add_mutually_exclusive_group()

    input_group.add_argument(
        "--message",
        type=str,
        help="Analyze a single wellness message.",
    )

    input_group.add_argument(
        "--input",
        type=str,
        help="Analyze wellness feedback from a TXT, CSV, PDF, or DOCX file.",
    )

    args = parser.parse_args()

    pipeline = WellnessPipeline(
        user_preferences={
            "preferred_categories": [
                "breathing",
                "mindfulness",
                "short_break",
            ]
        }
    )

    if args.message:

        result = pipeline.process_message(
            args.message.strip()
        )

        print_pipeline_result(result)

    elif args.input:

        input_data, status = read_cli_input(args.input)

        if input_data is None:
            print(f"Error: {status}")
            raise SystemExit(1)

        if isinstance(input_data, list):

            for message in input_data:

                result = pipeline.process_message(
                    message
                )

                print_pipeline_result(result)

        else:

            result = pipeline.process_message(
                input_data
            )

            print_pipeline_result(result)

    else:

        test_messages = [
            "I am extremely worried about my deadlines.",
            "I am angry about the amount of work I have.",
            "I feel happy about the progress I made today.",
            "I feel sad because my work has been difficult lately.",
            "I am slightly worried about tomorrow's meeting.",
        ]

        for message in test_messages:

            result = pipeline.process_message(message)

            print_pipeline_result(result)

if __name__ == "__main__":
    main()
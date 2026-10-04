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


if __name__ == "__main__":

    pipeline = WellnessPipeline(
        user_preferences={
            "preferred_categories": [
                "breathing",
                "mindfulness",
                "short_break",
            ]
        }
    )

    test_messages = [
        "I am extremely worried about my deadlines.",
        "I am angry about the amount of work I have.",
        "I feel happy about the progress I made today.",
        "I feel sad because my work has been difficult lately.",
        "I am slightly worried about tomorrow's meeting.",
    ]

    for message in test_messages:

        result = pipeline.process_message(message)

        print("\n" + "=" * 60)
        print("EMPLOYEE MESSAGE")
        print("=" * 60)

        print(message)

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
from collections import Counter


class WellnessTrendAnalyzer:
    """
    Analyzes an employee's emotional history over time.

    The analyzer uses previously generated emotional states to calculate:
    - emotion frequency
    - average emotional intensity
    - average negative-emotion intensity
    - polarity distribution
    - severity distribution
    - recent emotional trend
    """

    def __init__(self, emotional_history=None):
        self.emotional_history = emotional_history or []

    def add_emotional_state(self, emotional_state):
        if not isinstance(emotional_state, dict):
            raise ValueError(
                "emotional_state must be a dictionary."
            )

        self.emotional_history.append(emotional_state)

    def get_emotion_frequency(self):
        emotion_counts = Counter()

        for state in self.emotional_history:
            emotion = state.get("dominant_emotion")

            if emotion:
                emotion_counts[emotion] += 1

        return dict(emotion_counts)

    def get_average_intensity(self):
        if not self.emotional_history:
            return 0.0

        intensities = [
            state.get("emotional_intensity", 0)
            for state in self.emotional_history
        ]

        return round(
            sum(intensities) / len(intensities),
            2,
        )

    def get_average_negative_intensity(self):
        if not self.emotional_history:
            return 0.0

        intensities = [
            state.get("negative_emotion_intensity", 0)
            for state in self.emotional_history
        ]

        return round(
            sum(intensities) / len(intensities),
            2,
        )

    def get_polarity_distribution(self):
        polarity_counts = Counter()

        for state in self.emotional_history:
            polarity = state.get("polarity")

            if polarity:
                polarity_counts[polarity] += 1

        return dict(polarity_counts)

    def get_severity_distribution(self):
        severity_counts = Counter()

        for state in self.emotional_history:
            severity = state.get("severity")

            if severity:
                severity_counts[severity] += 1

        return dict(severity_counts)

    def get_recent_trend(self, limit=5):
        recent_states = self.emotional_history[-limit:]

        return [
            {
                "emotion": state.get("dominant_emotion"),
                "intensity": state.get(
                    "emotional_intensity",
                    0,
                ),
                "negative_intensity": state.get(
                    "negative_emotion_intensity",
                    0,
                ),
                "polarity": state.get("polarity"),
                "severity": state.get("severity"),
            }
            for state in recent_states
        ]

    def generate_summary(self):
        return {
            "total_emotional_records": len(
                self.emotional_history
            ),
            "emotion_frequency": (
                self.get_emotion_frequency()
            ),
            "average_emotional_intensity": (
                self.get_average_intensity()
            ),
            "average_negative_emotion_intensity": (
                self.get_average_negative_intensity()
            ),
            "polarity_distribution": (
                self.get_polarity_distribution()
            ),
            "severity_distribution": (
                self.get_severity_distribution()
            ),
            "recent_trend": self.get_recent_trend(),
        }


if __name__ == "__main__":

    analyzer = WellnessTrendAnalyzer()

    sample_history = [
        {
            "dominant_emotion": "fear",
            "emotional_intensity": 100.0,
            "negative_emotion_intensity": 100.0,
            "polarity": "negative",
            "severity": "high",
        },
        {
            "dominant_emotion": "anger",
            "emotional_intensity": 91.95,
            "negative_emotion_intensity": 91.95,
            "polarity": "negative",
            "severity": "high",
        },
        {
            "dominant_emotion": "joy",
            "emotional_intensity": 95.98,
            "negative_emotion_intensity": 2.97,
            "polarity": "positive",
            "severity": "low",
        },
        {
            "dominant_emotion": "sadness",
            "emotional_intensity": 95.14,
            "negative_emotion_intensity": 95.14,
            "polarity": "negative",
            "severity": "high",
        },
        {
            "dominant_emotion": "fear",
            "emotional_intensity": 64.49,
            "negative_emotion_intensity": 64.49,
            "polarity": "negative",
            "severity": "moderate",
        },
    ]

    for state in sample_history:
        analyzer.add_emotional_state(state)

    summary = analyzer.generate_summary()

    print("\nWELLNESS TREND ANALYSIS")
    print("=" * 50)

    for key, value in summary.items():
        print(f"{key}: {value}")
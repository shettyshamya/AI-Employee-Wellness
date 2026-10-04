from collections import Counter
from datetime import datetime, timezone


class WellnessTrendAnalyzer:
    """
    Analyzes an employee's emotional history over time.

    Supports:
    - emotion frequency
    - average emotional intensity
    - average negative-emotion intensity
    - polarity distribution
    - severity distribution
    - recent emotional trend
    - daily trends
    - weekly trends
    - monthly trends
    """

    def __init__(self, emotional_history=None):
        self.emotional_history = emotional_history or []

    def add_emotional_state(self, emotional_state):
        if not isinstance(emotional_state, dict):
            raise ValueError(
                "emotional_state must be a dictionary."
            )

        # Ensure every record has a timestamp.
        if "timestamp" not in emotional_state:
            emotional_state["timestamp"] = datetime.now(
                timezone.utc
            ).isoformat()

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
            2
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
            2
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
                "timestamp": state.get("timestamp"),
                "emotion": state.get("dominant_emotion"),
                "intensity": state.get(
                    "emotional_intensity", 0
                ),
                "negative_intensity": state.get(
                    "negative_emotion_intensity", 0
                ),
                "polarity": state.get("polarity"),
                "severity": state.get("severity"),
            }
            for state in recent_states
        ]

    def get_time_series(self):
        """
        Return timestamped emotional records suitable
        for visualization.
        """

        records = []

        for state in self.emotional_history:
            timestamp = state.get("timestamp")

            if not timestamp:
                continue

            try:
                parsed_timestamp = datetime.fromisoformat(
                    timestamp.replace("Z", "+00:00")
                )
            except (ValueError, TypeError):
                continue

            records.append(
                {
                    "timestamp": parsed_timestamp,
                    "emotion": state.get(
                        "dominant_emotion"
                    ),
                    "intensity": state.get(
                        "emotional_intensity", 0
                    ),
                    "negative_intensity": state.get(
                        "negative_emotion_intensity", 0
                    ),
                    "polarity": state.get("polarity"),
                    "severity": state.get("severity"),
                }
            )

        records.sort(key=lambda item: item["timestamp"])

        return records

    def get_daily_trends(self):
        """
        Aggregate emotional records by calendar day.
        """

        records = self.get_time_series()
        daily = {}

        for record in records:
            day = record["timestamp"].date()

            if day not in daily:
                daily[day] = {
                    "intensity": [],
                    "negative_intensity": [],
                    "emotions": [],
                }

            daily[day]["intensity"].append(
                record["intensity"]
            )

            daily[day]["negative_intensity"].append(
                record["negative_intensity"]
            )

            if record["emotion"]:
                daily[day]["emotions"].append(
                    record["emotion"]
                )

        return self._build_aggregated_trends(daily)

    def get_weekly_trends(self):
        """
        Aggregate emotional records by ISO calendar week.
        """

        records = self.get_time_series()
        weekly = {}

        for record in records:
            iso = record["timestamp"].isocalendar()

            week_key = (
                iso.year,
                iso.week
            )

            if week_key not in weekly:
                weekly[week_key] = {
                    "intensity": [],
                    "negative_intensity": [],
                    "emotions": [],
                }

            weekly[week_key]["intensity"].append(
                record["intensity"]
            )

            weekly[week_key]["negative_intensity"].append(
                record["negative_intensity"]
            )

            if record["emotion"]:
                weekly[week_key]["emotions"].append(
                    record["emotion"]
                )

        return self._build_aggregated_trends(
            weekly,
            weekly=True
        )

    def get_monthly_trends(self):
        """
        Aggregate emotional records by calendar month.
        """

        records = self.get_time_series()
        monthly = {}

        for record in records:
            month_key = (
                record["timestamp"].year,
                record["timestamp"].month
            )

            if month_key not in monthly:
                monthly[month_key] = {
                    "intensity": [],
                    "negative_intensity": [],
                    "emotions": [],
                }

            monthly[month_key]["intensity"].append(
                record["intensity"]
            )

            monthly[month_key]["negative_intensity"].append(
                record["negative_intensity"]
            )

            if record["emotion"]:
                monthly[month_key]["emotions"].append(
                    record["emotion"]
                )

        return self._build_aggregated_trends(
            monthly,
            monthly=True
        )

    def _build_aggregated_trends(
        self,
        grouped_data,
        weekly=False,
        monthly=False
    ):
        """
        Convert grouped records into chart-friendly data.
        """

        trends = []

        for period, values in sorted(
            grouped_data.items()
        ):
            intensities = values["intensity"]
            negative_intensities = (
                values["negative_intensity"]
            )
            emotions = values["emotions"]

            if weekly:
                label = (
                    f"{period[0]}-W{period[1]:02d}"
                )
            elif monthly:
                label = (
                    f"{period[0]}-{period[1]:02d}"
                )
            else:
                label = str(period)

            dominant_emotion = None

            if emotions:
                dominant_emotion = Counter(
                    emotions
                ).most_common(1)[0][0]

            trends.append(
                {
                    "period": label,
                    "average_intensity": round(
                        sum(intensities)
                        / len(intensities),
                        2
                    ),
                    "average_negative_intensity": round(
                        sum(negative_intensities)
                        / len(negative_intensities),
                        2
                    ),
                    "dominant_emotion": dominant_emotion,
                    "record_count": len(intensities),
                }
            )

        return trends

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
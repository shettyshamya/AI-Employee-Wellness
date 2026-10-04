import json
from pathlib import Path
from datetime import datetime


FEEDBACK_FILE = Path("data/processed/recommendation_feedback.json")


class RecommendationFeedback:
    """
    Stores recommendation interactions and feedback.

    Captures:
    - recommendation viewed
    - recommendation accepted
    - recommendation rejected
    - user rating
    - user preference changes
    """

    def __init__(self, feedback_file=FEEDBACK_FILE):
        self.feedback_file = Path(feedback_file)
        self.feedback_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.feedback_history = self._load_feedback()

    def _load_feedback(self):
        if not self.feedback_file.exists():
            return []

        try:
            with open(
                self.feedback_file,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

        except (json.JSONDecodeError, OSError):
            pass

        return []

    def _save_feedback(self):
        with open(
            self.feedback_file,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.feedback_history,
                file,
                indent=2,
            )

    def record_feedback(
        self,
        recommendation_id,
        viewed=False,
        accepted=None,
        rating=None,
        preference_changes=None,
        recommendation_category=None,
    ):
        feedback = {
            "recommendation_id": recommendation_id,
            "recommendation_category": recommendation_category,
            "viewed": bool(viewed),
            "accepted": accepted,
            "rating": rating,
            "preference_changes": (
                preference_changes or {}
            ),
            "timestamp": datetime.now().isoformat(),
        }

        self.feedback_history.append(feedback)
        self._save_feedback()

        return feedback

    def get_recommendation_feedback(
        self,
        recommendation_id,
    ):
        return [
            item
            for item in self.feedback_history
            if item.get("recommendation_id")
            == recommendation_id
        ]

    def get_acceptance_rate(
        self,
        recommendation_id,
    ):
        feedback = self.get_recommendation_feedback(
            recommendation_id
        )

        decisions = [
            item["accepted"]
            for item in feedback
            if item.get("accepted") is not None
        ]

        if not decisions:
            return None

        accepted_count = sum(
            1 for decision in decisions
            if decision is True
        )

        return round(
            accepted_count / len(decisions),
            2,
        )

    def get_average_rating(
        self,
        recommendation_id,
    ):
        feedback = self.get_recommendation_feedback(
            recommendation_id
        )

        ratings = [
            item["rating"]
            for item in feedback
            if isinstance(item.get("rating"), (int, float))
        ]

        if not ratings:
            return 0.0

        return round(
            sum(ratings) / len(ratings),
            2,
        )

    def get_feedback_summary(self):
        summary = {}

        recommendation_ids = {
            item.get("recommendation_id")
            for item in self.feedback_history
            if item.get("recommendation_id")
        }

        for recommendation_id in recommendation_ids:
            summary[recommendation_id] = {
                "total_interactions": len(
                    self.get_recommendation_feedback(
                        recommendation_id
                    )
                ),
                "acceptance_rate": (
                    self.get_acceptance_rate(
                        recommendation_id
                    )
                ),
                "average_rating": (
                    self.get_average_rating(
                        recommendation_id
                    )
                ),
            }

        return summary


if __name__ == "__main__":

    feedback = RecommendationFeedback()

    feedback.record_feedback(
        recommendation_id="breathing_01",
        viewed=True,
        accepted=True,
        rating=5,
    )

    feedback.record_feedback(
        recommendation_id="mindfulness_01",
        viewed=True,
        accepted=False,
        rating=2,
    )

    print("\nRECOMMENDATION FEEDBACK TEST")
    print("=" * 50)

    print(
        "Feedback history:",
        feedback.feedback_history,
    )

    print(
        "\nFeedback summary:",
        feedback.get_feedback_summary(),
    )
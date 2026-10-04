from collections import Counter

try:
    from .recommendation_feedback import RecommendationFeedback
except ImportError:
    from recommendation_feedback import RecommendationFeedback
    
RECOMMENDATIONS = [
    {
        "id": "breathing_01",
        "title": "2-Minute Breathing Exercise",
        "category": "breathing",
        "target_emotions": {"fear", "anger", "sadness"},
        "intensity_range": (0, 100),
    },
    {
        "id": "mindfulness_01",
        "title": "Short Mindfulness Exercise",
        "category": "mindfulness",
        "target_emotions": {"fear", "sadness", "anger"},
        "intensity_range": (20, 100),
    },
    {
        "id": "short_break_01",
        "title": "Take a Short Break",
        "category": "short_break",
        "target_emotions": {"anger", "fear", "sadness"},
        "intensity_range": (40, 100),
    },
    {
        "id": "reflection_01",
        "title": "Write Down What Is Worrying You",
        "category": "reflection",
        "target_emotions": {"fear", "sadness"},
        "intensity_range": (20, 80),
    },
    {
        "id": "positive_activity_01",
        "title": "Do a Short Enjoyable Activity",
        "category": "positive_activity",
        "target_emotions": {"joy", "surprise"},
        "intensity_range": (0, 100),
    },
]


class PersonalizedRecommender:
    """
    Explainable personalized wellness recommendation model.

    Uses:
    - detected emotions
    - emotional intensity
    - user preferences
    - previous interactions
    - recommendation history
    - emotional trends
    """

    def __init__(
        self,
        user_preferences=None,
        previous_interactions=None,
        recommendation_history=None,
        emotional_trends=None,
    ):
        self.user_preferences = user_preferences or {}
        self.previous_interactions = previous_interactions or []
        self.recommendation_history = recommendation_history or []
        self.emotional_trends = emotional_trends or []
        self.feedback = RecommendationFeedback()

    def update_preferences(self, preferences):
        if not isinstance(preferences, dict):
            raise ValueError("Preferences must be a dictionary.")

        self.user_preferences.update(preferences)

    def add_interaction(self, interaction):
        self.previous_interactions.append(interaction)

    def add_recommendation_history(self, recommendation):
        self.recommendation_history.append(recommendation)

    def update_emotional_trend(self, emotional_state):
        self.emotional_trends.append(emotional_state)

    def get_recent_emotional_trend(self, limit=5):
        return self.emotional_trends[-limit:]

    def get_preferred_categories(self):
        return self.user_preferences.get(
            "preferred_categories",
            [],
        )

    def get_previous_recommendations(self):
        return set(self.recommendation_history)

    def analyze_user_profile(self):
        emotion_counts = Counter()

        for state in self.emotional_trends:
            emotion = state.get("dominant_emotion")

            if emotion:
                emotion_counts[emotion] += 1

        return {
            "preferred_categories": self.get_preferred_categories(),
            "previous_recommendations": list(
                self.get_previous_recommendations()
            ),
            "emotion_frequency": dict(emotion_counts),
            "interaction_count": len(self.previous_interactions),
            "emotional_history_count": len(self.emotional_trends),
        }

    def calculate_recommendation_score(
        self,
        recommendation,
        emotional_state,
    ):
        """
        Calculate an explainable recommendation score.

        Maximum score = 100.
        """

        score = 0
        reasons = []

        dominant_emotion = emotional_state.get(
            "dominant_emotion"
        )

        detected_emotions = set(
            emotional_state.get(
                "detected_emotions",
                [],
            )
        )

        intensity = emotional_state.get(
            "emotional_intensity",
            0,
        )

        preferred_categories = set(
            self.get_preferred_categories()
        )

        # Historical emotional pattern
        emotional_trend = getattr(
            self,
            "emotional_trends",
            [],
        )

        recent_emotions = [
            state.get("dominant_emotion")
            for state in emotional_trend[-5:]
            if state.get("dominant_emotion")
        ]

        historical_emotion_count = recent_emotions.count(
            dominant_emotion
        )

        if historical_emotion_count >= 2:
            score += 10
            reasons.append(
                "matches a repeated recent emotional pattern"
            )

        # 1. Emotion match: up to 40 points
        target_emotions = recommendation["target_emotions"]

        if dominant_emotion in target_emotions:
            score += 40
            reasons.append(
                "matches dominant emotion"
            )

        elif detected_emotions & target_emotions:
            score += 25
            reasons.append(
                "matches detected emotion"
            )

        # 2. User preference: up to 30 points
        if recommendation["category"] in preferred_categories:
            score += 30
            reasons.append(
                "matches user preference"
            )

        # 3. Intensity suitability: up to 20 points
        minimum, maximum = recommendation["intensity_range"]

        if minimum <= intensity <= maximum:
            score += 20
            reasons.append(
                "matches emotional intensity"
            )

        # 4. Recommendation history
        recommendation_count = self.recommendation_history.count(
            recommendation["id"]
        )

        if recommendation_count == 0:
            score += 10
            reasons.append(
                "not previously recommended"
            )

        elif recommendation_count == 1:
            score -= 10
            reasons.append(
                "recommended once before"
            )

        elif recommendation_count == 2:
            score -= 20
            reasons.append(
                "recommended twice before"
            )

        else:
            score -= 30
            reasons.append(
                "recommended multiple times"
            )

        # 5. Recommendation feedback
        recommendation_id = recommendation["id"]

        acceptance_rate = self.feedback.get_acceptance_rate(
            recommendation_id
        )

        average_rating = self.feedback.get_average_rating(
            recommendation_id
        )

        if acceptance_rate is not None:
            if acceptance_rate >= 0.75:
                score += 10
                reasons.append(
                    "has a high acceptance rate"
                )

            elif acceptance_rate <= 0.25:
                score -= 10
                reasons.append(
                    "has a low acceptance rate"
                )

        if average_rating >= 4:
            score += 10
            reasons.append(
                "has a high user rating"
            )

        elif (
            average_rating > 0
            and average_rating <= 2
        ):
            score -= 10
            reasons.append(
                "has a low user rating"
            )

        # Keep score within 0-100
        score = max(
            0,
            min(score, 100),
        )

        return score, reasons

    def generate_recommendations(
        self,
        emotional_state,
        top_n=3,
    ):
        """
        Rank wellness recommendations according to
        emotional state and user personalization.
        """

        if not isinstance(emotional_state, dict):
            raise ValueError(
                "emotional_state must be a dictionary."
            )

        scored_recommendations = []

        for recommendation in RECOMMENDATIONS:
            score, reasons = self.calculate_recommendation_score(
                recommendation,
                emotional_state,
            )

            scored_recommendations.append(
                {
                    "id": recommendation["id"],
                    "title": recommendation["title"],
                    "category": recommendation["category"],
                    "score": score,
                    "reasons": reasons,
                }
            )

        scored_recommendations.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        # Prefer different recommendation categories
        selected = []
        selected_categories = set()

        for recommendation in scored_recommendations:
            if recommendation["category"] not in selected_categories:
                selected.append(recommendation)

                selected_categories.add(
                    recommendation["category"]
                )

            if len(selected) >= top_n:
                break

        # Fill remaining slots if necessary
        if len(selected) < top_n:
            for recommendation in scored_recommendations:
                if recommendation not in selected:
                    selected.append(recommendation)

                if len(selected) >= top_n:
                    break

        return selected

    def personalize(self, emotional_state):
        if not isinstance(emotional_state, dict):
            raise ValueError(
                "emotional_state must be a dictionary."
            )

        profile = self.analyze_user_profile()

        recommendations = self.generate_recommendations(
            emotional_state
        )

        for recommendation in recommendations:
            self.add_recommendation_history(
                recommendation["id"]
            )

        return {
            "current_emotion": emotional_state.get(
                "dominant_emotion"
            ),
            "detected_emotions": emotional_state.get(
                "detected_emotions",
                [],
            ),
            "emotional_intensity": emotional_state.get(
                "emotional_intensity",
                0,
            ),
            "negative_emotion_intensity": emotional_state.get(
                "negative_emotion_intensity",
                0,
            ),
            "polarity": emotional_state.get(
                "polarity"
            ),
            "severity": emotional_state.get(
                "severity"
            ),
            "user_preferences": self.user_preferences,
            "profile_summary": profile,
            "recommendations": recommendations,
        }


if __name__ == "__main__":

    recommender = PersonalizedRecommender(
        user_preferences={
            "preferred_categories": [
                "breathing",
                "mindfulness",
                "short_break",
            ]
        }
    )

    example_emotional_state = {
        "dominant_emotion": "fear",
        "detected_emotions": ["fear"],
        "emotional_intensity": 64.58,
        "negative_emotion_intensity": 64.58,
        "polarity": "negative",
        "severity": "moderate",
    }

    result = recommender.personalize(
        example_emotional_state
    )

    print("\nPERSONALIZED RECOMMENDATION PROFILE")

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nRECOMMENDATIONS")

    for recommendation in result["recommendations"]:
        print(
            f"- {recommendation['title']} "
            f"(score: {recommendation['score']})"
        )

        print(
            f"  category: {recommendation['category']}"
        )

        print(
            f"  reasons: "
            f"{', '.join(recommendation['reasons'])}"
        )
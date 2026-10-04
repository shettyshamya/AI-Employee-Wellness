import time

import pytest

from src.personalized_recommender import (
    PersonalizedRecommender,
)
from src.emotion_analyzer import EmotionAnalyzer


@pytest.fixture(scope="module")
def emotion_analyzer():
    return EmotionAnalyzer()


def build_emotional_state(emotion="fear"):
    return {
        "text": (
            "I am feeling worried about my workload "
            "and upcoming deadlines."
        ),
        "dominant_emotion": emotion,
        "detected_emotions": [emotion],
        "emotion_confidence": {
            "joy": 0.05,
            "sadness": 0.25,
            "anger": 0.20,
            "fear": 0.85,
            "surprise": 0.05,
            "disgust": 0.10,
        },
        "emotional_intensity": 75,
        "negative_emotion_intensity": 80,
        "intensity_details": {
            "modifier": 1.0,
        },
        "polarity": "negative",
        "mixed_emotional_state": False,
        "severity": "high",
    }


def test_emotion_analysis_response_time(
    emotion_analyzer,
):
    text = (
        "I am worried about my workload, "
        "but I am trying to stay positive."
    )

    start = time.perf_counter()

    result = emotion_analyzer.analyze(text)

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    assert result is not None
    assert "dominant_emotion" in result
    assert elapsed_ms < 5000


def test_emotion_analysis_repeated_stress(
    emotion_analyzer,
):
    messages = [
        "I feel happy about my progress.",
        "I am worried about my workload.",
        "I feel exhausted after a long day.",
        "I am excited about the new project.",
        "I am frustrated by the deadlines.",
    ]

    start = time.perf_counter()

    results = [
        emotion_analyzer.analyze(message)
        for message in messages
    ]

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    assert len(results) == len(messages)

    for result in results:
        assert result is not None
        assert "dominant_emotion" in result
        assert "emotion_confidence" in result

    assert elapsed_ms < 15000


def test_emotion_analysis_long_input(
    emotion_analyzer,
):
    text = (
        "I am feeling worried and stressed about my "
        "workload and deadlines. "
    ) * 100

    result = emotion_analyzer.analyze(text)

    assert result is not None
    assert "dominant_emotion" in result
    assert "emotion_confidence" in result


def test_emotion_analysis_invalid_input(
    emotion_analyzer,
):
    with pytest.raises(ValueError):
        emotion_analyzer.analyze("")


def test_recommender_response_time():
    recommender = PersonalizedRecommender(
        user_preferences={
            "preferred_categories": [
                "breathing",
                "mindfulness",
            ]
        },
        emotional_trends=[],
    )

    emotional_state = build_emotional_state()

    start = time.perf_counter()

    recommendations = (
        recommender.generate_recommendations(
            emotional_state,
            top_n=3,
        )
    )

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    assert recommendations
    assert len(recommendations) <= 3
    assert elapsed_ms < 1000


def test_recommender_repeated_stress():
    recommender = PersonalizedRecommender(
        user_preferences={
            "preferred_categories": [
                "breathing",
                "mindfulness",
                "short_break",
            ]
        },
        emotional_trends=[],
    )

    states = [
        build_emotional_state("fear"),
        build_emotional_state("sadness"),
        build_emotional_state("anger"),
        build_emotional_state("joy"),
    ]

    start = time.perf_counter()

    results = []

    for state in states:
        results.append(
            recommender.generate_recommendations(
                state,
                top_n=3,
            )
        )

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    assert len(results) == len(states)

    for recommendations in results:
        assert recommendations
        assert len(recommendations) <= 3

    assert elapsed_ms < 5000


def test_recommender_large_feedback_history():
    recommender = PersonalizedRecommender(
        user_preferences={
            "preferred_categories": [
                "breathing",
                "mindfulness",
            ]
        },
        emotional_trends=[],
    )

    recommender.feedback.feedback_history = [
        {
            "recommendation_id": (
                f"recommendation_{index % 5}"
            ),
            "recommendation_category": (
                "mindfulness"
            ),
            "viewed": True,
            "accepted": index % 2 == 0,
            "rating": (index % 5) + 1,
            "timestamp": (
                "2026-10-04T12:00:00+00:00"
            ),
        }
        for index in range(1000)
    ]

    emotional_state = build_emotional_state()

    start = time.perf_counter()

    recommendations = (
        recommender.generate_recommendations(
            emotional_state,
            top_n=3,
        )
    )

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    assert recommendations
    assert len(recommendations) <= 3
    assert elapsed_ms < 5000
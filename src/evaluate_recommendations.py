import json
import math
import time
from pathlib import Path

from src.personalized_recommender import PersonalizedRecommender, RECOMMENDATIONS
from src.recommendation_feedback import RecommendationFeedback


BASE_DIR = Path(__file__).resolve().parent.parent
TEST_CASES_PATH = (
    BASE_DIR / "data" / "processed" / "recommendation_test_cases.json"
)
REPORTS_DIR = BASE_DIR / "reports"

TOP_K = 3


def precision_at_k(recommended_ids, relevant_ids, k):
    top = recommended_ids[:k]

    if not top:
        return 0.0

    hits = sum(item in relevant_ids for item in top)

    return hits / len(top)


def recall_at_k(recommended_ids, relevant_ids, k):
    if not relevant_ids:
        return 0.0

    top = recommended_ids[:k]
    hits = sum(item in relevant_ids for item in top)

    return hits / len(relevant_ids)


def f1_at_k(precision, recall):
    if precision + recall == 0:
        return 0.0

    return 2 * precision * recall / (precision + recall)


def ndcg_at_k(recommended_ids, relevant_ids, k):
    top = recommended_ids[:k]

    dcg = 0.0

    for rank, recommendation_id in enumerate(top, start=1):
        if recommendation_id in relevant_ids:
            dcg += 1.0 / math.log2(rank + 1)

    ideal_hits = min(len(relevant_ids), k)

    if ideal_hits == 0:
        return 0.0

    ideal_dcg = sum(
        1.0 / math.log2(rank + 1)
        for rank in range(1, ideal_hits + 1)
    )

    return dcg / ideal_dcg


def diversity_at_k(recommendations, k):
    top = recommendations[:k]

    if not top:
        return 0.0

    categories = {
        recommendation["category"]
        for recommendation in top
    }

    return len(categories) / len(top)


def acceptance_rate(feedback_history):
    decisions = [
        item.get("accepted")
        for item in feedback_history
        if item.get("accepted") is not None
    ]

    if not decisions:
        return None

    accepted = sum(
        1
        for decision in decisions
        if decision is True
    )

    return accepted / len(decisions)


def average_rating(feedback_history):
    ratings = [
        item.get("rating")
        for item in feedback_history
        if isinstance(item.get("rating"), (int, float))
    ]

    if not ratings:
        return 0.0

    return sum(ratings) / len(ratings)


def baseline_recommendations(emotional_state, top_n=TOP_K):
    """
    Simple baseline:

    1. Prefer recommendations whose target emotions
       match the dominant emotion.
    2. Preserve the original recommendation order.
    3. Fill remaining slots with the original list.
    """

    dominant_emotion = emotional_state.get("dominant_emotion")

    matching = [
        recommendation
        for recommendation in RECOMMENDATIONS
        if dominant_emotion in recommendation["target_emotions"]
    ]

    remaining = [
        recommendation
        for recommendation in RECOMMENDATIONS
        if recommendation not in matching
    ]

    ordered = matching + remaining

    return ordered[:top_n]


def build_emotional_trends(history):
    return [
        {
            "dominant_emotion": emotion,
            "detected_emotions": [emotion],
            "emotional_intensity": 50,
            "negative_emotion_intensity": 50,
            "polarity": "negative",
            "severity": "moderate",
        }
        for emotion in history
    ]


def create_advanced_recommender(case):
    recommender = PersonalizedRecommender(
        user_preferences={
            "preferred_categories": case.get(
                "preferred_categories",
                []
            )
        },
        emotional_trends=build_emotional_trends(
            case.get("historical_emotions", [])
        ),
    )

    # Use an isolated feedback store so real application feedback
    # cannot contaminate the controlled benchmark.
    isolated_feedback = RecommendationFeedback()
    isolated_feedback.feedback_history = []

    # Load only controlled feedback defined by this benchmark case.
    for feedback in case.get("feedback_history", []):
        isolated_feedback.feedback_history.append(
            feedback
        )

    recommender.feedback = isolated_feedback

    return recommender


def evaluate_feedback(case):
    feedback_history = case.get(
        "feedback_history",
        []
    )

    return {
        "interaction_count": len(feedback_history),
        "acceptance_rate": acceptance_rate(
            feedback_history
        ),
        "average_rating": average_rating(
            feedback_history
        ),
    }


def evaluate_case(case):
    emotional_state = case["emotional_state"]

    relevant_ids = set(
        case["expected_relevant"]
    )

    # -------------------------
    # Baseline
    # -------------------------

    baseline_start = time.perf_counter()

    baseline = baseline_recommendations(
        emotional_state,
        TOP_K,
    )

    baseline_time_ms = (
        time.perf_counter() - baseline_start
    ) * 1000

    baseline_ids = [
        recommendation["id"]
        for recommendation in baseline
    ]

    baseline_precision = precision_at_k(
        baseline_ids,
        relevant_ids,
        TOP_K,
    )

    baseline_recall = recall_at_k(
        baseline_ids,
        relevant_ids,
        TOP_K,
    )

    baseline_f1 = f1_at_k(
        baseline_precision,
        baseline_recall,
    )

    baseline_ndcg = ndcg_at_k(
        baseline_ids,
        relevant_ids,
        TOP_K,
    )

    baseline_diversity = diversity_at_k(
        baseline,
        TOP_K,
    )

    # -------------------------
    # Advanced recommender
    # -------------------------

    recommender = create_advanced_recommender(
        case
    )

    advanced_start = time.perf_counter()

    advanced = recommender.generate_recommendations(
        emotional_state,
        top_n=TOP_K,
    )

    advanced_time_ms = (
        time.perf_counter() - advanced_start
    ) * 1000

    advanced_ids = [
        recommendation["id"]
        for recommendation in advanced
    ]

    advanced_precision = precision_at_k(
        advanced_ids,
        relevant_ids,
        TOP_K,
    )

    advanced_recall = recall_at_k(
        advanced_ids,
        relevant_ids,
        TOP_K,
    )

    advanced_f1 = f1_at_k(
        advanced_precision,
        advanced_recall,
    )

    advanced_ndcg = ndcg_at_k(
        advanced_ids,
        relevant_ids,
        TOP_K,
    )

    advanced_diversity = diversity_at_k(
        advanced,
        TOP_K,
    )

    feedback_summary = evaluate_feedback(case)

    return {
        "case_id": case["case_id"],
        "description": case["description"],
        "expected_relevant": list(relevant_ids),

        "feedback": feedback_summary,

        "baseline": {
            "recommendations": baseline_ids,
            "precision_at_k": baseline_precision,
            "recall_at_k": baseline_recall,
            "f1_at_k": baseline_f1,
            "ndcg_at_k": baseline_ndcg,
            "diversity_at_k": baseline_diversity,
            "response_time_ms": baseline_time_ms,
        },

        "advanced": {
            "recommendations": advanced_ids,
            "scores": [
                recommendation["score"]
                for recommendation in advanced
            ],
            "reasons": [
                recommendation["reasons"]
                for recommendation in advanced
            ],
            "precision_at_k": advanced_precision,
            "recall_at_k": advanced_recall,
            "f1_at_k": advanced_f1,
            "ndcg_at_k": advanced_ndcg,
            "diversity_at_k": advanced_diversity,
            "response_time_ms": advanced_time_ms,
        },
    }


def average(results, system, metric):
    values = [
        result[system][metric]
        for result in results
    ]

    if not values:
        return 0.0

    return sum(values) / len(values)


def run_evaluation():
    with open(
        TEST_CASES_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        test_cases = json.load(file)

    results = [
        evaluate_case(case)
        for case in test_cases
    ]

    feedback_cases = [
        result
        for result in results
        if result["feedback"]["interaction_count"] > 0
    ]

    feedback_acceptance_rates = [
        result["feedback"]["acceptance_rate"]
        for result in feedback_cases
        if result["feedback"]["acceptance_rate"]
        is not None
    ]

    feedback_average_ratings = [
        result["feedback"]["average_rating"]
        for result in feedback_cases
        if result["feedback"]["average_rating"] > 0
    ]

    summary = {
        "baseline": {
            "precision_at_k": average(
                results,
                "baseline",
                "precision_at_k",
            ),
            "recall_at_k": average(
                results,
                "baseline",
                "recall_at_k",
            ),
            "f1_at_k": average(
                results,
                "baseline",
                "f1_at_k",
            ),
            "ndcg_at_k": average(
                results,
                "baseline",
                "ndcg_at_k",
            ),
            "diversity_at_k": average(
                results,
                "baseline",
                "diversity_at_k",
            ),
            "response_time_ms": average(
                results,
                "baseline",
                "response_time_ms",
            ),
        },

        "advanced": {
            "precision_at_k": average(
                results,
                "advanced",
                "precision_at_k",
            ),
            "recall_at_k": average(
                results,
                "advanced",
                "recall_at_k",
            ),
            "f1_at_k": average(
                results,
                "advanced",
                "f1_at_k",
            ),
            "ndcg_at_k": average(
                results,
                "advanced",
                "ndcg_at_k",
            ),
            "diversity_at_k": average(
                results,
                "advanced",
                "diversity_at_k",
            ),
            "response_time_ms": average(
                results,
                "advanced",
                "response_time_ms",
            ),
        },

        "feedback": {
            "cases_with_feedback": len(
                feedback_cases
            ),
            "average_acceptance_rate": (
                sum(feedback_acceptance_rates)
                / len(feedback_acceptance_rates)
                if feedback_acceptance_rates
                else None
            ),
            "average_rating": (
                sum(feedback_average_ratings)
                / len(feedback_average_ratings)
                if feedback_average_ratings
                else 0.0
            ),
        },
    }

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = {
        "evaluation_type": (
            "controlled expert-defined "
            "recommendation benchmark"
        ),
        "note": (
            "expected_relevant lists are controlled "
            "benchmark labels, not observed employee "
            "acceptance data"
        ),
        "feedback_note": (
            "feedback_history is controlled benchmark "
            "input used to verify feedback-aware ranking"
        ),
        "summary": summary,
        "cases": results,
    }

    json_path = (
        REPORTS_DIR
        / "recommendation_evaluation.json"
    )

    with open(
        json_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            output,
            file,
            indent=2,
        )

    markdown_path = (
        REPORTS_DIR
        / "TASK9_RECOMMENDATION_EVALUATION.md"
    )

    lines = [
        "# Task 9 — Recommendation Evaluation",
        "",
        "## Evaluation setup",
        "",
        f"- Controlled test cases: {len(results)}",
        f"- Evaluation cutoff: Precision@{TOP_K}, Recall@{TOP_K}, F1@{TOP_K}",
        "- Ranking metric: NDCG@K",
        "- Diversity metric: unique recommendation categories / K",
        "- Response time: measured with `time.perf_counter()`",
        "- Acceptance rate: calculated from controlled feedback history",
        "- Baseline: dominant-emotion matching with fixed recommendation order",
        "- Advanced: personalized scoring using emotion, preferences, intensity, history, and feedback",
        "",
        "The `expected_relevant` values are controlled benchmark labels created for testing. They are not real employee acceptance measurements.",
        "",
        "Controlled feedback is used only to verify that the advanced ranking responds to prior recommendation interactions.",
        "",
        "## Results",
        "",
        "| Metric | Baseline | Advanced |",
        "|---|---:|---:|",
        f"| Precision@{TOP_K} | {summary['baseline']['precision_at_k']:.3f} | {summary['advanced']['precision_at_k']:.3f} |",
        f"| Recall@{TOP_K} | {summary['baseline']['recall_at_k']:.3f} | {summary['advanced']['recall_at_k']:.3f} |",
        f"| F1@{TOP_K} | {summary['baseline']['f1_at_k']:.3f} | {summary['advanced']['f1_at_k']:.3f} |",
        f"| NDCG@{TOP_K} | {summary['baseline']['ndcg_at_k']:.3f} | {summary['advanced']['ndcg_at_k']:.3f} |",
        f"| Diversity@{TOP_K} | {summary['baseline']['diversity_at_k']:.3f} | {summary['advanced']['diversity_at_k']:.3f} |",
        f"| Response time (ms) | {summary['baseline']['response_time_ms']:.3f} | {summary['advanced']['response_time_ms']:.3f} |",
        "",
        "## Feedback results",
        "",
        f"- Cases with controlled feedback: {summary['feedback']['cases_with_feedback']}",
    ]

    if summary["feedback"]["average_acceptance_rate"] is None:
        lines.append(
            "- Average acceptance rate: no acceptance data"
        )
    else:
        lines.append(
            f"- Average acceptance rate: "
            f"{summary['feedback']['average_acceptance_rate']:.3f}"
        )

    lines.extend(
        [
            f"- Average user rating: "
            f"{summary['feedback']['average_rating']:.3f}",
            "",
            "## Per-case results",
            "",
        ]
    )

    for result in results:
        lines.extend(
            [
                f"### {result['case_id']} — {result['description']}",
                "",
                f"- Expected relevant: {', '.join(result['expected_relevant'])}",
                f"- Controlled feedback interactions: {result['feedback']['interaction_count']}",
                f"- Controlled acceptance rate: {result['feedback']['acceptance_rate']}",
                f"- Controlled average rating: {result['feedback']['average_rating']:.3f}",
                f"- Baseline recommendations: {', '.join(result['baseline']['recommendations'])}",
                f"- Advanced recommendations: {', '.join(result['advanced']['recommendations'])}",
                f"- Baseline Precision@{TOP_K}: {result['baseline']['precision_at_k']:.3f}",
                f"- Advanced Precision@{TOP_K}: {result['advanced']['precision_at_k']:.3f}",
                f"- Baseline Recall@{TOP_K}: {result['baseline']['recall_at_k']:.3f}",
                f"- Advanced Recall@{TOP_K}: {result['advanced']['recall_at_k']:.3f}",
                f"- Baseline F1@{TOP_K}: {result['baseline']['f1_at_k']:.3f}",
                f"- Advanced F1@{TOP_K}: {result['advanced']['f1_at_k']:.3f}",
                f"- Baseline NDCG@{TOP_K}: {result['baseline']['ndcg_at_k']:.3f}",
                f"- Advanced NDCG@{TOP_K}: {result['advanced']['ndcg_at_k']:.3f}",
                f"- Baseline diversity: {result['baseline']['diversity_at_k']:.3f}",
                f"- Advanced diversity: {result['advanced']['diversity_at_k']:.3f}",
                "",
            ]
        )

    with open(
        markdown_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write("\n".join(lines))

    print("Recommendation evaluation completed.")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {markdown_path}")
    print()
    print("Average results:")

    print(
        f"Baseline Precision@{TOP_K}: "
        f"{summary['baseline']['precision_at_k']:.3f}"
    )

    print(
        f"Advanced Precision@{TOP_K}: "
        f"{summary['advanced']['precision_at_k']:.3f}"
    )

    print(
        f"Baseline Recall@{TOP_K}: "
        f"{summary['baseline']['recall_at_k']:.3f}"
    )

    print(
        f"Advanced Recall@{TOP_K}: "
        f"{summary['advanced']['recall_at_k']:.3f}"
    )

    print(
        f"Baseline F1@{TOP_K}: "
        f"{summary['baseline']['f1_at_k']:.3f}"
    )

    print(
        f"Advanced F1@{TOP_K}: "
        f"{summary['advanced']['f1_at_k']:.3f}"
    )

    print(
        f"Baseline NDCG@{TOP_K}: "
        f"{summary['baseline']['ndcg_at_k']:.3f}"
    )

    print(
        f"Advanced NDCG@{TOP_K}: "
        f"{summary['advanced']['ndcg_at_k']:.3f}"
    )

    print(
        f"Baseline diversity: "
        f"{summary['baseline']['diversity_at_k']:.3f}"
    )

    print(
        f"Advanced diversity: "
        f"{summary['advanced']['diversity_at_k']:.3f}"
    )

    print(
        f"Baseline response time: "
        f"{summary['baseline']['response_time_ms']:.3f} ms"
    )

    print(
        f"Advanced response time: "
        f"{summary['advanced']['response_time_ms']:.3f} ms"
    )

    if summary["feedback"]["average_acceptance_rate"] is None:
        print("Average acceptance rate: no acceptance data")
    else:
        print(
            "Average acceptance rate: "
            f"{summary['feedback']['average_acceptance_rate']:.3f}"
        )

    print(
        "Average user rating: "
        f"{summary['feedback']['average_rating']:.3f}"
    )


if __name__ == "__main__":
    run_evaluation()
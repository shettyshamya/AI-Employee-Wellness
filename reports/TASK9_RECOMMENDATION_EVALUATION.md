# Task 9 — Recommendation Evaluation

## Evaluation setup

- Controlled test cases: 5
- Evaluation cutoff: Precision@3, Recall@3, F1@3
- Ranking metric: NDCG@K
- Diversity metric: unique recommendation categories / K
- Response time: measured with `time.perf_counter()`
- Acceptance rate: calculated from controlled feedback history
- Baseline: dominant-emotion matching with fixed recommendation order
- Advanced: personalized scoring using emotion, preferences, intensity, history, and feedback

The `expected_relevant` values are controlled benchmark labels created for testing. They are not real employee acceptance measurements.

Controlled feedback is used only to verify that the advanced ranking responds to prior recommendation interactions.

## Results

| Metric | Baseline | Advanced |
|---|---:|---:|
| Precision@3 | 0.733 | 0.733 |
| Recall@3 | 0.867 | 0.867 |
| F1@3 | 0.767 | 0.767 |
| NDCG@3 | 0.894 | 0.906 |
| Diversity@3 | 1.000 | 1.000 |
| Response time (ms) | 0.004 | 0.023 |

## Feedback results

- Cases with controlled feedback: 1
- Average acceptance rate: 0.500
- Average user rating: 3.500

## Per-case results

### case_01 — High fear intensity

- Expected relevant: short_break_01, breathing_01, mindfulness_01
- Controlled feedback interactions: 2
- Controlled acceptance rate: 0.5
- Controlled average rating: 3.500
- Baseline recommendations: breathing_01, mindfulness_01, short_break_01
- Advanced recommendations: breathing_01, mindfulness_01, short_break_01
- Baseline Precision@3: 1.000
- Advanced Precision@3: 1.000
- Baseline Recall@3: 1.000
- Advanced Recall@3: 1.000
- Baseline F1@3: 1.000
- Advanced F1@3: 1.000
- Baseline NDCG@3: 1.000
- Advanced NDCG@3: 1.000
- Baseline diversity: 1.000
- Advanced diversity: 1.000

### case_02 — High anger intensity

- Expected relevant: short_break_01, breathing_01, mindfulness_01
- Controlled feedback interactions: 0
- Controlled acceptance rate: None
- Controlled average rating: 0.000
- Baseline recommendations: breathing_01, mindfulness_01, short_break_01
- Advanced recommendations: breathing_01, short_break_01, mindfulness_01
- Baseline Precision@3: 1.000
- Advanced Precision@3: 1.000
- Baseline Recall@3: 1.000
- Advanced Recall@3: 1.000
- Baseline F1@3: 1.000
- Advanced F1@3: 1.000
- Baseline NDCG@3: 1.000
- Advanced NDCG@3: 1.000
- Baseline diversity: 1.000
- Advanced diversity: 1.000

### case_03 — High sadness intensity

- Expected relevant: breathing_01, reflection_01, mindfulness_01
- Controlled feedback interactions: 0
- Controlled acceptance rate: None
- Controlled average rating: 0.000
- Baseline recommendations: breathing_01, mindfulness_01, short_break_01
- Advanced recommendations: breathing_01, mindfulness_01, short_break_01
- Baseline Precision@3: 0.667
- Advanced Precision@3: 0.667
- Baseline Recall@3: 0.667
- Advanced Recall@3: 0.667
- Baseline F1@3: 0.667
- Advanced F1@3: 0.667
- Baseline NDCG@3: 0.765
- Advanced NDCG@3: 0.765
- Baseline diversity: 1.000
- Advanced diversity: 1.000

### case_04 — Positive joy state

- Expected relevant: positive_activity_01
- Controlled feedback interactions: 0
- Controlled acceptance rate: None
- Controlled average rating: 0.000
- Baseline recommendations: positive_activity_01, breathing_01, mindfulness_01
- Advanced recommendations: positive_activity_01, breathing_01, mindfulness_01
- Baseline Precision@3: 0.333
- Advanced Precision@3: 0.333
- Baseline Recall@3: 1.000
- Advanced Recall@3: 1.000
- Baseline F1@3: 0.500
- Advanced F1@3: 0.500
- Baseline NDCG@3: 1.000
- Advanced NDCG@3: 1.000
- Baseline diversity: 1.000
- Advanced diversity: 1.000

### case_05 — Repeated fear pattern

- Expected relevant: short_break_01, breathing_01, reflection_01
- Controlled feedback interactions: 0
- Controlled acceptance rate: None
- Controlled average rating: 0.000
- Baseline recommendations: breathing_01, mindfulness_01, short_break_01
- Advanced recommendations: breathing_01, reflection_01, mindfulness_01
- Baseline Precision@3: 0.667
- Advanced Precision@3: 0.667
- Baseline Recall@3: 0.667
- Advanced Recall@3: 0.667
- Baseline F1@3: 0.667
- Advanced F1@3: 0.667
- Baseline NDCG@3: 0.704
- Advanced NDCG@3: 0.765
- Baseline diversity: 1.000
- Advanced diversity: 1.000

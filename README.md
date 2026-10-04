# AI-Based Employee Wellness Management Platform

## 📌 Project Overview

The **AI-Based Employee Wellness Management Platform** is an AI/ML-based system designed to analyze employee feedback, identify sentiment and emotional patterns, track wellness trends, and generate personalized wellness recommendations.

The platform processes employee inputs from multiple sources such as:

* 💬 Text/chat input
* 📄 TXT files
* 📊 CSV files
* 📕 PDF files
* 📝 DOCX files

The system combines NLP preprocessing, VADER sentiment analysis, transformer-based emotion analysis, emotional trend tracking, personalized recommendation ranking, recommendation feedback learning, and explainable recommendations.

The project is developed incrementally from a reliable baseline sentiment pipeline toward a complete personalized employee wellness workflow.

---

# 🎯 Project Objectives

* Collect employee feedback from multiple input formats.
* Validate and clean incoming text data.
* Perform NLP preprocessing.
* Analyze sentiment using VADER.
* Detect employee emotions using ML/transformer-based models.
* Calculate emotional intensity and severity.
* Track emotional states over time.
* Detect repeated emotional patterns.
* Generate personalized wellness recommendations.
* Use user preferences and historical behavior in recommendation ranking.
* Learn from recommendation feedback.
* Provide understandable explanations for recommendations.
* Evaluate recommendation quality using controlled test cases.
* Integrate the complete ML workflow into the existing wellness pipeline.
* Maintain compatibility with the existing API and data-processing workflow.

---

# 🏗️ Complete System Architecture

```text
                         EMPLOYEE INPUT
                              │
             ┌────────────────┼────────────────┐
             ↓                ↓                ↓
           Chat             Files            CSV
                              │
                    ┌─────────┴─────────┐
                    ↓                   ↓
                   TXT               PDF / DOCX
                    │                   │
                    └─────────┬─────────┘
                              ↓
                       TEXT INGESTION
                              ↓
                      INPUT VALIDATION
                              ↓
                       PREPROCESSING
                              ↓
                    SENTIMENT ANALYSIS
                              ↓
                  BERT / DistilBERT
                              ↓
                EMOTION + CONFIDENCE
                              ↓
                  EMOTION INTENSITY
                              ↓
                 EMOTIONAL HISTORY
                              ↓
                 TREND & PATTERN ANALYSIS
                              ↓
              PERSONALIZED RECOMMENDATION
                              ↓
                 HYBRID RANKING MODEL
                              ↓
              FEEDBACK + USER PREFERENCES
                              ↓
                EXPLAINABLE RECOMMENDATION
                              ↓
                 WELLNESS RECOMMENDATION
                              ↓
                    EXISTING API / DB
                              ↓
                       REPORTING
```

---

# 📂 Project Structure

```text
AI-Employee-Wellness/
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── recommendation_feedback.json
│       └── recommendation_test_cases.json
│
├── src/
│   ├── emotion_analyzer.py
│   ├── evaluate_distilbert.py
│   ├── evaluate_recommendations.py
│   ├── ingestion.py
│   ├── personalized_recommender.py
│   ├── prepare_go_emotions.py
│   ├── preprocessing.py
│   ├── recommendation_feedback.py
│   ├── report.py
│   ├── sentiment.py
│   ├── train_emotion_models.py
│   ├── wellness_pipeline.py
│   └── wellness_trend_analyzer.py
│
├── models/
├── reports/
│   ├── TASK9_RECOMMENDATION_EVALUATION.md
│   └── recommendation_evaluation.json
│
├── notebooks/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🚀 Milestone 1 — Text Ingestion & Baseline Sentiment

## Task 1 — Text Ingestion Validation

The ingestion module was tested with multiple input formats:

| Input Type                    | Status    |
| ----------------------------- | --------- |
| Direct text input             | ✅         |
| TXT file                      | ✅         |
| CSV file                      | ✅         |
| PDF file                      | ✅         |
| DOCX file                     | ✅         |
| Empty input                   | ✅ Handled |
| Whitespace-only input         | ✅ Handled |
| Empty TXT file                | ✅ Handled |
| Empty CSV file                | ✅ Handled |
| Missing CSV column            | ✅ Handled |
| Unsupported file type         | ✅ Handled |
| Emojis and special characters | ✅         |

---

## Task 2 — Text Preprocessing Validation

The preprocessing module performs:

* Tokenization
* Stop-word removal
* Lemmatization
* Noise filtering
* Punctuation handling
* Special-character handling
* Emoji preservation
* Repeated-space handling
* Empty-input handling
* Negation preservation

Example:

```text
Original:
I am feeling very stressed because of my workload!!!

Processed:
feeling stressed workload
```

Negation is preserved:

```text
Original:
I am not happy with my workload.

Processed:
not happy workload
```

---

## Task 3 — VADER Sentiment Validation

VADER was selected as the baseline sentiment-analysis method.

The system generates:

* Positive score
* Negative score
* Neutral score
* Compound score
* Sentiment classification

The scores are generated dynamically and are not hardcoded.

---

## Task 4 — Initial Sentiment Report

The system generates a sentiment report containing:

* Employee ID
* Original employee feedback
* Processed text
* Sentiment classification
* Positive score
* Negative score
* Neutral score
* Compound score

Example:

```text
reports/milestone1_sentiment_report.csv
```

---

## Task 5 — Complete Pipeline Integration

The complete baseline pipeline was tested:

```text
Input
  ↓
Ingestion
  ↓
Preprocessing
  ↓
VADER
  ↓
Sentiment Result
  ↓
Report
```

Integration testing confirmed that input, processed, and sentiment record counts remain consistent.

---

# 🧠 Milestone 2 — Emotion Analysis & Personalized Wellness

## Task 6 — Emotional Trend & User State Tracking

The platform now maintains historical emotional information and uses it to identify changes in employee emotional state.

Implemented capabilities include:

* Emotion frequency tracking
* Emotional intensity over time
* Dominant emotion detection
* Positive/negative trend tracking
* Repeated emotional pattern detection
* Recent emotional state
* Emotional history
* Personalized recommendations based on previous patterns

The trend analyzer produces information such as:

```text
Total records: 5

Emotion frequency:
{
    "fear": 2,
    "anger": 1,
    "joy": 1,
    "sadness": 1
}

Average intensity: 89.51
Average negative intensity: 70.91

Polarity distribution:
{
    "negative": 4,
    "positive": 1
}

Severity distribution:
{
    "high": 3,
    "low": 1,
    "moderate": 1
}
```

### Historical Pattern Influence

Repeated emotions can influence future recommendations.

For example, if fear appears repeatedly in recent employee feedback, recommendations can receive an additional reason such as:

```text
matches a repeated recent emotional pattern
```

This verifies that recommendations are not based only on the current message.

---

# 🤖 Task 7 — Recommendation Feedback Learning

A feedback mechanism was implemented to capture recommendation interactions.

The system supports:

* Recommendation viewed
* Recommendation accepted
* Recommendation rejected
* User rating
* User preference changes
* Recommendation interaction history

Feedback is stored in:

```text
data/processed/recommendation_feedback.json
```

Example:

```json
{
    "recommendation_id": "breathing_01",
    "viewed": true,
    "accepted": true,
    "rating": 5,
    "preference_changes": {},
    "timestamp": "2026-01-01T10:00:00"
}
```

The feedback system calculates:

* Acceptance rate
* Average user rating
* Total interactions

Example:

```text
breathing_01
Acceptance rate: 1.0
Average rating: 5.0

mindfulness_01
Acceptance rate: 0.0
Average rating: 2.0
```

These feedback statistics are incorporated into recommendation scoring.

A recommendation with strong historical acceptance and rating can receive a higher ranking score, while recommendations with poor feedback can receive a lower score.

---

# 💡 Task 8 — Recommendation Explainability

Every personalized recommendation includes dynamically generated reasons explaining why it was selected.

Examples include:

```text
matches dominant emotion
matches user preference
matches emotional intensity
matches a repeated recent emotional pattern
not previously recommended
recommended once before
recommended multiple times
has a high acceptance rate
has a high user rating
has a low acceptance rate
has a low user rating
```

Example recommendation:

```text
2-Minute Breathing Exercise

Score: 100

Reasons:
- matches dominant emotion
- matches user preference
- matches emotional intensity
- not previously recommended
- has a high acceptance rate
- has a high user rating
```

This provides transparency into the recommendation ranking rather than returning unexplained recommendations.

---

# 📊 Task 9 — Advanced Recommendation Evaluation

The recommendation system was evaluated using a controlled test dataset containing five emotional scenarios:

```text
case_01 — High fear intensity
case_02 — High anger intensity
case_03 — High sadness intensity
case_04 — Positive joy state
case_05 — Repeated fear pattern
```

Test cases are stored in:

```text
data/processed/recommendation_test_cases.json
```

The evaluation compares:

```text
Baseline Recommendation
        VS
Advanced Personalized Recommendation
```

The baseline uses dominant-emotion matching and fixed recommendation ordering.

The advanced system uses:

* Emotion
* Emotional intensity
* User preferences
* Recommendation history
* Emotional history
* Repeated patterns
* Feedback signals
* Acceptance rate
* User ratings
* Dynamic scoring

---

## Evaluation Metrics

The system evaluates:

* Precision@3
* Recall@3
* F1-score@3
* NDCG@3
* Recommendation diversity
* Response time
* Acceptance rate
* Average user rating

---

## Latest Evaluation Results

```text
Baseline Precision@3: 0.733
Advanced Precision@3: 0.733

Baseline Recall@3: 0.867
Advanced Recall@3: 0.867

Baseline F1@3: 0.767
Advanced F1@3: 0.767

Baseline NDCG@3: 0.894
Advanced NDCG@3: 0.906

Baseline diversity: 1.000
Advanced diversity: 1.000

Baseline response time: approximately 0.003 ms
Advanced response time: approximately 0.026 ms

Average acceptance rate: 0.500
Average user rating: 3.500
```

### Interpretation

The advanced recommender currently matches the baseline on Precision, Recall, and F1.

However, the advanced system improves ranking quality:

```text
NDCG:
Baseline = 0.894
Advanced = 0.906
```

The improvement demonstrates that personalization and historical signals can improve recommendation ordering even when the top-3 relevance counts remain unchanged.

The evaluation also confirms that feedback information is being incorporated successfully:

```text
Average acceptance rate = 0.500
Average user rating     = 3.500
```

Generated reports:

```text
reports/TASK9_RECOMMENDATION_EVALUATION.md
reports/recommendation_evaluation.json
```

---

# 🔄 Task 10 — Complete ML Integration & Project Cleanup

The complete wellness workflow has been integrated and tested.

## Complete Flow

```text
Text Input
    ↓
Preprocessing
    ↓
Sentiment Analysis
    ↓
BERT / DistilBERT Emotion Analysis
    ↓
Emotion + Confidence
    ↓
Emotion Intensity
    ↓
User Emotional History
    ↓
Trend Detection
    ↓
Feedback History
    ↓
Personalized Recommendation Model
    ↓
Recommendation Ranking
    ↓
Explainable Wellness Recommendation
```

The integrated pipeline is implemented in:

```text
src/wellness_pipeline.py
```

Supporting modules include:

```text
src/emotion_analyzer.py
src/personalized_recommender.py
src/recommendation_feedback.py
src/wellness_trend_analyzer.py
```

---

## Task 10 Verification

The following areas were tested during integration:

| Requirement                     | Status |
| ------------------------------- | ------ |
| Existing ingestion pipeline     | ✅      |
| Existing preprocessing pipeline | ✅      |
| Existing sentiment analysis     | ✅      |
| Dynamic emotion predictions     | ✅      |
| Emotional intensity             | ✅      |
| Emotional history               | ✅      |
| Trend analysis                  | ✅      |
| Personalized recommendations    | ✅      |
| Dynamic recommendation ranking  | ✅      |
| Historical pattern influence    | ✅      |
| Recommendation explanations     | ✅      |
| Feedback storage                | ✅      |
| Acceptance-rate learning        | ✅      |
| User-rating learning            | ✅      |
| Recommendation evaluation       | ✅      |
| Python module compilation       | ✅      |
| End-to-end wellness pipeline    | ✅      |

Python source compilation was verified using:

```bash
python -m compileall src
```

The compilation completed successfully.

---

# 🧪 Recommendation System Example

Example employee message:

```text
I am extremely worried about my deadlines.
```

Emotional analysis:

```text
Dominant emotion: fear
Intensity: 100.0
Negative intensity: 100.0
Polarity: negative
Severity: high
```

Personalized recommendations:

```text
1. 2-Minute Breathing Exercise
   Score: 100

   Reasons:
   - matches dominant emotion
   - matches user preference
   - matches emotional intensity
   - not previously recommended
   - has a high acceptance rate
   - has a high user rating

2. Take a Short Break
   Score: 100

   Reasons:
   - matches dominant emotion
   - matches user preference
   - matches emotional intensity
   - not previously recommended

3. Short Mindfulness Exercise
   Score: 80

   Reasons:
   - matches dominant emotion
   - matches user preference
   - matches emotional intensity
   - not previously recommended
   - has a low acceptance rate
   - has a low user rating
```

A later repeated fear state can additionally produce:

```text
matches a repeated recent emotional pattern
```

and may change the recommendation ranking.

---

# ▶️ Running the System

## Install Dependencies

```bash
py -m pip install -r requirements.txt
```

---

## Run Baseline Tests

```bash
py test_ingestion.py
py test_preprocessing.py
py test_sentiment.py
py test_report.py
py test_pipeline.py
py test_real_dataset.py
```

---

## Run Emotion Analysis

```bash
python -m src.emotion_analyzer
```

---

## Run Personalized Recommendations

Use module execution from the project root:

```bash
python -m src.personalized_recommender
```

---

## Run Recommendation Feedback

```bash
python src/recommendation_feedback.py
```

---

## Run Wellness Trend Analysis

```bash
python -m src.wellness_trend_analyzer
```

---

## Run Complete Wellness Pipeline

From the project root:

```bash
python -m src.wellness_pipeline
```

Using `python -m` is recommended because the project uses the `src` package structure.

---

## Run Recommendation Evaluation

```bash
python -m src.evaluate_recommendations
```

Generated files:

```text
reports/recommendation_evaluation.json
reports/TASK9_RECOMMENDATION_EVALUATION.md
```

---

## Compile All Source Files

```bash
python -m compileall src
```

---

# 🛠️ Technologies Used

* **Python**
* **Pandas**
* **NLTK**
* **VADER Sentiment**
* **PyMuPDF**
* **python-docx**
* **Scikit-learn**
* **PyTorch**
* **Hugging Face Transformers**
* **DistilBERT / BERT**
* **GoEmotions**
* **Git & GitHub**

---

# 📋 Project Status

| Task    | Description                           | Status     |
| ------- | ------------------------------------- | ---------- |
| Task 1  | Text ingestion validation             | ✅ Complete |
| Task 2  | Text preprocessing                    | ✅ Complete |
| Task 3  | VADER sentiment validation            | ✅ Complete |
| Task 4  | Sentiment reporting                   | ✅ Complete |
| Task 5  | Pipeline integration                  | ✅ Complete |
| Task 6  | Emotional trend & user state tracking | ✅ Complete |
| Task 7  | Recommendation feedback learning      | ✅ Complete |
| Task 8  | Recommendation explainability         | ✅ Complete |
| Task 9  | Advanced recommendation evaluation    | ✅ Complete |
| Task 10 | ML integration & cleanup              | ✅ Complete |

## **Tasks 1–10: COMPLETED ✅**

---

# 📁 Important Generated Files

### Recommendation feedback

```text
data/processed/recommendation_feedback.json
```

### Recommendation test cases

```text
data/processed/recommendation_test_cases.json
```

### Task 9 evaluation

```text
reports/TASK9_RECOMMENDATION_EVALUATION.md
reports/recommendation_evaluation.json
```

---

# 🔮 Future Development

Potential future improvements include:

* Larger real-world recommendation datasets
* More extensive user feedback collection
* A/B testing of recommendation strategies
* More advanced semantic content matching
* Personalized wellness dashboards
* API endpoints for recommendation feedback
* Database-backed employee wellness history
* Model fine-tuning on domain-specific wellness data
* More comprehensive recommendation diversity metrics
* Automated regression testing
* Production monitoring and model performance tracking

---

# ⚠️ Data Privacy

Employee feedback can contain sensitive information. Any deployment using real employee data should implement appropriate:

* Privacy controls
* Access control
* Data anonymization
* Encryption
* Secure storage
* Authentication
* Authorization
* Data-retention policies

The repository should not contain confidential employee information, credentials, API keys, passwords, or other private data.

Generated feedback and evaluation data should also be reviewed before committing to a public repository.

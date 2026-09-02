# AI-Based Employee Wellness Management Platform

## 📌 Project Overview

The **AI-Based Employee Wellness Management Platform** is an AI/ML-based system designed to analyze employee feedback and identify sentiment and emotional patterns from textual data.

The platform is intended to process employee inputs from multiple sources such as:

* 💬 Text/chat input
* 📄 TXT files
* 📊 CSV files
* 📕 PDF files
* 📝 DOCX files

The system processes the collected text, performs NLP preprocessing, and applies baseline sentiment analysis to identify whether employee feedback is **Positive, Negative, or Neutral**.

The project is being developed incrementally, with the first milestone focusing on reliable text ingestion, preprocessing, baseline sentiment analysis, reporting, and pipeline integration.

---

# 🎯 Project Objectives

* Collect employee feedback from multiple input formats.
* Validate and clean incoming text data.
* Perform NLP preprocessing.
* Analyze employee feedback using sentiment analysis.
* Generate sentiment scores and classifications.
* Create reports that can be used for employee wellness analysis.
* Build a foundation for future emotion classification and personalized wellness recommendations.

---

# 🏗️ Current System Architecture

```text
                EMPLOYEE FEEDBACK
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
      Chat            Files        CSV Data
                       │
              ┌────────┴────────┐
              ↓                 ↓
             TXT           PDF / DOCX
              │                 │
              └────────┬────────┘
                       ↓
                TEXT INGESTION
                       ↓
                INPUT VALIDATION
                       ↓
                 PREPROCESSING
                       ↓
              VADER SENTIMENT
                       ↓
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       Positive      Neutral      Negative
          │            │            │
          └────────────┼────────────┘
                       ↓
                SENTIMENT REPORT
```

---

# 📂 Project Structure

```text
AI-Employee-Wellness/
│
├── data/
│   └── raw/
│       └── Dataset and sample input files
│
├── src/
│   ├── ingestion.py
│   ├── preprocessing.py
│   ├── sentiment.py
│   └── report.py
│
├── models/
│
├── reports/
│
├── notebooks/
│
├── app.py
│
├── test_ingestion.py
├── test_preprocessing.py
├── test_sentiment.py
├── test_report.py
├── test_pipeline.py
├── test_real_dataset.py
│
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

### Example

**Original:**

```text
I am feeling very stressed because of my workload!!!
```

**Processed:**

```text
feeling stressed workload
```

Another example:

**Original:**

```text
I am not happy with my workload.
```

**Processed:**

```text
not happy workload
```

The preprocessing pipeline was also tested using long employee feedback, short text, repeated spaces, emojis, and special characters.

---

# 📊 Task 3 — VADER Sentiment Validation

VADER was selected as the baseline sentiment analysis method.

The system generates:

* Positive score
* Negative score
* Neutral score
* Compound score
* Sentiment classification

### Example Results

| Input                                                              | Sentiment | Compound Score |
| ------------------------------------------------------------------ | --------- | -------------: |
| I really enjoy my work and feel happy with my team 😊              | Positive  |         0.9216 |
| I am feeling very stressed because of my workload 😔               | Negative  |        -0.2247 |
| I attended the employee meeting today.                             | Neutral   |         0.0000 |
| I am extremely excited and happy about the new project! 🎉         | Positive  |         0.9253 |
| I am extremely frustrated, exhausted and unhappy with my workload. | Negative  |        -0.8508 |

The scores are generated dynamically by VADER and are not hardcoded.

---

# 📈 Task 4 — Initial Sentiment Report

The system generates a sentiment report containing:

* Employee ID
* Original employee feedback
* Processed text
* Sentiment classification
* Positive score
* Negative score
* Neutral score
* Compound score

The report is generated as a CSV file.

Example output:

```text
reports/milestone1_sentiment_report.csv
```

---

# 🧪 Task 5 — Complete Pipeline Integration

The complete pipeline was tested to verify that information moves correctly between every module.

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

The integration test successfully confirmed that:

```text
Input records       = 5
Processed records   = 5
Sentiment records   = 5
```

Result:

```text
PASS: All modules processed the same number of records.
```

---

# 🗃️ Real Dataset Validation

After validating the system using sample employee feedback, the complete pipeline was tested using a **10,000-record workplace stress dataset**.

### Dataset columns

```text
Employee_ID
Message
Word_Count
Sentiment_Score
Employee_Role
Department
Stress_Level
```

For Milestone 1, the `Message` column was used as the actual employee text input.

The existing `Sentiment_Score` and `Stress_Level` fields were not used to generate the VADER sentiment results.

---

## Real Dataset Results

```text
Total records:       10,000
Empty messages:           0
Valid text records:  10,000
Processed records:  10,000
Sentiment records:  10,000
```

### VADER Sentiment Distribution

| Sentiment |    Records | Percentage |
| --------- | ---------: | ---------: |
| Positive  |      5,451 |     54.51% |
| Neutral   |      3,270 |     32.70% |
| Negative  |      1,279 |     12.79% |
| **Total** | **10,000** |   **100%** |

The complete real-dataset pipeline completed successfully.

```text
PASS: Complete real-dataset pipeline executed successfully.
```

Generated report:

```text
reports/milestone1_real_dataset_report.csv
```

---

# 🛠️ Technologies Used

* **Python**
* **Pandas**
* **NLTK**
* **VADER Sentiment**
* **PyMuPDF**
* **python-docx**
* **Scikit-learn** *(planned for future ML components)*
* **Git & GitHub**

---

# 📦 Installation

Clone the repository:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd AI-Employee-Wellness
```

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

---

# ▶️ Running the Tests

### Test text ingestion

```bash
py test_ingestion.py
```

### Test preprocessing

```bash
py test_preprocessing.py
```

### Test VADER sentiment

```bash
py test_sentiment.py
```

### Test report generation

```bash
py test_report.py
```

### Test complete pipeline

```bash
py test_pipeline.py
```

### Test real dataset

```bash
py test_real_dataset.py
```

---

# 📋 Milestone 1 Status

| Component                   | Status     |
| --------------------------- | ---------- |
| Multi-format text ingestion | ✅ Complete |
| Input validation            | ✅ Complete |
| Text preprocessing          | ✅ Complete |
| VADER baseline              | ✅ Complete |
| Sentiment report            | ✅ Complete |
| Pipeline integration        | ✅ Complete |
| Real dataset validation     | ✅ Complete |

### **Milestone 1: COMPLETED ✅**

---

# 🔮 Future Development

The current milestone establishes the baseline sentiment-analysis pipeline.

Future development will extend the platform toward:

* ML-based emotion classification
* Employee emotion detection
* Stress and wellness pattern analysis
* Personalized wellness recommendations
* Employee wellness dashboards
* Trend analysis over time
* Model evaluation and improvement
* Integration of additional employee feedback sources

---

# ⚠️ Data Privacy

Employee feedback can contain sensitive information. Any deployment using real employee data should implement appropriate privacy, access-control, anonymization, and data-protection measures.

The repository should not contain confidential employee information, credentials, API keys, or other private data.

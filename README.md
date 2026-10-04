# AI-Based Employee Wellness Management Platform

## Project Overview

The **AI-Based Employee Wellness Management Platform** is an AI/ML-based system designed to analyze employee feedback, identify sentiment and emotional patterns, track wellness trends, and generate personalized wellness recommendations.

The platform supports:

- Direct text/chat input
- TXT files
- CSV files
- PDF files
- DOCX files

The system combines:

- Text preprocessing
- VADER sentiment analysis
- DistilBERT emotion analysis
- Emotional intensity analysis
- Emotional trend analysis
- Personalized recommendation ranking
- Recommendation feedback learning
- Recommendation explainability
- Streamlit dashboard
- Report generation and export
- Automated testing
- CLI execution
- Privacy-safe reporting

---

# System Architecture

```text
                         EMPLOYEE INPUT
                              |
             +----------------+----------------+
             |                |                |
            Chat             Files             CSV
                              |
                    +---------+---------+
                    |                   |
                   TXT              PDF / DOCX
                    |                   |
                    +---------+---------+
                              |
                       TEXT INGESTION
                              |
                       INPUT VALIDATION
                              |
                       PREPROCESSING
                              |
                    SENTIMENT ANALYSIS
                              |
                         DistilBERT
                              |
                    EMOTION + CONFIDENCE
                              |
                    EMOTION INTENSITY
                              |
                 EMOTIONAL HISTORY
                              |
                 TREND & PATTERN ANALYSIS
                              |
              PERSONALIZED RECOMMENDATION
                              |
                 HYBRID RANKING MODEL
                              |
              FEEDBACK + USER PREFERENCES
                              |
                EXPLAINABLE RECOMMENDATION
                              |
                 WELLNESS RECOMMENDATION
                              |
                         REPORTING
                              |
                    STREAMLIT DASHBOARD
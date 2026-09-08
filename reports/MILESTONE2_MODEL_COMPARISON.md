\# Milestone 2: Emotion Classification Model Comparison



\## Objective



The objective of Milestone 2 was to train and evaluate transformer-based

emotion classification models for detecting employee emotions from text.



\## Dataset



The GoEmotions dataset was used for training and evaluation.



The dataset was converted into six emotion labels:



\- Joy

\- Sadness

\- Anger

\- Fear

\- Surprise

\- Disgust



The processed dataset contained:



\- Training samples: 6,624

\- Validation samples: 804

\- Test samples: 833



\## Models



Two transformer-based models were trained:



1\. DistilBERT

2\. BERT



Both models were trained for one epoch and evaluated on the same test set.



\## Results



| Metric | DistilBERT | BERT |

|---|---:|---:|

| Exact-match accuracy | 76.47% | 78.99% |

| Precision | 85.59% | 85.65% |

| Recall | 76.04% | 79.16% |

| Macro-F1 | 80.24% | 82.12% |



\## Analysis



BERT achieved better performance than DistilBERT on the test dataset.



The improvements were:



\- Accuracy: +2.52 percentage points

\- Precision: +0.06 percentage points

\- Recall: +3.12 percentage points

\- Macro-F1: +1.88 percentage points



The Macro-F1 score was selected as the primary comparison metric because

the task involves multiple emotion labels and class imbalance.



\## Selected Model



BERT was selected as the final emotion classification model because it

achieved the highest test Macro-F1 score of 82.12%.



\## Conclusion



Milestone 2 successfully completed the preparation, training, evaluation,

and comparison of transformer-based emotion classification models.



The trained BERT model will be used as the preferred model for the next

stage of the AI Employee Wellness platform.



from pathlib import Path

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)


EMOTIONS = [
    "joy",
    "sadness",
    "anger",
    "fear",
    "surprise",
    "disgust",
]

POSITIVE_EMOTIONS = {"joy"}
NEGATIVE_EMOTIONS = {
    "sadness",
    "anger",
    "fear",
    "disgust",
}

MODEL_DIR = Path("models/bert")
THRESHOLD = 0.2

# Simple text cues for the intensity heuristic
INTENSIFIERS = {
    "very", "really", "extremely", "incredibly",
    "so", "deeply", "overwhelmingly", "terribly",
}

MITIGATORS = {
    "slightly", "somewhat", "mildly", "a little",
    "a bit", "kind of", "sort of",
}


class EmotionAnalyzer:
    def __init__(self, model_dir=MODEL_DIR):
        self.model_dir = Path(model_dir)

        if not self.model_dir.exists():
            raise FileNotFoundError(
                f"Model folder not found: {self.model_dir}"
            )

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_dir
        )

        self.model = (
            AutoModelForSequenceClassification.from_pretrained(
                self.model_dir
            )
        )

        self.model.eval()

    def calculate_intensity(self, text, emotion_scores):
        """
        Dynamic, explainable intensity heuristic.

        Starts with the strongest emotion probability,
        then adjusts it using simple intensity words.

        This is NOT a validated psychological measure.
        """
        base_intensity = max(emotion_scores.values())

        words = set(text.lower().split())

        has_intensifier = bool(words & INTENSIFIERS)

        has_mitigator = any(
            phrase in text.lower()
            for phrase in MITIGATORS
        )

        modifier = 1.0

        if has_intensifier:
            modifier *= 1.2

        if has_mitigator:
            modifier *= 0.75

        intensity = base_intensity * modifier * 100

        # Keep the score between 0 and 100
        intensity = max(0.0, min(100.0, intensity))

        return round(intensity, 2), {
            "base_probability": round(
                float(base_intensity), 4
            ),
            "intensifier_detected": has_intensifier,
            "mitigator_detected": has_mitigator,
            "modifier": round(modifier, 2),
        }

    def analyze(self, text):
        if not isinstance(text, str) or not text.strip():
            raise ValueError(
                "Please provide non-empty text."
            )

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128,
        )

        with torch.no_grad():
            outputs = self.model(**inputs)

        probabilities = torch.sigmoid(
            outputs.logits
        )[0].cpu().tolist()

        emotion_scores = {
            emotion: float(probability)
            for emotion, probability in zip(
                EMOTIONS, probabilities
            )
        }

        # 1. Dominant emotion
        dominant_emotion = max(
            emotion_scores,
            key=emotion_scores.get,
        )

        # 2. Multiple detected emotions
        detected_emotions = [
            emotion
            for emotion, score in emotion_scores.items()
            if score >= THRESHOLD
        ]

        if not detected_emotions:
            detected_emotions = [dominant_emotion]

        # 3. Separate positive and negative signals
        positive_score = max(
            emotion_scores[e]
            for e in POSITIVE_EMOTIONS
        )

        negative_score = max(
            emotion_scores[e]
            for e in NEGATIVE_EMOTIONS
        )

        # 4. Polarity
        has_positive = positive_score >= THRESHOLD
        has_negative = negative_score >= THRESHOLD

        if has_positive and has_negative:
            polarity = "mixed"
        elif has_positive:
            polarity = "positive"
        elif has_negative:
            polarity = "negative"
        else:
            polarity = "uncertain"

        # 5. Mixed emotional state
        mixed_emotional_state = (
            has_positive and has_negative
        )

        # 6. Dynamic emotional intensity
        emotional_intensity, intensity_details = (
            self.calculate_intensity(
                text, emotion_scores
            )
        )
        7# Calculate modifier-adjusted negative emotion intensity
        modifier = intensity_details["modifier"]

        negative_intensity = round(
            min(negative_score * modifier, 1.0) * 100,
            2
        )

        if negative_intensity >= 80:    
            severity = "high"
        elif negative_intensity >= 50:
            severity = "moderate"
        else:
            severity = "low"

        return {
    "text": text,
    "dominant_emotion": dominant_emotion,
    "detected_emotions": detected_emotions,
    "emotion_confidence": {
        emotion: round(score, 4)
        for emotion, score in emotion_scores.items()
    },
    "emotional_intensity": emotional_intensity,
    "negative_emotion_intensity": negative_intensity,
    "intensity_details": intensity_details,
    "polarity": polarity,
    "mixed_emotional_state": mixed_emotional_state,
    "severity": severity,
}


if __name__ == "__main__":
    analyzer = EmotionAnalyzer()

    test_messages = [
        "I feel happy and excited about my progress.",
        "I am worried and angry about my workload.",
        "I feel sad, but I am also excited about my future.",
        "I am extremely worried about my deadlines.",
        "I am slightly worried about my deadlines.",
    ]

    for text in test_messages:
        result = analyzer.analyze(text)

        print("\n" + "=" * 50)
        print("EMOTIONAL STATE ANALYSIS")

        for key, value in result.items():
            print(f"{key}: {value}")
from .enums import ConfidenceText
from typing import Dict
import unicodedata


class ContentModerator:
    """
    Handles text moderation by validating, preprocessing,
    classifying, and converting confidence to human-readable form.
    """

    def __init__(self, classifier):
        self.classifier = classifier

    def predict_text(self, text: str) -> Dict:
        """
        Main method to classify text
        Returns a dictionary with label score, and confidence_text.
        """

        text = self._preprocess_text(text)
        result = self.classifier(text)[0]

        if (
            not isinstance(result, dict)
            or "label" not in result
            or "score" not in result
        ):
            raise ValueError("Malformed model output")

        label, score = result["label"], result["score"]

        return {
            "label": label,
            "score": score,
            "confidence_text": self._convert_score_to_text(score),
        }

    def _preprocess_text(self, text: str) -> str:
        """Sanitizes text to be model-ready."""

        text = unicodedata.normalize("NFKC", text)
        text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")

        return "".join(text.split())

    def _convert_score_to_text(self, score) -> str:
        if score > 0.85:
            return ConfidenceText.HIGHLY_CONFIDENT.value
        if score > 0.55:
            return ConfidenceText.MODERATELY_CONFIDENT.value
        return ConfidenceText.NOT_CONFIDENT.value

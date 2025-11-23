from typing import Dict
import unicodedata


class ContentModerator:
    """
    Handles text moderation by validating, preprocessing, and classifying
    """

    def __init__(self, classifier):
        self.classifier = classifier

    def predict_text(self, text: str) -> Dict:
        """
        Main method to classify text.
        Returns a dictionary with label and confidence score.
        """

        text = self._preprocess_text(text)
        result = self.classifier(text)[0]

        if (
            not isinstance(result, dict)
            or "label" not in result
            or "score" not in result
        ):
            raise ValueError("Malformed model output")

        label, score = result["label"].lower(), result["score"]

        return {
            "label": label,
            "score": score,
        }

    def _preprocess_text(self, text: str) -> str:
        """Sanitizes text to be model-ready."""

        text = unicodedata.normalize("NFKC", text)
        text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")

        return "".join(text.split())

import unicodedata


class ContentModerator:
    def __init__(self, classifier):
        self.classifier = classifier

    def predict_text(self, text: str) -> dict:
        text = self._preprocess_text(text)
        result = self.classifier(text)[0]

        return {
            "label": result["label"],
            "score": result["score"],
        }

    def _preprocess_text(self, text: str) -> str:
        text = unicodedata.normalize("NFKC", text)
        text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")
        return " ".join(text.split())

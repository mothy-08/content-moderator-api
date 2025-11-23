from enum import Enum


class ConfidenceText(Enum):
    """Enum representing confidence score in text"""

    HIGHLY_CONFIDENT = "high"
    MODERATELY_CONFIDENT = "moderate"
    NOT_CONFIDENT = "not"

from functools import lru_cache
from transformers import pipeline


@lru_cache(maxsize=1)
def get_classifier():
    """
    Lazy-loads the Hugging Face text-classification pipeline.
    Ensures a single instance is used across the service.
    """
    return pipeline("text-classification", "mothy-08/drbftcm")

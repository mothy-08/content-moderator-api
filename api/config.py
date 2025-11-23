from functools import lru_cache
from transformers import pipeline


@lru_cache(maxsize=1)
def get_classifier():
    return pipeline("text-classification", "mothy-08/drbftcm")

"""Türkçe E-Posta Yanlış Pozitif Spam Riski Azaltma Sistemi."""

from .pipeline import FalsePositiveReducer
from .spam_detector import SpamDetector
from .softener import Softener
from .preprocessing import clean_text
from .postprocess import postprocess

__version__ = "1.0.0"
__all__ = [
    "FalsePositiveReducer",
    "SpamDetector",
    "Softener",
    "clean_text",
    "postprocess",
]

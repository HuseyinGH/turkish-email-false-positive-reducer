"""
Spam tespit modülü.

TF-IDF + kalibre edilmiş Linear SVM ile bir e-postanın spam olma
olasılığını hesaplar. Makale Bölüm 3.4'te açıklanmıştır.

Modeller Hugging Face Hub üzerinden indirilir:
  - turkish-spam-svm/spam_svm.joblib
  - turkish-spam-svm/tfidf_vectorizer.joblib
"""

import joblib

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    hf_hub_download = None

from .preprocessing import clean_text


class SpamDetector:
    """TF-IDF + Linear SVM tabanlı spam tespit modülü."""

    def __init__(self, hf_repo: str = "HuseyinGH/turkish-spam-svm"):
        """
        Args:
            hf_repo: Hugging Face model deposu kimliği.
        """
        if hf_hub_download is None:
            raise ImportError("huggingface_hub gerekli: pip install huggingface_hub")

        svm_path = hf_hub_download(hf_repo, "spam_svm.joblib")
        vec_path = hf_hub_download(hf_repo, "tfidf_vectorizer.joblib")

        self.model = joblib.load(svm_path)
        self.vectorizer = joblib.load(vec_path)

    def predict(self, text: str) -> dict:
        """
        Bir metnin spam olasılığını döndürür.

        Args:
            text: Değerlendirilecek e-posta metni.

        Returns:
            {"spam_prob": float, "label": "spam"|"normal"}
        """
        cleaned = clean_text(text)
        features = self.vectorizer.transform([cleaned])
        prob = float(self.model.predict_proba(features)[0, 1])
        return {
            "spam_prob": prob,
            "label": "spam" if prob > 0.5 else "normal",
        }


if __name__ == "__main__":
    detector = SpamDetector()
    test = "TEBRİKLER! 1.000.000 TL KAZANDINIZ! Hemen tıklayın!"
    print(detector.predict(test))

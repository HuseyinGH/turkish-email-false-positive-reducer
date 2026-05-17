"""
Bütünleşik pipeline.

Üç aşamayı (tespit -> eşik tabanlı yönlendirme -> yumuşatma + yeniden
değerlendirme) tek bir arayüzde birleştirir. Makale Bölüm 3.3'te
açıklanan mimariyi uygular.
"""

from .spam_detector import SpamDetector
from .softener import Softener
from .postprocess import postprocess


class FalsePositiveReducer:
    """Türkçe e-postalarda yanlış pozitif spam riskini azaltan hibrit sistem."""

    def __init__(
        self,
        spam_repo: str = "HuseyinGH/turkish-spam-svm",
        softener_repo: str = "HuseyinGH/mt5-tr-softener",
        threshold: float = 0.5,
    ):
        """
        Args:
            spam_repo: Spam classifier HF deposu.
            softener_repo: Yumuşatma modeli HF deposu.
            threshold: Yumuşatma için spam olasılığı eşiği (varsayılan 0.5).
        """
        self.detector = SpamDetector(spam_repo)
        self.softener = Softener(softener_repo)
        self.threshold = threshold

    def process(self, text: str) -> dict:
        """
        Bir e-postayı üç aşamalı pipeline'dan geçirir.

        Args:
            text: Girdi e-posta metni.

        Returns:
            {
              "original": str,
              "spam_before": float,
              "softened": str | None,
              "spam_after": float | None,
              "action": "passed" | "softened",
              "issues": list[str],
            }
        """
        # --- Aşama 1: Tespit ---
        before = self.detector.predict(text)
        spam_before = before["spam_prob"]

        # --- Aşama 2: Eşik tabanlı yönlendirme ---
        if spam_before < self.threshold:
            return {
                "original": text,
                "spam_before": spam_before,
                "softened": None,
                "spam_after": None,
                "action": "passed",
                "issues": [],
            }

        # --- Aşama 3: Yumuşatma + son işleme + yeniden değerlendirme ---
        raw_output = self.softener.soften(text)
        post = postprocess(text, raw_output)
        softened = post["text"]

        after = self.detector.predict(softened)
        spam_after = after["spam_prob"]

        return {
            "original": text,
            "spam_before": spam_before,
            "softened": softened,
            "spam_after": spam_after,
            "action": "softened",
            "issues": post["issues"],
        }


if __name__ == "__main__":
    reducer = FalsePositiveReducer()

    ornekler = [
        "KARGONUZ TESLİM EDİLEMEDİ! HEMEN turkcell.com.tr ADRESİNE GİRİN!!!",
        "Merhaba, toplantı notlarını ekte paylaşıyorum. İyi çalışmalar.",
    ]
    for e in ornekler:
        sonuc = reducer.process(e)
        print(f"\nGirdi: {e}")
        print(f"  Aksiyon: {sonuc['action']}")
        print(f"  Önce spam: {sonuc['spam_before']:.3f}")
        if sonuc["action"] == "softened":
            print(f"  Yumuşatılmış: {sonuc['softened']}")
            print(f"  Sonra spam: {sonuc['spam_after']:.3f}")

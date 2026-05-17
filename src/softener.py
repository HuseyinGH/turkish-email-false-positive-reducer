"""
Yumuşatma modülü.

Türkçe özetleme görevinde önceden eğitilmiş, ardından yumuşatma görevine
adapte edilmiş mT5-small modeli ile agresif tonlu metni kurumsal/profesyonel
bir dile dönüştürür. Makale Bölüm 3.5'te açıklanmıştır.
"""

import torch
from transformers import MT5Tokenizer, MT5ForConditionalGeneration


class Softener:
    """mT5-small tabanlı metin yumuşatma modülü."""

    TASK_PREFIX = "yumusat: "

    def __init__(self, hf_repo: str = "HuseyinGH/mt5-tr-softener"):
        """
        Args:
            hf_repo: Hugging Face model deposu kimliği.
        """
        self.tokenizer = MT5Tokenizer.from_pretrained(hf_repo)
        self.model = MT5ForConditionalGeneration.from_pretrained(hf_repo)
        self.model.eval()

    def soften(self, text: str, max_len: int = 256) -> str:
        """
        Verilen metni kurumsal tona dönüştürür.

        Args:
            text: Yumuşatılacak e-posta metni.
            max_len: Maksimum jeton uzunluğu.

        Returns:
            Yumuşatılmış metin.
        """
        input_text = self.TASK_PREFIX + text
        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            max_length=max_len,
            truncation=True,
        )
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_len,
                num_beams=4,
                no_repeat_ngram_size=3,
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


if __name__ == "__main__":
    softener = Softener()
    test = "FATURANIZI ÖDEMEYİ UNUTMAYIN!!! SON GÜN BUGÜN!"
    print("Girdi :", test)
    print("Çıktı :", softener.soften(test))

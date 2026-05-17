"""
Ön işleme modülü.

Spam tespit modülü için metin temizleme işlemlerini içerir.
Makale Bölüm 3.2'de açıklanan adımları uygular.
"""

import re


def clean_text(text: str) -> str:
    """
    Spam tespiti için metni temizler.

    Adımlar (makale Bölüm 3.2):
      1. Küçük harfe dönüştürme
      2. URL'leri "URL" jetonu ile değiştirme
      3. Sayıları "NUM" jetonu ile değiştirme
      4. Türkçe karakterleri koruyarak alfasayısal olmayanları temizleme
      5. Boşluk normalizasyonu

    Args:
        text: Ham e-posta metni.

    Returns:
        Temizlenmiş metin.
    """
    text = str(text).lower()
    text = re.sub(r"http[s]?://\S+", " URL ", text)
    text = re.sub(r"www\.\S+", " URL ", text)
    text = re.sub(r"\b\d+\b", " NUM ", text)
    # Türkçe karakterler korunur
    text = re.sub(r"[^\wçğıöşüÇĞİÖŞÜ\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


if __name__ == "__main__":
    ornek = "ACIL!!! Siparişiniz 12345 numaralı kargoda. http://kargo.example.com adresini ziyaret edin."
    print("Girdi :", ornek)
    print("Çıktı :", clean_text(ornek))

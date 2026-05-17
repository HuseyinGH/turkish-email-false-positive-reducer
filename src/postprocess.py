"""
Kural tabanlı son işleme katmanı.

Nöral modelin çıktısını üç kural katmanından geçirir
(makale Bölüm 3.5.1):
  1. Kritik bilgi geri yükleme (marka / URL / sayı koruma)
  2. Bilinen hatalı ikamelerin düzeltilmesi
  3. Kalite denetimi

NOT: Aşağıdaki BRAND_DICT ve KNOWN_FIXES sözlükleri temsilî bir
çekirdek listedir. Tam liste (130+ marka) eğitim sürecinde
genişletilmiştir; Kaggle notebook'unda eksiksiz hâli yer alır.
"""

import re

# Çekirdek marka koruma sözlüğü (tam liste için bk. Kaggle notebook)
BRAND_DICT = {
    "akbank": "Akbank", "garanti": "Garanti BBVA", "qnb": "QNB",
    "ziraat": "Ziraat Bankası", "isbank": "İş Bankası", "yapikredi": "Yapı Kredi",
    "turkcell": "Turkcell", "vodafone": "Vodafone", "turktelekom": "Türk Telekom",
    "trendyol": "Trendyol", "hepsiburada": "Hepsiburada", "n11": "N11",
    "getir": "Getir", "yemeksepeti": "Yemeksepeti", "amazon": "Amazon",
    "netflix": "Netflix", "spotify": "Spotify", "bluetv": "BluTV",
    "aras": "Aras Kargo", "mng": "MNG Kargo", "yurtici": "Yurtiçi Kargo",
    "ptt": "PTT Kargo", "surat": "Sürat Kargo",
    "dask": "DASK", "sgk": "SGK", "epdk": "EPDK", "edevlet": "e-Devlet",
}

# Modelin sıkça yaptığı hatalı ikameler (temsilî)
KNOWN_FIXES = {
    r"\bmüşteri̇\b": "müşteri",
    r"\bhesabini\b": "hesabını",
    r"\bsi̇pari̇ş\b": "sipariş",
}


def _extract_entities(text: str) -> dict:
    """Metinden marka, URL ve sayısal bilgileri çıkarır."""
    urls = re.findall(r"\b(?:http[s]?://|www\.)\S+|\b\w+\.(?:com|net|org|gov|edu)(?:\.tr)?\S*", text)
    numbers = re.findall(r"\b\d[\d.,]*\s*(?:TL|₺|%|adet|gün)?\b", text)
    brands = [b for key, b in BRAND_DICT.items() if key in text.lower()]
    return {"urls": urls, "numbers": numbers, "brands": brands}


def postprocess(original: str, generated: str) -> dict:
    """
    Nöral çıktıya kural tabanlı son işleme uygular.

    Args:
        original: Orijinal (girdi) metin.
        generated: Nöral modelin ürettiği yumuşatılmış metin.

    Returns:
        {"text": str, "issues": list[str]}
    """
    text = generated
    issues = []

    # --- Katman 1: Kritik bilgi geri yükleme ---
    orig_entities = _extract_entities(original)
    gen_lower = text.lower()

    missing_brands = [b for b in orig_entities["brands"] if b.lower() not in gen_lower]
    missing_urls = [u for u in orig_entities["urls"] if u.lower() not in gen_lower]
    missing_numbers = [n for n in orig_entities["numbers"]
                       if n.strip() and n.strip() not in text]

    appendix = []
    if missing_brands:
        appendix.extend(missing_brands)
        issues.append(f"marka geri yüklendi: {missing_brands}")
    if missing_urls:
        appendix.extend(missing_urls)
        issues.append(f"URL geri yüklendi: {missing_urls}")
    if missing_numbers:
        appendix.extend(missing_numbers)
        issues.append(f"sayı geri yüklendi: {missing_numbers}")

    if appendix:
        text = text.rstrip(".") + ". " + " ".join(appendix)

    # --- Katman 2: Bilinen hatalı ikamelerin düzeltilmesi ---
    for pattern, repl in KNOWN_FIXES.items():
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    # --- Katman 3: Kalite denetimi ---
    words = text.split()
    if len(words) != len(set(words)) and len(words) > 5:
        # tekrar eden kelime oranı yüksekse işaretle
        repeat_ratio = 1 - len(set(words)) / len(words)
        if repeat_ratio > 0.3:
            issues.append("yüksek kelime tekrarı")

    if len(text) < len(original) * 0.3:
        issues.append("aşırı kısalma")

    return {"text": text.strip(), "issues": issues}


if __name__ == "__main__":
    orig = "TURKCELL faturanız 250 TL! turkcell.com.tr adresinden ödeyin!"
    gen = "Faturanızın ödenmesi gerekmektedir."
    result = postprocess(orig, gen)
    print("Sonuç :", result["text"])
    print("Notlar:", result["issues"])

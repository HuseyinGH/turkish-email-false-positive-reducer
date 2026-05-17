"""
Türkçe E-Posta Yanlış Pozitif Spam Riski Azaltıcı — Gradio Demo

Hugging Face Spaces üzerinde çalışacak şekilde tasarlanmıştır.
İki model Hugging Face Hub'dan otomatik indirilir.

NOT: Aşağıdaki SPAM_REPO ve MT5_REPO değişkenlerini kendi
Hugging Face kullanıcı adınla güncellemeyi unutma.
"""

import re
import joblib
import torch
import gradio as gr
from huggingface_hub import hf_hub_download
from transformers import MT5Tokenizer, MT5ForConditionalGeneration

# === MODEL DEPOLARI (HuggingFace) ===
SPAM_REPO = "HuseyinGH/turkish-spam-svm"
MT5_REPO = "HuseyinGH/mt5-tr-softener"

# === SPAM CLASSIFIER YÜKLE ===
print("Spam classifier yükleniyor...")
svm_path = hf_hub_download(SPAM_REPO, "spam_svm.joblib")
vec_path = hf_hub_download(SPAM_REPO, "tfidf_vectorizer.joblib")
svm = joblib.load(svm_path)
vectorizer = joblib.load(vec_path)

# === YUMUŞATMA MODELİ YÜKLE ===
print("Yumuşatma modeli yükleniyor...")
tokenizer = MT5Tokenizer.from_pretrained(MT5_REPO)
softener_model = MT5ForConditionalGeneration.from_pretrained(MT5_REPO)
softener_model.eval()
print("Modeller hazır.")

# === MARKA KORUMA SÖZLÜĞÜ (çekirdek) ===
BRAND_DICT = {
    "akbank": "Akbank", "garanti": "Garanti BBVA", "qnb": "QNB",
    "turkcell": "Turkcell", "vodafone": "Vodafone", "trendyol": "Trendyol",
    "hepsiburada": "Hepsiburada", "n11": "N11", "getir": "Getir",
    "netflix": "Netflix", "spotify": "Spotify", "aras": "Aras Kargo",
    "mng": "MNG Kargo", "yurtici": "Yurtiçi Kargo", "ptt": "PTT Kargo",
    "dask": "DASK", "sgk": "SGK", "epdk": "EPDK", "edevlet": "e-Devlet",
}


def clean_text(text):
    """Spam tespiti için metni temizler."""
    t = str(text).lower()
    t = re.sub(r"http[s]?://\S+", " URL ", t)
    t = re.sub(r"www\.\S+", " URL ", t)
    t = re.sub(r"\b\d+\b", " NUM ", t)
    t = re.sub(r"[^\wçğıöşüÇĞİÖŞÜ\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def predict_spam(text):
    """Spam olasılığını (0-1) döndürür."""
    features = vectorizer.transform([clean_text(text)])
    return float(svm.predict_proba(features)[0, 1])


def soften(text):
    """mT5 ile metni yumuşatır."""
    input_text = f"yumusat: {text}"
    inputs = tokenizer(input_text, return_tensors="pt",
                       max_length=256, truncation=True)
    with torch.no_grad():
        outputs = softener_model.generate(
            **inputs, max_length=256, num_beams=4, no_repeat_ngram_size=3
        )
    softened = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Basit marka geri yükleme
    missing = [b for k, b in BRAND_DICT.items()
               if k in text.lower() and b.lower() not in softened.lower()]
    if missing:
        softened = softened.rstrip(".") + ". " + " ".join(missing)
    return softened


def process(text):
    """Üç aşamalı pipeline."""
    if not text or not text.strip():
        return "", 0.0, "", 0.0, "Lütfen bir e-posta metni girin."

    spam_before = predict_spam(text) * 100

    if spam_before < 50:
        return (
            text, round(spam_before, 1), "", 0.0,
            f"✓ Bu metin spam riski düşük (%{spam_before:.1f}). "
            f"Yumuşatmaya gerek yok — sistem müdahale etmez.",
        )

    softened = soften(text)
    spam_after = predict_spam(softened) * 100
    drop = spam_before - spam_after

    status = (f"⚡ Spam riski %{drop:.1f} puan azaldı "
              f"(%{spam_before:.1f} → %{spam_after:.1f}).")
    if spam_after < 50:
        status += " Metin artık normal kategoride."

    return (text, round(spam_before, 1), softened,
            round(spam_after, 1), status)


# === GRADIO ARAYÜZÜ ===
with gr.Blocks(title="Türkçe E-Posta Yumuşatıcı",
               theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📧 Türkçe E-Posta Yanlış Pozitif Spam Riski Azaltıcı")
    gr.Markdown(
        "Meşru fakat agresif tonlu e-postalarınızı kurumsal/profesyonel "
        "tonda yeniden ifade eder ve spam filtrelerine takılma riskini azaltır. "
        "Düşük riskli metinlere müdahale edilmez."
    )

    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(
                label="Orijinal E-Posta",
                placeholder="Örn: KARGONUZ TESLİM EDİLEMEDİ! HEMEN KONTROL EDİN!",
                lines=5,
            )
            btn = gr.Button("Analiz Et ve Yumuşat", variant="primary")
        with gr.Column():
            out_orig = gr.Textbox(label="Orijinal Metin", interactive=False)
            score_before = gr.Number(label="Önce Spam Olasılığı (%)")
            out_soft = gr.Textbox(label="Yumuşatılmış Metin", interactive=False)
            score_after = gr.Number(label="Sonra Spam Olasılığı (%)")
            status = gr.Textbox(label="Durum", interactive=False)

    btn.click(process, inputs=inp,
              outputs=[out_orig, score_before, out_soft, score_after, status])

    gr.Markdown("### Örnekler")
    gr.Examples(
        examples=[
            ["DİKKAT SON GÜN!!! Performans formlarını doldurmadınız, bugün "
             "saat 17:00'de sistem KAPANACAKTIR! Zamsız kalmak istemiyorsanız "
             "HEMEN DOLDURUN!"],
            ["TRAFİK SİGORTANIZ GECİKTİ! BÜYÜK CEZA YİYECEKSİNİZ!!! RAY Sigorta "
             "poliçenizi yaptırmadan TRAFİĞE ÇIKMAYIN! Aracınız BAĞLANABİLİR, "
             "HEMEN teklif alın!"],
            ["GÜVENCE BEDELİNİZ EKSİK KALDI! EPDK sisteminde güncellenen 450 TL "
             "tarife farkını hemen yatırmazsanız elektriğiniz KESİN OLARAK "
             "kesilecek!"],
        ],
        inputs=inp,
    )

    gr.Markdown("---")
    gr.Markdown(
        "**Etik kullanım:** Bu sistem spam veya phishing içeriklerinin "
        "filtrelerden kaçırılması için değil; meşru ama agresif kurumsal "
        "e-postaların profesyonelleştirilmesi için tasarlanmıştır."
    )

if __name__ == "__main__":
    demo.launch()

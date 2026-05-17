# Türkçe E-Postalarda Yanlış Pozitif Spam Riskini Azaltma

Türkçe e-postalarda yanlış pozitif spam sınıflandırması riskini azaltmaya yönelik
hibrit bir yapay zekâ sistemi. Sistem, bir e-postanın spam olup olmadığını tespit
etmenin ötesine geçerek, meşru fakat agresif tonlu kurumsal e-postaları daha
profesyonel/kurumsal bir dile dönüştürür.

## 📰 Makale

Bu repo, aşağıdaki yüksek lisans çalışmasının kod ve veri yardımcılarını içerir:

> Kaplan, H. (2026). Türkçe E-Postalarda Yanlış Pozitif Spam Riskini Azaltmaya
> Yönelik Hibrit Bir Yapay Zekâ Sistemi: Tespit ve Kurumsal Dile Dönüştürme.
> [Dergi adı — yayım sonrası eklenecek].

## 🏗️ Sistem Mimarisi

Sistem üç aşamadan oluşmaktadır:

1. **Tespit Modülü** — TF-IDF + Linear SVM (spam-sınıfı F1 = 0.9886)
2. **Eşik Tabanlı Yönlendirme** — %50 üzeri spam riski taşıyan içerik yumuşatmaya yönlendirilir
3. **Yumuşatma Modülü** — mT5-small (Türkçe, fine-tuned) + kural tabanlı son işleme

## 📊 Sonuçlar

Tutulmuş (held-out) test seti — 118 meşru fakat agresif tonlu e-posta:

| Metrik | Değer |
|---|---|
| Risk altı altküme ortalama spam | %74.5 → %41.0 (-33.4 puan) |
| Normal kategoriye geçen | 25/40 (%62.5) |
| BERTScore F1 | 0.7146 |
| Marka koruma | %100 |
| URL koruma | %91.4 |
| Sayı koruma | %93.8 |

## 🚀 Canlı Demo

Gradio demo: https://huggingface.co/spaces/HuseyinGH/turkish-email-softener

## 📦 Kullanılan Veri Setleri

Spam sınıflandırma veri seti aşağıdaki kamuya açık kaynaklardan derlenmiştir.
Kaynak veri kümeleri bu repoda yeniden dağıtılmamakta; aşağıdaki bağlantılardan
erişilebilir:

| Kaynak | Erişim |
|---|---|
| Turkish Spam V01 | UCI — doi.org/10.24432/C5WG7F (CC BY 4.0) |
| cuneytdemir/turkish-spam-dataset | Kaggle |
| emrahaydemr/turkish-mail-dataset-normalspam | Kaggle |
| anilguven/turkish_spam_email | Hugging Face |
| Turkish SMS Collection (Karasoy & Ballı, 2022) | Kaggle: onurkarasoy/turkish-sms-collection |

## ⚙️ Kurulum

```bash
git clone https://github.com/HuseyinGH/turkish-email-false-positive-reducer.git
cd turkish-email-false-positive-reducer
pip install -r requirements.txt
```

## 💻 Kullanım

```python
from src.pipeline import FalsePositiveReducer

reducer = FalsePositiveReducer()
result = reducer.process("KARGONUZ TESLİM EDİLEMEDİ! HEMEN KONTROL EDİN!!!")

print(result["spam_before"])   # örn. 0.78
print(result["softened"])      # yumuşatılmış metin
print(result["spam_after"])    # örn. 0.22
```

## 📓 Kaggle Notebook

Tam reproduksiyon (eğitim + değerlendirme) için:
https://www.kaggle.com/code/huseyinkaplan0/yumusatma-modeli-v4

## 🤖 Modeller

- **Spam Classifier (SVM)**: https://huggingface.co/HuseyinGH/turkish-spam-svm
- **Yumuşatma Modeli (mT5)**: https://huggingface.co/HuseyinGH/mt5-tr-softener

## ⚖️ Etik Kullanım

Bu sistem, spam veya kimlik avı (phishing) içeriklerinin spam filtrelerinden
kaçırılması amacıyla geliştirilmemiştir. Yalnızca meşru içerikli ancak yapısal
olarak agresif tonda yazıldığı için yanlış pozitif spam riski taşıyan e-postaları
kurumsal/profesyonel bir dile dönüştürmek içindir. Sistem otomatik karar vermez;
kullanıcıya öneri sunar.

## 📜 Lisans

Bu repodaki kod MIT lisansı ile dağıtılmaktadır — bk. [LICENSE](LICENSE).
Kaynak veri kümelerinin lisansları kendi sağlayıcılarına aittir.

## 👤 Yazar

Hüseyin Kaplan — Süleyman Demirel Üniversitesi, Fen Bilimleri Enstitüsü

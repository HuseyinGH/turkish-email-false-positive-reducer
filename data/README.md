# Veri Setleri

## Spam Sınıflandırma Veri Seti

Spam sınıflandırma veri seti, beş kamuya açık kaynaktan ve proje sürecinde
derlenen ek örneklerden birleştirilmiştir. **Birleştirilmiş ham veri seti bu
repoda yeniden dağıtılmamaktadır** — kaynak veri kümelerinin lisans koşulları
gözetilerek yalnızca kaynaklara atıf verilmiştir.

| Kaynak | Erişim |
|---|---|
| Turkish Spam V01 | https://doi.org/10.24432/C5WG7F (CC BY 4.0) |
| cuneytdemir/turkish-spam-dataset | kaggle.com/datasets/cuneytdemir/turkish-spam-dataset |
| emrahaydemr/turkish-mail-dataset-normalspam | kaggle.com/datasets/emrahaydemr/turkish-mail-dataset-normalspam |
| anilguven/turkish_spam_email | huggingface.co/datasets/anilguven/turkish_spam_email |
| Turkish SMS Collection | kaggle.com/datasets/onurkarasoy/turkish-sms-collection |

Birleştirme + temizlik sonrası: 6.727 e-posta (3.522 spam + 3.205 normal).

## Yumuşatma Eş Veri Seti (Sentetik)

Yumuşatma modelinin eğitimi için GPT-5.5 ve Gemini 3.1 Pro ile üretilip yedi
katmanlı kalite filtresinden geçirilen sentetik eş veri seti kullanılmıştır.
Bu veri seti tamamen bu çalışma kapsamında üretilmiştir:

https://www.kaggle.com/datasets/huseyinkaplan0/tez-spam-emails-tr

## samples/

`samples/` klasöründe, sistemin nasıl çalıştığını göstermek amacıyla küçük
örnek dosyalar bulunur (anonim, temsilî).

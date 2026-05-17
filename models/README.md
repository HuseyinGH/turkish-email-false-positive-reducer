# Modeller

Model ağırlıkları boyutları nedeniyle bu repoda tutulmaz; Hugging Face Hub
üzerinden barındırılır.

## Spam Classifier (Linear SVM)

- **HF Deposu**: https://huggingface.co/HuseyinGH/turkish-spam-svm
- TF-IDF + CalibratedClassifierCV(LinearSVC, cv=3)
- Test seti spam-sınıfı F1: 0.9886

Dosyalar: `spam_svm.joblib`, `tfidf_vectorizer.joblib`

## Yumuşatma Modeli (mT5-small)

- **HF Deposu**: https://huggingface.co/HuseyinGH/mt5-tr-softener
- Baz model: ozcangundes/mt5-small-turkish-summarization
- 1.235 eş veri çifti ile yeniden eğitilmiş (7 epok)
- BERTScore F1: 0.7146

## Kullanım

`src/spam_detector.py` ve `src/softener.py` modülleri bu modelleri otomatik
olarak Hugging Face Hub'dan indirir.

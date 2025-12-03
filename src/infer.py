import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import joblib
import pandas as pd
from feature_engineering import extract_features

base_dir = r"C:\Users\Марлен\Documents\ai-security-assistant"
model_path = os.path.join(base_dir, "models", "mvp_model.pkl")
vectorizer_path = os.path.join(base_dir, "models", "vectorizer.pkl")

# ПРИНУДИТЕЛЬНАЯ ПЕРЕЗАГРУЗКА при каждом импорте
import importlib
if 'model' in globals():
    importlib.reload(sys.modules[__name__])

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

def predict_message(text):
    """Predict if message is phishing or safe"""
    df_test = pd.DataFrame({'content': [text]})
    X_test = extract_features(df_test, vectorizer=vectorizer)
    
    label = model.predict(X_test)[0]
    proba = model.predict_proba(X_test)[0]
    confidence = max(proba)
    
    return label, confidence

if __name__ == "__main__":
    test_messages = [
        "Привет, как дела?",
        "Нужна помощь со статьей",
        "Срочно верифицируйте аккаунт по ссылке!",
        "Ваш аккаунт заблокирован. Нажмите здесь!"
    ]
    
    for msg in test_messages:
        label, conf = predict_message(msg)
        symbol = "✓" if (label == "safe" and ("дела" in msg or "помощь" in msg)) or (label == "phish" and ("Срочно" in msg or "заблокирован" in msg)) else "✗"
        print(f"{symbol} Text: {msg}")
        print(f"   Prediction: {label}, Confidence: {conf:.4f}\n")
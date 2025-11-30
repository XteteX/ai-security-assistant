import joblib
import pandas as pd
from feature_engineering import extract_features

# Загрузка модели
model = joblib.load("../models/mvp_model.pkl")

def predict_risk(text):
    df = pd.DataFrame([{'content': text}])
    X = extract_features(df)
    pred = model.predict(X)[0]
    proba = model.predict_proba(X).max()
    return pred, proba

# Пример использования
if __name__ == "__main__":
    text = "Ваш аккаунт заблокирован. Срочно подтвердите данные"
    label, confidence = predict_risk(text)
    print(f"Prediction: {label}, Confidence: {confidence}")

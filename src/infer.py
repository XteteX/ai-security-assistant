import joblib
import pandas as pd
from feature_engineering import extract_features
from explain import build_feature_summary, generate_explanation
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "mvp_model.pkl"
VECTORIZER_PATH = PROJECT_ROOT / "models" / "vectorizer.pkl"

def load_artifacts():
    """Load model artifacts from disk."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
    if not VECTORIZER_PATH.exists():
        raise FileNotFoundError(f"Vectorizer not found: {VECTORIZER_PATH}")
    model = joblib.load(str(MODEL_PATH))
    vectorizer = joblib.load(str(VECTORIZER_PATH))
    return model, vectorizer

model, vectorizer = load_artifacts()

def predict_message(text):
    """Predict if message is phishing or safe"""
    df_test = pd.DataFrame({'content': [text]})
    X_test = extract_features(df_test, vectorizer=vectorizer)
    
    label = model.predict(X_test)[0]
    proba = model.predict_proba(X_test)[0]
    confidence = max(proba)
    
    feature_summary = build_feature_summary(X_test.iloc[0].to_dict())
    explanation = generate_explanation(feature_summary, label, confidence)

    return label, confidence, explanation

if __name__ == "__main__":
    test_messages = [
        "Привет, как дела?",
        "Нужна помощь со статьей",
        "Срочно верифицируйте аккаунт по ссылке!",
        "Ваш аккаунт заблокирован. Нажмите здесь!"
    ]
    
    for msg in test_messages:
        label, conf, explanation = predict_message(msg)
        symbol = "✓" if (label == "safe" and ("дела" in msg or "помощь" in msg)) or (label == "phish" and ("Срочно" in msg or "заблокирован" in msg)) else "✗"
        print(f"{symbol} Text: {msg}")
        print(f"   Prediction: {label}, Confidence: {conf:.4f}\n")
        if explanation:
            print("   Explanation:")
            print(f"   {explanation}\n")

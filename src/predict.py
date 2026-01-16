import joblib
from pathlib import Path
from .feature_engineering import extract_features
from .explain import build_feature_summary, generate_explanation

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "mvp_model.pkl"
VECTORIZER_PATH = PROJECT_ROOT / "models" / "vectorizer.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
if not VECTORIZER_PATH.exists():
    raise FileNotFoundError(f"Vectorizer not found: {VECTORIZER_PATH}")

model = joblib.load(str(MODEL_PATH))
vectorizer = joblib.load(str(VECTORIZER_PATH))

def predict_risk(input_model, df):
    """Predict risk for DataFrame"""
    X = extract_features(df, vectorizer=vectorizer)
    predictions = input_model.predict(X)
    probabilities = input_model.predict_proba(X)
    confidence = probabilities.max(axis=1)[0]
    prediction = "Safe" if predictions[0] == 0 else "Phishing"
    return prediction, confidence


def predict_risk_with_explanation(input_model, df):
    """Predict risk and optionally generate a human-readable explanation."""
    prediction, confidence = predict_risk(input_model, df)
    feature_row = extract_features(df, vectorizer=vectorizer).iloc[0].to_dict()
    feature_summary = build_feature_summary(feature_row)
    explanation = generate_explanation(feature_summary, prediction, confidence)
    return prediction, confidence, explanation

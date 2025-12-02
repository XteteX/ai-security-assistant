import os
import sys
import pandas as pd
import joblib

# === 1. Определяем путь к папке src ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))   # .../ai-security-assistant/src
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))   # .../ai-security-assistant

SRC_DIR = os.path.join(PROJECT_ROOT, "src")

# === 2. Добавляем src в sys.path ===
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

# === 3. Теперь импорт работает ===
from feature_engineering import extract_features

# === 4. Путь к модели ===
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "mvp_model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

MODEL = joblib.load(MODEL_PATH)


def predict_message(text: str):
    df = pd.DataFrame([{"content": text}])
    feats = extract_features(df)
    proba = MODEL.predict_proba(feats)[0]
    label = MODEL.classes_[proba.argmax()]
    confidence = float(max(proba))
    return label, confidence


if __name__ == "__main__":
    print(predict_message("hello world"))

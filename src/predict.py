import pandas as pd
from xgboost import XGBClassifier
from src.feature_engineering import extract_features

# Создаем и обучаем модель на MVP данных
# В реальном проекте лучше загружать обученную модель через joblib
model = XGBClassifier(
    n_estimators=50,
    max_depth=3,
    use_label_encoder=False,
    eval_metric='logloss'
)

def train_model(df: pd.DataFrame):
    X = extract_features(df)
    y = df['label']
    model.fit(X, y)

def predict_risk(model, df: pd.DataFrame):
    X = extract_features(df)
    preds = model.predict(X)
    probs = model.predict_proba(X)
    # Возвращаем первый элемент, если один пример
    return preds[0], max(probs[0])

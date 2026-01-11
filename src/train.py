import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from feature_engineering import extract_features
from pathlib import Path

# ИСПРАВЛЯЕМ ПУТЬ - используем PROJECT_ROOT как в боте
PROJECT_ROOT = Path(__file__).resolve().parents[1]
base_dir = PROJECT_ROOT

data_path = base_dir / "data" / "raw" / "security_logs.csv"
model_path = base_dir / "models" / "mvp_model.pkl"
vectorizer_path = base_dir / "models" / "vectorizer.pkl"

print(f"📂 PROJECT_ROOT: {PROJECT_ROOT}")
print(f"📊 Data path: {data_path}")
print(f"💾 Model will be saved to: {model_path}\n")

# Проверяем, существует ли файл с данными
if not data_path.exists():
    raise FileNotFoundError(f"Data file not found: {data_path}")

df = pd.read_csv(data_path, encoding='utf-8')
print(f"✓ Loaded {len(df)} records")
print(f"Class distribution:\n{df['label'].value_counts()}\n")

vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
vectorizer.fit(df['content'])
print(f"✓ Vocabulary size: {len(vectorizer.vocabulary_)}\n")

X = extract_features(df, vectorizer=vectorizer)
y = df['label']

print(f"✓ Feature shape: {X.shape}")
print(f"✓ Features: {list(X.columns)}\n")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ИСПОЛЬЗУЕМ Random Forest
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    random_state=42,
    class_weight='balanced',
    min_samples_split=5
)

print("🤖 Training model...")
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n⭐ Top 15 features:")
print(feature_importance.head(15))

# Создаем папку для моделей
model_path.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(model, str(model_path))
joblib.dump(vectorizer, str(vectorizer_path))

print(f"\n✅ Model saved to {model_path}")
print(f"✅ Vectorizer saved to {vectorizer_path}")
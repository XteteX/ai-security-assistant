import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # ИЗМЕНИЛИ
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from feature_engineering import extract_features

base_dir = r"C:\Users\Марлен\Documents\ai-security-assistant"
data_path = os.path.join(base_dir, "data", "raw", "security_logs.csv")
model_path = os.path.join(base_dir, "models", "mvp_model.pkl")
vectorizer_path = os.path.join(base_dir, "models", "vectorizer.pkl")

df = pd.read_csv(data_path, encoding='utf-8')
print(f"Loaded {len(df)} records")
print(f"Class distribution:\n{df['label'].value_counts()}\n")

vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
vectorizer.fit(df['content'])
print(f"Vocabulary size: {len(vectorizer.vocabulary_)}\n")

X = extract_features(df, vectorizer=vectorizer)
y = df['label']

print(f"Feature shape: {X.shape}\n")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ИСПОЛЬЗУЕМ Random Forest вместо Logistic Regression
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    random_state=42,
    class_weight='balanced',
    min_samples_split=5
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 15 features:")
print(feature_importance.head(15))

os.makedirs(os.path.dirname(model_path), exist_ok=True)
joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)

print(f"\n✓ Model saved to {model_path}")
print(f"✓ Vectorizer saved to {vectorizer_path}")
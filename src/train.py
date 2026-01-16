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

X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    df[['content']], df['label'], test_size=0.2, random_state=42, stratify=df['label']
)

vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
vectorizer.fit(X_train_raw['content'])
print(f"✓ Vocabulary size: {len(vectorizer.vocabulary_)}\n")

X_train = extract_features(X_train_raw, vectorizer=vectorizer)
X_test = extract_features(X_test_raw, vectorizer=vectorizer)

print(f"✓ Train feature shape: {X_train.shape}")
print(f"✓ Test feature shape: {X_test.shape}")
print(f"✓ Features: {list(X_train.columns)}\n")

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
    'feature': X_train.columns,
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

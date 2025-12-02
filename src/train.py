import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from feature_engineering import extract_features



base_dir = "C:/Users/Марлен/Documents/ai-security-assistant"
file_path = os.path.join(base_dir, "data", "raw", "security_logs.csv")

df = pd.read_csv(file_path)


X = extract_features(df)
y = df['label']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


models_dir = os.path.join(base_dir, "models")
os.makedirs(models_dir, exist_ok=True)  
model_path = os.path.join(models_dir, "mvp_model.pkl")
joblib.dump(model, model_path)

print(f"Модель обучена и сохранена в {model_path}!")
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# TF-IDF векторизатор (будет обучаться на тренировочных данных)
tfidf_vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words='english',
    max_features=500  # можно увеличить позже
)

def clean_text(text: str) -> str:
    """Простая очистка текста"""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " url ", text)  # ссылки
    text = re.sub(r"\S+@\S+", " email ", text)       # email
    text = re.sub(r"[^a-z0-9\s]", " ", text)         # убрать спецсимволы
    text = re.sub(r"\s+", " ", text)                 # убрать лишние пробелы
    return text.strip()

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """Возвращает матрицу признаков для модели"""
    df = df.copy()
    df['content_clean'] = df['content'].astype(str).apply(clean_text)
    X = tfidf_vectorizer.fit_transform(df['content_clean'])
    return X

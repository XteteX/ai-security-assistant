from urllib.parse import urlparse
import pandas as pd
from datetime import datetime

# =========================
# URL признаки
# =========================
def extract_url_features(url_string):
    """Извлекаем базовые признаки из URL"""
    try:
        parsed = urlparse(url_string)
        domain = parsed.netloc.lower()

        suspicious_score = 0
        if any(word in domain for word in ['verify', 'secure', 'account', 'update', 'confirm', 'login', 'bank', 'payment']):
            suspicious_score += 2
        if any(tld in domain for tld in ['.tk', '.ml', '.ga', '.cf', '.ru', '.info', '.site', '.org', '.net']):
            suspicious_score += 1
        if domain.count('-') >= 2:
            suspicious_score += 1

        return {
            'url_suspicious_score': suspicious_score,
            'url_has_ip': 1 if any(char.isdigit() for char in domain.split('.')) and domain.replace('.','').isdigit() else 0,
            'url_has_suspicious_tld': 1 if any(tld in domain for tld in ['.tk', '.ml', '.ga', '.cf', '.ru', '.info', '.site']) else 0,
            'url_dots_count': domain.count('.'),
            'url_domain_length': len(domain),
            'url_dashes_count': domain.count('-')
        }
    except:
        return {
            'url_suspicious_score': 0,
            'url_has_ip': 0,
            'url_has_suspicious_tld': 0,
            'url_dots_count': 0,
            'url_domain_length': 0,
            'url_dashes_count': 0
        }

# =========================
# Основная функция извлечения признаков
# =========================
def extract_features(df, vectorizer=None):
    df = df.copy()
    if 'content' not in df.columns:
        raise ValueError("DataFrame must contain 'content' column")
    df['content'] = df['content'].fillna('').astype(str)

    # --- базовые текстовые признаки ---
    df['length'] = df['content'].apply(len)
    df['word_count'] = df['content'].apply(lambda x: len(x.split()))
    df['num_links'] = df['content'].apply(lambda x: x.lower().count('http'))

    # Фишинг / безопасные слова
    phishing_words = [
        'срочно', 'верифи', 'пароль', 'клик', 'подтверд', 'восстан',
        'блокирова', 'закрыт', 'выигра', 'приз', 'ограничен', 'угроз',
        'действ', 'немедленно', 'обнови', 'активиру', 'подключи', 'код',
        'аккаунт', 'заполните', 'форма', 'проверку', 'оплатите', 'доступ',
        'платеж', 'подтвердите', 'заблокирован', 'проверить', 'ссылка', 
        'здесь', 'нажмите', 'отправьте', 'введите', 'задолженн'
    ]
    safe_words = [
        'привет', 'спасибо', 'помощь', 'встреч', 'урок', 'домашн',
        'учител', 'материал', 'задан', 'экзамен', 'друг', 'семья'
    ]
    df['phishing_words'] = df['content'].apply(lambda x: sum(3 for word in phishing_words if word in x.lower()))
    df['safe_words'] = df['content'].apply(lambda x: sum(2 for word in safe_words if word in x.lower()))
    df['uppercase_ratio'] = df['content'].apply(lambda x: sum(1 for c in x if c.isupper()) / len(x) if len(x) > 0 else 0)
    df['exclamation_count'] = df['content'].apply(lambda x: x.count('!'))
    df['email_count'] = df['content'].apply(lambda x: x.lower().count('@'))

    # --- URL признаки ---
    url_features = df['content'].apply(lambda x: extract_url_features(x) if 'http' in x.lower() else {
        'url_suspicious_score': 0, 'url_has_ip': 0, 'url_has_suspicious_tld': 0,
        'url_dots_count': 0, 'url_domain_length': 0, 'url_dashes_count': 0
    })
    url_df = pd.DataFrame(url_features.tolist())
    df = pd.concat([df, url_df], axis=1)

    # --- Упрощенные WHOIS/SSL признаки (без WHOIS запросов) ---
    df['domain_age_days'] = 0
    df['last_update_days'] = 0
    df['has_ssl'] = 0

    # --- TF-IDF признаки ---
    if vectorizer is not None:
        tfidf_matrix = vectorizer.transform(df['content'])
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(),
                                columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])])
        df = pd.concat([df.reset_index(drop=True), tfidf_df], axis=1)

    feature_columns = [col for col in df.columns if col not in ['content', 'label', 'id', 'input_type']]
    return df[feature_columns]
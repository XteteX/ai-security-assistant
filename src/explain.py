import json
import os
from urllib.request import Request, urlopen


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o-mini"


def build_feature_summary(feature_row):
    """Prepare a concise feature summary for explanation."""
    fields = [
        "phishing_words",
        "safe_words",
        "num_links",
        "url_suspicious_score",
        "url_has_ip",
        "url_has_suspicious_tld",
        "uppercase_ratio",
        "exclamation_count",
        "email_count",
        "domain_age_days",
        "has_ssl",
        "length",
        "word_count",
    ]
    summary = {}
    for field in fields:
        if field in feature_row:
            summary[field] = feature_row[field]
    return summary


def generate_explanation(feature_summary, prediction, confidence):
    """Generate a short explanation using OpenAI API.

    Returns None when API is unavailable or disabled.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    prompt = (
        "Сформулируй краткое объяснение решения модели в 3-5 пунктах. "
        "Опирайся на признаки и итоговый класс. "
        "Не выдумывай новые факты."
    )
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Ты помогаешь объяснить решение модели по признакам.",
            },
            {
                "role": "user",
                "content": (
                    f"Класс: {prediction}\n"
                    f"Уверенность: {confidence:.4f}\n"
                    f"Признаки: {json.dumps(feature_summary, ensure_ascii=False)}\n"
                    f"{prompt}"
                ),
            },
        ],
        "temperature": 0.2,
        "max_tokens": 200,
    }

    request = Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=10) as response:
            response_body = response.read().decode("utf-8")
        data = json.loads(response_body)
        return data["choices"][0]["message"]["content"].strip()
    except (OSError, KeyError, ValueError, IndexError):
        return None

import os

import google.generativeai as genai


def _build_prompt(text: str, label: str, confidence: float) -> str:
    label_ru = "фишинг" if label == "phish" else "безопасно"
    confidence_percent = f"{confidence * 100:.1f}%"
    return (
        "Ты — помощник по кибербезопасности. Объясни, почему модель "
        f"могла классифицировать сообщение как «{label_ru}» с уверенностью {confidence_percent}.\n"
        "Условия:\n"
        "- Используй 2–4 кратких пункта.\n"
        "- Опирайся только на текст сообщения и общие признаки (социальная инженерия, срочность, просьба перейти по ссылке, "
        "подозрительные домены, грамматические ошибки, давление, финансовые обещания).\n"
        "- Не утверждай, что у тебя есть доступ к данным пользователя или внутренностям модели.\n"
        "- Если сообщение выглядит безопасно, укажи, какие признаки снижают риск.\n\n"
        f"Сообщение:\n{text}"
    )


def generate_explanation(text: str, label: str, confidence: float) -> str | None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = _build_prompt(text, label, confidence)
    response = model.generate_content(prompt)
    if not response or not response.text:
        return None
    return response.text.strip()

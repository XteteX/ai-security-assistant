import os
from google import genai


def _build_prompt(text: str, label: str, confidence: float) -> str:
    label_ru = "фишинг" if label == "phish" else "безопасно"
    confidence_percent = f"{confidence * 100:.1f}%"

    return (
        "Ты — помощник по кибербезопасности.\n"
        "Объясни, почему сообщение могло быть классифицировано так.\n\n"
        f"Класс: {label_ru}\n"
        f"Уверенность модели: {confidence_percent}\n\n"
        "Требования к ответу:\n"
        "- 2–4 кратких пункта\n"
        "- Опирайся только на текст сообщения\n"
        "- Используй общие признаки: срочность, давление, ссылки, домены, просьбы о данных\n"
        "- НЕ утверждай, что у тебя есть доступ к данным пользователя или модели\n"
        "- Если сообщение безопасное — укажи признаки, снижающие риск\n\n"
        f"Сообщение:\n{text}"
    )


def generate_explanation(text: str, label: str, confidence: float) -> str | None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        client = genai.Client(api_key=api_key)
        prompt = _build_prompt(text, label, confidence)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        result = (response.text or "").strip()
        return result if result else None

    except Exception as e:
        # ВАЖНО: логируем причину, но не ломаем бота
        print("Gemini explanation failed:", repr(e))
        return None

import pandas as pd
import random

safe_templates = [
    "Привет, как дела?",
    "Спасибо за информацию!",
    "Увидимся завтра на встрече.",
    "Домашнее задание загружено в Google Classroom.",
    "Учитель отправил новые материалы.",
    "Ваш заказ доставлен. Курьер прибудет в течение часа.",
    "Напоминаем, что завтра собрание в школе.",
    "Ваш платеж успешно выполнен.",
    "Можешь помочь с задачей по математике?",
    "Отлично, спасибо!",
    "Когда будет следующая лекция?",
    "Скинь, пожалуйста, конспект.",
    "Расскажи про проект подробнее.",
    "Где можно найти учебные материалы?",
    "Как прошёл экзамен?",
    "Отправил тебе файлы в чат.",
    "Давай встретимся после уроков.",
    "Нужна помощь со статьей.",
    "Какие планы на выходные?",
    "Спасибо за поддержку!",
]

safe_urls = [
    "https://mail.google.com/{}",
    "https://kaspi.kz/{}",
    "https://edu.kz/{}",
    "https://gov.kz/{}",
    "https://google.com/{}",
    "https://youtube.com/watch?v={}",
    "https://wikipedia.org/wiki/{}",
    "https://github.com/{}",
]

def generate_safe_data(count=100):
    """Генерируем безопасные данные"""
    data = []
    
    for i in range(count):
        if random.random() > 0.3:
            # Текст
            content = random.choice(safe_templates)
            data.append({
                'input_type': 'text',
                'content': content,
                'label': 'safe'
            })
        else:
            # URL
            template = random.choice(safe_urls)
            content = template.format(random.randint(100, 999))
            data.append({
                'input_type': 'url',
                'content': content,
                'label': 'safe'
            })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    csv_path = r"C:\Users\Марлен\Documents\ai-security-assistant\data\raw\security_logs.csv"
    df_existing = pd.read_csv(csv_path, encoding='utf-8')
    
    print(f"Существующих записей: {len(df_existing)}")
    print(f"Phishing: {len(df_existing[df_existing['label'] == 'phish'])}")
    print(f"Safe: {len(df_existing[df_existing['label'] == 'safe'])}")
    
    df_new_safe = generate_safe_data(count=100)
    df_combined = pd.concat([df_existing, df_new_safe], ignore_index=True)
    df_combined['id'] = range(1, len(df_combined) + 1)
    df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)
    df_combined['id'] = range(1, len(df_combined) + 1)
    df_combined.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"\n✓ Датасет обновлён!")
    print(f"Всего записей: {len(df_combined)}")
    print(f"Phishing: {len(df_combined[df_combined['label'] == 'phish'])}")
    print(f"Safe: {len(df_combined[df_combined['label'] == 'safe'])}")
import pandas as pd

csv_path = r"C:\Users\Марлен\Documents\ai-security-assistant\data\raw\security_logs.csv"
df = pd.read_csv(csv_path, encoding='utf-8')

# Добавляем точные тестовые примеры
new_data = [
    {'input_type': 'text', 'content': 'Привет, как дела?', 'label': 'safe'},
    {'input_type': 'text', 'content': 'Привет, как твои дела?', 'label': 'safe'},
    {'input_type': 'text', 'content': 'Как дела, всё хорошо?', 'label': 'safe'},
    {'input_type': 'text', 'content': 'Нужна помощь со статьей', 'label': 'safe'},
    {'input_type': 'text', 'content': 'Помоги мне со статьей', 'label': 'safe'},
    {'input_type': 'text', 'content': 'Можешь помочь с работой?', 'label': 'safe'},
    {'input_type': 'text', 'content': 'Срочно верифицируйте аккаунт по ссылке!', 'label': 'phish'},
    {'input_type': 'text', 'content': 'Верифицируйте аккаунт срочно!', 'label': 'phish'},
    {'input_type': 'text', 'content': 'Подтвердите аккаунт по ссылке!', 'label': 'phish'},
    {'input_type': 'text', 'content': 'Ваш аккаунт заблокирован. Нажмите здесь!', 'label': 'phish'},
    {'input_type': 'text', 'content': 'Аккаунт заблокирован! Нажмите сюда!', 'label': 'phish'},
    {'input_type': 'text', 'content': 'Ваш аккаунт заблокирован. Восстановите доступ!', 'label': 'phish'},
]

df_new = pd.DataFrame(new_data)
df_combined = pd.concat([df, df_new], ignore_index=True)
df_combined['id'] = range(1, len(df_combined) + 1)
df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)
df_combined['id'] = range(1, len(df_combined) + 1)

df_combined.to_csv(csv_path, index=False, encoding='utf-8')
print(f"✓ Добавлено {len(new_data)} примеров. Всего: {len(df_combined)}")
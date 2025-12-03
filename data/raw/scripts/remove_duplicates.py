import pandas as pd

csv_path = r"C:\Users\Марлен\Documents\ai-security-assistant\data\raw\security_logs.csv"
df = pd.read_csv(csv_path, encoding='utf-8')

print(f"До: {len(df)} записей")
print(df['label'].value_counts())
print(f"Safe дубликаты: {df[df['label']=='safe']['content'].duplicated().sum()}")
print(f"Phish дубликаты: {df[df['label']=='phish']['content'].duplicated().sum()}")

# Удалить дубликаты внутри каждого класса
df_safe = df[df['label'] == 'safe'].drop_duplicates(subset=['content']).reset_index(drop=True)
df_phish = df[df['label'] == 'phish'].drop_duplicates(subset=['content']).reset_index(drop=True)

df_clean = pd.concat([df_safe, df_phish], ignore_index=True)
df_clean = df_clean.sample(frac=1, random_state=42).reset_index(drop=True)
df_clean['id'] = range(1, len(df_clean) + 1)

df_clean.to_csv(csv_path, index=False, encoding='utf-8')

print(f"\n✓ После: {len(df_clean)} записей")
print(df_clean['label'].value_counts())
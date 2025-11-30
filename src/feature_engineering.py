import pandas as pd
def extract_features(df):
    df = df.copy()
    
    # Длина текста/URL
    df['length'] = df['content'].apply(len)
    
    # Количество слов
    df['word_count'] = df['content'].apply(lambda x: len(str(x).split()))
    
    # Количество ссылок
    df['num_links'] = df['content'].apply(lambda x: str(x).count('http'))
    
    # Подозрительные слова
    suspicious_words = ['urgent','verify','login','код','срочно']
    df['suspicious_words'] = df['content'].apply(lambda x: sum(word in x.lower() for word in suspicious_words))
    
    return df[['length','word_count','num_links','suspicious_words']]

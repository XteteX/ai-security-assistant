import pandas as pd
import random

# Шаблоны фишинга
phishing_templates = [
    "Ваш аккаунт {service} заблокирован. Срочно подтвердите данные по ссылке.",
    "Поздравляем! Вы выиграли {prize}. Для получения оплатите доставку {amount} тг.",
    "Срочно! Ваш банковский счёт будет закрыт через {hours} часов. Обновите реквизиты.",
    "Акция! Пополни баланс и получи х{multiplier}. Осталось {minutes} минут!",
    "Техподдержка {service}. Отправьте код из SMS, иначе аккаунт удалят.",
    "Ваша карта {card_type} заблокирована. Заполните форму для разблокировки.",
    "Подтвердите личность. Отправьте {doc_type} по ссылке ниже.",
    "Ваш {device} заражён вирусами! Скачайте антивирус по ссылке.",
    "Я случайно перевёл вам {amount} тенге. Верните, пожалуйста, по ссылке.",
    "СРОЧНО! Ваш {relative} в беде. Нужны деньги. Не звоните, переведите сюда!",
    "Обновление безопасности {service}. Введите пароль для продолжения работы.",
    "Ваш платёж не прошёл. Повторите попытку через эту форму.",
    "Обнаружена подозрительная активность в аккаунте {service}. Проверьте срочно!",
    "Вы выбраны участником опроса. Введите {data_type} и получите {amount} тг.",
    "Сессия истекла. Авторизуйтесь заново по ссылке, иначе доступ закроется.",
    "Внимание! Ваш заказ не может быть доставлен. Подтвердите адрес здесь.",
    "Ваша подписка {service} истекает. Продлите сейчас со скидкой 50%!",
    "Последнее предупреждение! Оплатите задолженность {amount} тг до {date}.",
    "Ваши данные устарели. Обновите информацию, иначе аккаунт будет удалён.",
    "Бонус {amount} тенге на ваш счёт! Активируйте по ссылке в течение часа.",
]

phishing_urls = [
    "http://secure-login-{service}.com/verify",
    "https://{service}-support-center-{num}.info",
    "http://bank-{country}-confirm-{num}.net",
    "https://free-{prize}-giveaway-{num}.org",
    "http://{service}-recovery-id-{num}.ru",
    "https://{service}-verify-account-{num}.site",
    "http://update-{service}-security-{num}.com",
    "https://{service}-payment-confirm-{num}.net",
    "http://promo-bonus-{service}-{num}.info",
    "https://safety-check-{service}-{num}.org",
]

# Параметры для подстановки
params = {
    'service': ['Kaspi', 'Instagram', 'Facebook', 'Google', 'Telegram', 'WhatsApp', 'VK', 'Mail.ru', 'Steam', 'TikTok'],
    'prize': ['iPhone 15', 'Samsung Galaxy', 'MacBook Pro', 'iPad', 'AirPods', 'PlayStation 5', '100000 тенге'],
    'amount': ['5000', '10000', '15000', '25000', '50000'],
    'hours': ['12', '24', '48'],
    'multiplier': ['2', '3', '5', '10'],
    'minutes': ['10', '15', '30', '60'],
    'card_type': ['Visa', 'MasterCard', 'UnionPay', 'МИР'],
    'doc_type': ['фото паспорта', 'селфи с паспортом', 'копию СНП', 'скан документа'],
    'device': ['компьютер', 'телефон', 'планшет', 'ноутбук'],
    'relative': ['родственник', 'сын', 'дочь', 'друг', 'коллега'],
    'data_type': ['email', 'номер телефона', 'данные карты', 'адрес'],
    'date': ['сегодня', 'завтра', '15.12.2024'],
    'country': ['Kazakhstan', 'Russia', 'Ukraine'],
    'num': [str(random.randint(100, 999)) for _ in range(100)]
}

def generate_phishing_data(count=100):
    """Генерируем фишинговые данные"""
    data = []
    
    for i in range(count):
        # Выбираем случайный тип (текст или URL)
        if random.random() > 0.5:
            # Текст
            template = random.choice(phishing_templates)
            content = template
            
            # Заполняем параметры
            for key in params:
                if '{' + key + '}' in content:
                    content = content.replace('{' + key + '}', random.choice(params[key]))
            
            data.append({
                'input_type': 'text',
                'content': content,
                'label': 'phish'
            })
        else:
            # URL
            template = random.choice(phishing_urls)
            content = template
            
            # Заполняем параметры
            for key in params:
                if '{' + key + '}' in content:
                    content = content.replace('{' + key + '}', random.choice(params[key]))
            
            data.append({
                'input_type': 'url',
                'content': content,
                'label': 'phish'
            })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Загрузить существующий датасет
    csv_path = r"C:\Users\Марлен\Documents\ai-security-assistant\data\raw\security_logs.csv"
    df_existing = pd.read_csv(csv_path, encoding='utf-8')
    
    print(f"Существующих записей: {len(df_existing)}")
    print(f"Phishing: {len(df_existing[df_existing['label'] == 'phish'])}")
    print(f"Safe: {len(df_existing[df_existing['label'] == 'safe'])}")
    
    # Генерируем новые фишинговые примеры
    df_new_phishing = generate_phishing_data(count=100)
    
    # Объединяем
    df_combined = pd.concat([df_existing, df_new_phishing], ignore_index=True)
    
    # Пересчитываем ID
    df_combined['id'] = range(1, len(df_combined) + 1)
    
    # Перемешиваем
    df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)
    df_combined['id'] = range(1, len(df_combined) + 1)
    
    # Сохраняем
    df_combined.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"\n✓ Датасет обновлён!")
    print(f"Всего записей: {len(df_combined)}")
    print(f"Phishing: {len(df_combined[df_combined['label'] == 'phish'])}")
    print(f"Safe: {len(df_combined[df_combined['label'] == 'safe'])}")
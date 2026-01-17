import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print(f"sys.path[0]: {sys.path[0]}")

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ИМПОРТИРУЕМ НАПРЯМУЮ joblib и функции
import joblib
import pandas as pd
import sys
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from feature_engineering import extract_features
from gemini_explainer import generate_explanation

# ЗАГРУЖАЕМ МОДЕЛЬ НАПРЯМУЮ В БОТЕ
base_dir = PROJECT_ROOT
model_path = base_dir / "models" / "mvp_model.pkl"
vectorizer_path = base_dir / "models" / "vectorizer.pkl"

print(f"\n📂 Загружаю модель из: {model_path}")
print(f"   Файл существует: {model_path.exists()}")

model = joblib.load(str(model_path))
vectorizer = joblib.load(str(vectorizer_path))

def predict_message_bot(text):
    """Predict функция для бота"""
    df_test = pd.DataFrame({'content': [text]})
    X_test = extract_features(df_test, vectorizer=vectorizer)
    label = model.predict(X_test)[0]
    proba = model.predict_proba(X_test)[0]
    confidence = max(proba)
    return label, confidence

# ТЕСТ ПРИ ЗАПУСКЕ
print("\n🔍 Тестирую модель при запуске бота:")
test_label, test_conf = predict_message_bot("Срочно верифицируйте аккаунт!")
print(f"   Тест: label={test_label}, confidence={test_conf:.4f}\n")

TOKEN = os.environ.get("TG_TOKEN")
if not TOKEN:
    raise RuntimeError("Set TG_TOKEN environment variable: $env:TG_TOKEN = 'YOUR_TOKEN'")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я AI Security Assistant.\n\n"
        "Отправь мне текст или ссылку, и я проверю, безопасно ли это.\n\n"
        "Команды:\n"
        "/start - начать\n"
        "/help - помощь"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 Как использовать:\n\n"
        "1. Отправь мне любое сообщение или ссылку\n"
        "2. Я проверю, фишинг это или нет\n"
        "3. Увидишь результат с уровнем уверенности\n"
        "4. Если подключен Gemini API — получишь краткое объяснение\n\n"
        "Примеры:\n"
        "✅ 'Привет, как дела?'\n"
        "❌ 'Срочно подтвердите аккаунт!'"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text("🔍 Проверяю...")
    
    try:
        label, confidence = predict_message_bot(text)
        
        print(f"DEBUG: text='{text[:50]}', label={label}, confidence={confidence:.4f}")
        
        if label == 'phish':
            emoji = "🚨"
            result = "ФИШИНГ"
            color = "🔴"
        else:
            emoji = "✅"
            result = "БЕЗОПАСНО"
            color = "🟢"

        explanation = generate_explanation(text, label, confidence)
        
        response = (
            f"{emoji} **{result}** {color}\n\n"
            f"📊 Уверенность: {confidence*100:.1f}%\n\n"
            f"💬 Сообщение:\n`{text[:200]}{'...' if len(text) > 200 else ''}`"
        )

        if explanation:
            response += f"\n\n🧠 Объяснение:\n{explanation}"
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        await update.message.reply_text(
            f"❌ Ошибка при проверке:\n`{str(e)}`",
            parse_mode='Markdown'
        )

def main():
    print("🤖 Запуск бота...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("✅ Бот запущен! Нажмите Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()

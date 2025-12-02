import os
import joblib
import pandas as pd
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from src.predict import predict_risk

# Получить токен из переменной окружения (не из кода!)
TOKEN = os.environ.get("TG_TOKEN")
if not TOKEN:
    raise RuntimeError("Set TG_TOKEN environment variable: $env:TG_TOKEN = '8479187060:AAGd3Nm211zuQ68jHfbO6hJI06nk8eJSeCk'")

# Путь к модели — от корня проекта (3 уровня вверх: app/bot/tg_bot.py -> корень)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "mvp_model.pkl"
print(f"Model path: {MODEL_PATH}")
print(f"Exists? {MODEL_PATH.exists()}")

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

model = joblib.load(str(MODEL_PATH))

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Send me a message or URL, and I will check if it's safe or phishing."
    )

# Обработка текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    df = pd.DataFrame([{"content": text}])
    prediction, confidence = predict_risk(model, df)
    await update.message.reply_text(f"Prediction: {prediction}, Confidence: {confidence:.2f}")

# Обработка файлов
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_path = PROJECT_ROOT / "data" / "raw" / update.message.document.file_name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    await file.download_to_drive(str(file_path))
    df = pd.DataFrame([{"content": update.message.document.file_name}])
    prediction, confidence = predict_risk(model, df)
    await update.message.reply_text(f"File: {update.message.document.file_name}\nPrediction: {prediction}, Confidence: {confidence:.2f}")

# Основная функция запуска бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    
    app.run_polling()

if __name__ == "__main__":
    main()
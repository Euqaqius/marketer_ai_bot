import os
import logging
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
import openai
import sqlite3
from datetime import datetime

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Подключение к SQLite для логирования
conn = sqlite3.connect("logs.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    url TEXT,
    date TEXT,
    result TEXT
)
""")
conn.commit()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я — ИИ-маркетолог 🤖\n"
        "Отправь ссылку на сайт, и я подскажу, что можно улучшить, чтобы получать больше клиентов."
    )

# Обработка входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = extract_url(update.message.text)
    if not url:
        await update.message.reply_text("❌ Пожалуйста, пришлите корректную ссылку на сайт.")
        return

    await update.message.reply_text("🔍 Анализирую сайт, это займёт 10–15 секунд...")

    try:
        headers = {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/115.0.0.0 Safari/537.36")
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string.strip() if soup.title else "Без заголовка"
        body_text = soup.get_text(separator=' ', strip=True)[:3000]

        prompt = (
            f"Проанализируй сайт с точки зрения маркетинга и UX.\n"
            f"Заголовок: {title}\n"
            f"URL: {url}\n"
            f"Текст сайта: {body_text}\n\n"
            f"Сделай краткий аудит — 3–5 пунктов, что можно улучшить, чтобы повысить число заявок. "
            f"Пиши простым языком. В конце добавь общее резюме."
        )

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content.strip()

        await update.message.reply_text(result)

        # Логируем
        cursor.execute("INSERT INTO logs (telegram_id, url, date, result) VALUES (?, ?, ?, ?)", (
            update.message.from_user.id,
            url,
            datetime.now().isoformat(),
            result[:500]  # усечённый результат
        ))
        conn.commit()

    except Exception as e:
        logging.error(f"Ошибка при обработке сайта: {e}", exc_info=True)
        await update.message.reply_text(f"⚠️ Не удалось загрузить сайт. Проверьте ссылку.\nОшибка: {e}")


# Вытаскиваем ссылку
def extract_url(text):
    if not text:
        return None
    if not text.startswith("http"):
        text = "http://" + text
    return text if "." in text else None

# Запуск приложения
if __name__ == "__main__":
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN отсутствует в .env")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY отсутствует в .env")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущен")
    app.run_polling()

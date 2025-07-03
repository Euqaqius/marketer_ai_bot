# 🤖 AI Marketing Bot

Бот для Telegram, который делает краткий маркетинг- и UX-аудит сайта по ссылке, используя OpenAI GPT-4o.

## 📦 Возможности

- Принимает ссылку на сайт
- Делает запрос и извлекает текст с сайта
- Отправляет текст в OpenAI GPT для анализа
- Возвращает 3–5 пунктов с рекомендациями по улучшению
- Логирует запросы в SQLite базу

## 🚀 Установка

1. Клонируй репозиторий или распакуй архив:
    ```bash
    git clone https://github.com/yourusername/ai_marketing_bot.git
    cd ai_marketing_bot
    ```

2. Создай виртуальное окружение и активируй его:
    ```bash
    python -m venv venv
    source venv/bin/activate  # или venv\Scripts\activate на Windows
    ```

3. Установи зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Создай файл `.env` на основе `.env.example`:
    ```bash
    cp .env.example .env
    ```

5. Запусти бота:
    ```bash
    python main.py
    ```

## 🧠 Используемые технологии

- Python
- Telegram Bot API (`python-telegram-bot`)
- OpenAI GPT-4o
- BeautifulSoup
- SQLite

## ⚠️ Важно

- Для работы необходимы действующие API-ключи OpenAI и Telegram.
- GPT-4o работает только с новым SDK OpenAI (`openai >= 1.0.0`).

## 📄 Лицензия

MIT

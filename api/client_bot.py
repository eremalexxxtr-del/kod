import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Токен берется из настроек Vercel (переменная CLIENT_BOT_TOKEN)
TOKEN = os.environ.get('CLIENT_BOT_TOKEN')

@app.route('/api/client_bot', methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        user_name = update["message"]["from"].get("first_name", "Друже")
        
        # Текст приветствия (тот самый функционал)
        welcome_text = (
            f"👋 Вітаю, {user_name}!\n\n"
            f"Дякую за довіру! Я отримав вашу заявку на розробку лендингу. 🚀\n\n"
            f"📥 **Ось те, що я обіцяв:**\n"
            f"• [Прайс-лист на послуги](https://google.com) (заміни на своє посилання)\n"
            f"• [Бриф на розробку](https://google.com) (заміни на своє посилання)\n\n"
            f"Я вже вивчаю ваш запит і напишу вам особисто протягом години. Гарного дня!"
        )
        
        # Отправка сообщения клиенту
        send_message(chat_id, welcome_text)
        
    return jsonify({"status": "ok"}), 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    requests.post(url, json=payload)

# Это нужно для работы на Vercel
def handler(request):
    return app(request)
import os
import json
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Получаем размер тела запроса
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON"})
            return

        # Достаем данные из payload твоего JS
        name = data.get('name', 'Не вказано')
        contact = data.get('contact', 'Не вказано')
        message_text = data.get('message', '')
        need_bot = "ТАК (+500 грн) 🤖" if data.get('need_bot') else "Ні"

        # Токены из переменных окружения Vercel
        token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')

        if not token or not chat_id:
            self._send_response(500, {"error": "Server config error"})
            return

        # Формируем красивое сообщение для Telegram
        tg_msg = (
            f"🔥 <b>НОВА ЗАЯВКА | ko.d</b> 🔥\n\n"
            f"👤 <b>Ім'я:</b> {name}\n"
            f"📞 <b>Контакт:</b> {contact}\n"
            f"🛠 <b>Потрібен бот:</b> {need_bot}\n"
        )
        
        if message_text:
            tg_msg += f"📝 <b>Проєкт:</b> {message_text}\n"
            
        tg_msg += f"\n🌐 <i>Джерело: Vercel Backend</i>"

        # Запрос к Telegram API
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": tg_msg,
            "parse_mode": "html"
        }

        try:
            r = requests.post(url, json=payload)
            if r.status_code == 200:
                self._send_response(200, {"status": "success"})
            else:
                self._send_response(502, {"error": "Telegram API Error"})
        except Exception as e:
            self._send_response(500, {"error": str(e)})

    # Вспомогательный метод для отправки HTTP-ответов
    def _send_response(self, status_code, json_body):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        # Разрешаем CORS (чтобы браузер не блокировал запросы)
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        self.wfile.write(json.dumps(json_body).encode('utf-8'))
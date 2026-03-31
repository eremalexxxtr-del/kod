import os
import json
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Читаем то, что прислал Telegram
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
            
            # 2. Если кто-то нажал /start или написал сообщение
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                user_name = update["message"]["from"].get("first_name", "Друже")
                
                # 3. Достаем токен из настроек Vercel
                token = os.environ.get('CLIENT_BOT_TOKEN')
                
                # 4. Текст ответа бота
                text = (
                    f"👋 Вітаю, {user_name}!\n\n"
                    f"Дякую за довіру! Я отримав вашу заявку на розробку лендингу. 🚀\n\n"
                    f"📥 **Ось обіцяні матеріали:**\n"
                    f"• Прайс-лист на послуги\n"
                    f"• Бриф на розробку\n\n"
                    f"Розробник зв'яжеться з вами найближчим часом."
                )
                
                # 5. Отправляем сообщение клиенту
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                requests.post(url, json={
                    "chat_id": chat_id, 
                    "text": text,
                    "parse_mode": "Markdown"
                })
        except Exception as e:
            print("Error:", e)

        # 6. Обязательно говорим Vercel, что всё ОК (иначе сервер зависнет)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
        return
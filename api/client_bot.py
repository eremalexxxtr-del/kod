import os
import json
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
            
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                user_name = update["message"]["from"].get("first_name", "Друже")
                token = os.environ.get('CLIENT_BOT_TOKEN')
                
                # Текст стал короче, так как суть теперь в кнопках
                text = (
                    f"👋 Вітаю, {user_name}!\n\n"
                    f"Дякую за довіру! Я отримав вашу заявку на розробку лендингу. 🚀\n\n"
                    f"👇 Ось обіцяні матеріали. Тисніть на кнопки нижче:"
                )
                
                # А ВОТ И САМИ КНОПКИ
                reply_markup = {
                    "inline_keyboard": [
                        [{"text": "📊 Мій прайс-лист", "url": "https://docs.google.com/document/..."}], # Замени на свою ссылку
                        [{"text": "📝 Бриф на розробку", "url": "https://forms.gle/..."}],            # Замени на свою ссылку
                        [{"text": "👨‍💻 Написати мені особисто", "url": "https://t.me/ТВОЙ_ЛИЧНЫЙ_ЮЗЕРНЕЙМ"}] # Замени на свой юзернейм
                    ]
                }
                
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                requests.post(url, json={
                    "chat_id": chat_id, 
                    "text": text,
                    "parse_mode": "Markdown",
                    "reply_markup": reply_markup
                })
        except Exception as e:
            print("Error:", e)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
        return
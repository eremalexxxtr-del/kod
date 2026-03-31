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
                user_name = update["message"]["from"].get("first_name", "Клієнт")
                text_received = update["message"].get("text", "")
                token = os.environ.get('CLIENT_BOT_TOKEN')
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                
                # 1. Если клиент только зашел и нажал /start
                if text_received == "/start":
                    text = (
                        f"👋 Вітаю, {user_name}!\n\n"
                        f"Я отримав заявку на розробку лендингу. 🚀\n"
                        f"Обирай потрібний розділ у меню внизу екрана 👇"
                    )
                    # ВОТ ОНА - НИЖНЯЯ КЛАВИАТУРА ВМЕСТО ПОЛЯ ВВОДА
                    reply_markup = {
                        "keyboard": [
                            [{"text": "📊 Мій прайс-лист"}],
                            [{"text": "📝 Бриф на розробку"}],
                            [{"text": "👨‍💻 Написати мені особисто"}]
                        ],
                        "resize_keyboard": True, # Делает кнопки аккуратными
                        "is_persistent": True    # Держит клавиатуру всегда открытой
                    }
                    requests.post(url, json={"chat_id": chat_id, "text": text, "reply_markup": reply_markup})
                
                # 2. Обработка нажатий на нижние кнопки (тут вставляй свои ссылки)
                elif text_received == "📊 Мій прайс-лист":
                    requests.post(url, json={"chat_id": chat_id, "text": "Ось посилання на мій прайс: https://google.com"})
                    
                elif text_received == "📝 Бриф на розробку":
                    requests.post(url, json={"chat_id": chat_id, "text": "Заповнити бриф можна за цим посиланням: https://google.com"})
                    
                elif text_received == "👨‍💻 Написати мені особисто":
                    requests.post(url, json={"chat_id": chat_id, "text": "Пиши напряму сюди: https://t.me/твой_юзернейм"})
                    
                # 3. ЗАЩИТА ОТ СПАМА (если пишут любой текст руками)
                else:
                    requests.post(url, json={"chat_id": chat_id, "text": "Будь ласка, користуйся кнопками внизу екрана 👇"})

        except Exception as e:
            print("Error:", e)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
        return
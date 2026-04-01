import html
import json
import os
from http.server import BaseHTTPRequestHandler

import requests


REQUEST_TIMEOUT_SECONDS = 10
MENU_PRICE = "📊 Мій прайс"
MENU_BRIEF = "📝 Бриф на розробку"
MENU_CONTACT = "💬 Написати напряму"


def _env(name, fallback=""):
    return str(os.environ.get(name, fallback) or "").strip()


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self._send_response(204)

    def do_POST(self):
        token = _env("CLIENT_BOT_TOKEN")
        if not token:
            self._send_response(500, {"error": "Missing CLIENT_BOT_TOKEN."})
            return

        try:
            update = self._load_payload()
        except ValueError as error:
            self._send_response(400, {"error": str(error)})
            return

        message = update.get("message") or {}
        chat = message.get("chat") or {}
        sender = message.get("from") or {}
        chat_id = chat.get("id")
        text_received = str(message.get("text") or "").strip()
        user_name = html.escape(str(sender.get("first_name") or "друже"), quote=False)

        if not chat_id:
            self._send_response(200, {"status": "ignored"})
            return

        price_url = _env("NTVX_PRICE_LIST_URL", "https://t.me/ntvx31")
        brief_url = _env("NTVX_BRIEF_URL", "https://t.me/ntvx31")
        owner_url = _env("NTVX_OWNER_TG_URL", "https://t.me/ntvx31")

        if text_received in ("/start", "/menu"):
            text = (
                f"Вітаю, {user_name}.\n\n"
                "Я бот студії NTVX. Тут можна швидко відкрити прайс, "
                "бриф або перейти в прямий контакт без зайвого пошуку."
            )
            self._send_message(token, chat_id, text, self._keyboard())
        elif text_received == MENU_PRICE:
            self._send_message(token, chat_id, f"Прайс-лист: {price_url}", self._keyboard())
        elif text_received == MENU_BRIEF:
            self._send_message(token, chat_id, f"Бриф на розробку: {brief_url}", self._keyboard())
        elif text_received == MENU_CONTACT:
            self._send_message(token, chat_id, f"Прямий контакт: {owner_url}", self._keyboard())
        else:
            self._send_message(
                token,
                chat_id,
                "Скористайтеся кнопками нижче, щоб швидко отримати потрібний матеріал.",
                self._keyboard(),
            )

        self._send_response(200, {"status": "ok"})

    def _load_payload(self):
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        if content_length <= 0:
            raise ValueError("Empty request body.")

        raw_body = self.rfile.read(content_length)
        try:
            return json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError("Invalid JSON payload.") from error

    def _keyboard(self):
        return {
            "keyboard": [
                [{"text": MENU_PRICE}],
                [{"text": MENU_BRIEF}],
                [{"text": MENU_CONTACT}],
            ],
            "resize_keyboard": True,
            "is_persistent": True,
        }

    def _send_message(self, token, chat_id, text, reply_markup=None):
        payload = {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": True,
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup

        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

    def _send_response(self, status_code, payload=None):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        if payload is not None and status_code != 204:
            self.wfile.write(json.dumps(payload).encode("utf-8"))

import html
import json
import os
from http.server import BaseHTTPRequestHandler

import requests


REQUEST_TIMEOUT_SECONDS = 10

MENU_MATERIALS = "📦 Матеріали"
MENU_PRICE = "📊 Прайс"
MENU_BRIEF = "📝 Бриф"
MENU_CASES = "🧠 Кейси"
MENU_CALL = "📞 Дзвінок"
MENU_CONTACT = "💬 Написати напряму"
MENU_PROCESS = "⚙️ Як працюємо"

ACTION_MENU = "menu"
ACTION_MATERIALS = "materials"
ACTION_PRICE = "price"
ACTION_BRIEF = "brief"
ACTION_CASES = "cases"
ACTION_CALL = "call"
ACTION_CONTACT = "contact"
ACTION_PROCESS = "process"


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

        try:
            self._handle_update(token, update)
        except requests.RequestException:
            self._send_response(502, {"error": "Telegram request failed."})
            return

        self._send_response(200, {"status": "ok"})

    def _handle_update(self, token, update):
        callback = update.get("callback_query")
        message = update.get("message") or (callback.get("message") if callback else {}) or {}
        sender = (
            (update.get("message") or {}).get("from")
            or (callback.get("from") if callback else {})
            or {}
        )
        chat = message.get("chat") or {}
        chat_id = chat.get("id")

        if not chat_id:
            return

        brand_name = _env("NTVX_BRAND_NAME", "NTVX")
        owner_url = _env("NTVX_OWNER_TG_URL", "https://t.me/ntvx31")
        price_url = _env("NTVX_PRICE_LIST_URL", owner_url)
        brief_url = _env("NTVX_BRIEF_URL", owner_url)
        cases_url = _env("NTVX_CASES_URL", owner_url)
        booking_url = _env("NTVX_BOOKING_URL", owner_url)
        site_url = _env("NTVX_SITE_URL", "https://ntvx-studio.vercel.app")
        response_time = _env("NTVX_RESPONSE_TIME", "2 годин")
        materials_payload = _env("NTVX_LANDING_PAYLOAD", "landing_materials")

        ctx = {
            "brand_name": brand_name,
            "owner_url": owner_url,
            "price_url": price_url,
            "brief_url": brief_url,
            "cases_url": cases_url,
            "booking_url": booking_url,
            "site_url": site_url,
            "response_time": response_time,
            "materials_payload": materials_payload,
            "user_name": html.escape(str(sender.get("first_name") or "друже"), quote=False),
        }

        if callback:
            action = str(callback.get("data") or "").strip()
            callback_id = callback.get("id")
            if callback_id:
                self._answer_callback(token, callback_id)
            self._route_action(token, chat_id, action, ctx)
            return

        text_received = str((update.get("message") or {}).get("text") or "").strip()

        if text_received.startswith("/start"):
            payload = text_received[6:].strip()
            self._send_welcome(token, chat_id, ctx, from_landing=(payload == materials_payload))
            return

        if text_received in ("/menu", MENU_MATERIALS):
            self._route_action(token, chat_id, ACTION_MATERIALS, ctx)
        elif text_received in ("/help", MENU_PROCESS):
            self._route_action(token, chat_id, ACTION_PROCESS, ctx)
        elif text_received == MENU_PRICE:
            self._route_action(token, chat_id, ACTION_PRICE, ctx)
        elif text_received == MENU_BRIEF:
            self._route_action(token, chat_id, ACTION_BRIEF, ctx)
        elif text_received == MENU_CASES:
            self._route_action(token, chat_id, ACTION_CASES, ctx)
        elif text_received == MENU_CALL:
            self._route_action(token, chat_id, ACTION_CALL, ctx)
        elif text_received == MENU_CONTACT:
            self._route_action(token, chat_id, ACTION_CONTACT, ctx)
        else:
            self._send_message(
                token,
                chat_id,
                (
                    f"Щоб не губити вас у діалозі, я працюю через короткі сценарії {ctx['brand_name']}.\n\n"
                    "Оберіть потрібний розділ нижче: матеріали, прайс, бриф, кейси, дзвінок або прямий контакт."
                ),
                reply_markup=self._reply_keyboard(),
                inline_markup=self._inline_menu(),
            )

    def _send_welcome(self, token, chat_id, ctx, from_landing=False):
        text = (
            f"Вітаю, {ctx['user_name']}.\n\n"
            f"Я concierge-бот студії {ctx['brand_name']}. Тут можна за 30 секунд отримати "
            "матеріали для запуску: прайс, бриф, кейси та прямий контакт без зайвих повідомлень."
        )

        if from_landing:
            text += (
                "\n\nВи прийшли з лендингу, тому я вже зібрав для вас стартовий пакет. "
                "Натисніть потрібний напрям нижче."
            )

        self._send_message(
            token,
            chat_id,
            text,
            reply_markup=self._reply_keyboard(),
        )

        if from_landing:
            self._route_action(token, chat_id, ACTION_MATERIALS, ctx)
        else:
            self._send_message(
                token,
                chat_id,
                "Швидке меню нижче. Можна відкрити потрібний сценарій в один тап.",
                inline_markup=self._inline_menu(),
            )

    def _route_action(self, token, chat_id, action, ctx):
        if action in ("", ACTION_MENU):
            self._send_message(
                token,
                chat_id,
                "Оберіть потрібний розділ. Я тримаю лише корисні сценарії без зайвого шуму.",
                reply_markup=self._reply_keyboard(),
            )
            self._send_message(
                token,
                chat_id,
                "Швидкі дії:",
                inline_markup=self._inline_menu(),
            )
            return

        if action == ACTION_MATERIALS:
            self._send_message(
                token,
                chat_id,
                (
                    "Ось швидкий пакет матеріалів для старту:\n\n"
                    "1. Прайс і пакети\n"
                    "2. Бриф на запуск\n"
                    "3. Кейси / референси\n"
                    "4. Контакт або бронювання дзвінка"
                ),
                reply_markup=self._reply_keyboard(),
                inline_markup={
                    "inline_keyboard": [
                        [
                            {"text": "Прайс", "callback_data": ACTION_PRICE},
                            {"text": "Бриф", "callback_data": ACTION_BRIEF},
                        ],
                        [
                            {"text": "Кейси", "callback_data": ACTION_CASES},
                            {"text": "Дзвінок", "callback_data": ACTION_CALL},
                        ],
                        [
                            {"text": "Написати напряму", "callback_data": ACTION_CONTACT},
                        ],
                    ]
                },
            )
            return

        if action == ACTION_PRICE:
            self._send_message(
                token,
                chat_id,
                (
                    f"Прайс {ctx['brand_name']}:\n\n"
                    "Тут зібрані пакети, строки, опції по landing page та супровідних рішеннях. "
                    "Після перегляду можна одразу перейти до брифу або забронювати дзвінок."
                ),
                reply_markup=self._reply_keyboard(),
                inline_markup={
                    "inline_keyboard": [
                        [{"text": "Відкрити прайс", "url": ctx["price_url"]}],
                        [
                            {"text": "Бриф", "callback_data": ACTION_BRIEF},
                            {"text": "Дзвінок", "callback_data": ACTION_CALL},
                        ],
                    ]
                },
            )
            return

        if action == ACTION_BRIEF:
            self._send_message(
                token,
                chat_id,
                (
                    "Бриф потрібен, щоб зібрати офер, структуру сторінки та зрозуміти scope до старту.\n\n"
                    "Його можна заповнити в зручному темпі, а після цього я швидко повернуся з наступним кроком."
                ),
                reply_markup=self._reply_keyboard(),
                inline_markup={
                    "inline_keyboard": [
                        [{"text": "Відкрити бриф", "url": ctx["brief_url"]}],
                        [
                            {"text": "Кейси", "callback_data": ACTION_CASES},
                            {"text": "Написати напряму", "callback_data": ACTION_CONTACT},
                        ],
                    ]
                },
            )
            return

        if action == ACTION_CASES:
            self._send_message(
                token,
                chat_id,
                (
                    "Тут можна подивитися приклади, референси або поточну студійну добірку.\n\n"
                    "Якщо потрібен розбір саме під ваш продукт, напишіть напряму й я підберу релевантні приклади."
                ),
                reply_markup=self._reply_keyboard(),
                inline_markup={
                    "inline_keyboard": [
                        [{"text": "Відкрити кейси", "url": ctx["cases_url"]}],
                        [
                            {"text": "Прайс", "callback_data": ACTION_PRICE},
                            {"text": "Контакт", "callback_data": ACTION_CONTACT},
                        ],
                    ]
                },
            )
            return

        if action == ACTION_CALL:
            self._send_message(
                token,
                chat_id,
                (
                    f"Якщо зручніше пройтися по задачі голосом, можна одразу забронювати дзвінок.\n\n"
                    f"Типова відповідь від студії: до {ctx['response_time']} у робочий час."
                ),
                reply_markup=self._reply_keyboard(),
                inline_markup={
                    "inline_keyboard": [
                        [{"text": "Забронювати дзвінок", "url": ctx["booking_url"]}],
                        [
                            {"text": "Бриф", "callback_data": ACTION_BRIEF},
                            {"text": "Контакт", "callback_data": ACTION_CONTACT},
                        ],
                    ]
                },
            )
            return

        if action == ACTION_CONTACT:
            self._send_message(
                token,
                chat_id,
                (
                    "Прямий контакт відкриє діалог без бот-сценарію.\n\n"
                    "Підійде, якщо у вас вже є задача, дедлайн або треба швидко синхронізуватися по бюджету."
                ),
                reply_markup=self._reply_keyboard(),
                inline_markup={
                    "inline_keyboard": [
                        [{"text": "Написати напряму", "url": ctx["owner_url"]}],
                        [
                            {"text": "Прайс", "callback_data": ACTION_PRICE},
                            {"text": "Бриф", "callback_data": ACTION_BRIEF},
                        ],
                    ]
                },
            )
            return

        if action == ACTION_PROCESS:
            self._send_message(
                token,
                chat_id,
                (
                    f"Як ми працюємо в {ctx['brand_name']}:\n\n"
                    "1. Фіксуємо офер і задачу\n"
                    "2. Збираємо структуру та visual direction\n"
                    "3. Робимо landing і lead-flow\n"
                    "4. Тестуємо, запускаємо, підтримуємо контакт\n\n"
                    f"Сайт студії: {ctx['site_url']}"
                ),
                reply_markup=self._reply_keyboard(),
                inline_markup={
                    "inline_keyboard": [
                        [
                            {"text": "Матеріали", "callback_data": ACTION_MATERIALS},
                            {"text": "Написати", "callback_data": ACTION_CONTACT},
                        ]
                    ]
                },
            )
            return

        self._send_message(
            token,
            chat_id,
            "Не знайшов цей сценарій. Повертаю вас у головне меню.",
            reply_markup=self._reply_keyboard(),
        )
        self._send_message(
            token,
            chat_id,
            "Швидкі дії:",
            inline_markup=self._inline_menu(),
        )

    def _reply_keyboard(self):
        return {
            "keyboard": [
                [{"text": MENU_MATERIALS}, {"text": MENU_PRICE}],
                [{"text": MENU_BRIEF}, {"text": MENU_CASES}],
                [{"text": MENU_CALL}, {"text": MENU_CONTACT}],
                [{"text": MENU_PROCESS}],
            ],
            "resize_keyboard": True,
            "is_persistent": True,
        }

    def _inline_menu(self):
        return {
            "inline_keyboard": [
                [
                    {"text": "Матеріали", "callback_data": ACTION_MATERIALS},
                    {"text": "Прайс", "callback_data": ACTION_PRICE},
                ],
                [
                    {"text": "Бриф", "callback_data": ACTION_BRIEF},
                    {"text": "Кейси", "callback_data": ACTION_CASES},
                ],
                [
                    {"text": "Дзвінок", "callback_data": ACTION_CALL},
                    {"text": "Контакт", "callback_data": ACTION_CONTACT},
                ],
            ]
        }

    def _load_payload(self):
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        if content_length <= 0:
            raise ValueError("Empty request body.")

        raw_body = self.rfile.read(content_length)
        try:
            return json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError("Invalid JSON payload.") from error

    def _answer_callback(self, token, callback_id):
        self._post_telegram(
            token,
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id,
            },
        )

    def _send_message(self, token, chat_id, text, reply_markup=None, inline_markup=None):
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        if inline_markup:
            payload["reply_markup"] = inline_markup
        elif reply_markup:
            payload["reply_markup"] = reply_markup

        self._post_telegram(token, "sendMessage", payload)

    def _post_telegram(self, token, method, payload):
        response = requests.post(
            f"https://api.telegram.org/bot{token}/{method}",
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()

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

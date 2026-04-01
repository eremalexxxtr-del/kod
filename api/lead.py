import html
import json
import os
import time
import uuid
from http.server import BaseHTTPRequestHandler

import requests


PHONE_MIN_DIGITS = 9
PHONE_MAX_DIGITS = 15
NAME_MAX_LENGTH = 80
MESSAGE_MAX_LENGTH = 1200
REQUEST_TIMEOUT_SECONDS = 10
MIN_FORM_FILL_SECONDS = 2


def _clean(value):
    return str(value or "").strip()


def _escape(value):
    return html.escape(_clean(value), quote=False)


def _normalize_multiline(value):
    return _escape(value).replace("\r\n", "\n").replace("\r", "\n")


def _is_valid_contact(value):
    if value.startswith("@"):
        username = value[1:]
        if len(username) < 4 or len(username) > 32:
            return False
        return all(char.isalnum() or char == "_" for char in username)

    digits = "".join(char for char in value if char.isdigit())
    return PHONE_MIN_DIGITS <= len(digits) <= PHONE_MAX_DIGITS


def _safe_int(value):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _format_duration(seconds):
    if seconds is None or seconds < 0:
        return ""

    minutes, remainder = divmod(int(seconds), 60)
    if minutes:
        return f"{minutes} хв {remainder} с"
    return f"{remainder} с"


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self._send_response(204)

    def do_POST(self):
        try:
            payload = self._load_payload()
        except ValueError as error:
            self._send_response(400, {"error": str(error)})
            return

        if _clean(payload.get("website")):
            self._send_response(200, {"status": "ignored"})
            return

        fill_seconds = self._get_fill_seconds(payload)
        if fill_seconds is not None and fill_seconds < MIN_FORM_FILL_SECONDS:
            self._send_response(200, {"status": "ignored"})
            return

        field_errors = self._validate(payload)
        if field_errors:
            self._send_response(422, {"error": "Validation failed.", "fields": field_errors})
            return

        token = _clean(os.environ.get("TELEGRAM_BOT_TOKEN"))
        chat_id = _clean(os.environ.get("TELEGRAM_CHAT_ID"))
        if not token or not chat_id:
            self._send_response(500, {"error": "Server config error."})
            return

        lead_id = uuid.uuid4().hex[:10].upper()
        telegram_payload = {
            "chat_id": chat_id,
            "text": self._build_message(payload, lead_id, fill_seconds),
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        message_thread_id = _safe_int(os.environ.get("TELEGRAM_MESSAGE_THREAD_ID"))
        if message_thread_id:
            telegram_payload["message_thread_id"] = message_thread_id

        try:
            response = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json=telegram_payload,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.RequestException:
            self._send_response(502, {"error": "Lead delivery failed.", "leadId": lead_id})
            return

        if response.ok:
            self._send_response(200, {"status": "success", "leadId": lead_id})
            return

        self._send_response(502, {"error": "Telegram API error.", "leadId": lead_id})

    def _load_payload(self):
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        if content_length <= 0:
            raise ValueError("Empty request body.")

        raw_body = self.rfile.read(content_length)
        try:
            return json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError("Invalid JSON payload.") from error

    def _get_fill_seconds(self, payload):
        started_at = _safe_int(payload.get("started_at"))
        if not started_at:
            return None

        now_ms = int(time.time() * 1000)
        elapsed_ms = now_ms - started_at
        if elapsed_ms < 0:
            return None
        return elapsed_ms / 1000

    def _validate(self, payload):
        name = _clean(payload.get("name"))
        contact = _clean(payload.get("contact"))
        message = _clean(payload.get("message"))

        errors = {}

        if len(name) < 2:
            errors["name"] = "Вкажіть ім'я довжиною від 2 символів."
        elif len(name) > NAME_MAX_LENGTH:
            errors["name"] = "Ім'я не може бути довшим за 80 символів."

        if not contact:
            errors["contact"] = "Вкажіть телефон або Telegram."
        elif not _is_valid_contact(contact):
            errors["contact"] = "Вкажіть коректний телефон або Telegram username."

        if len(message) > MESSAGE_MAX_LENGTH:
            errors["message"] = "Опис задачі занадто довгий."

        return errors

    def _build_message(self, payload, lead_id, fill_seconds):
        need_bot = "Так, потрібен bot flow" if payload.get("need_bot") else "Ні, тільки landing"
        source = _escape(payload.get("source") or "landing")
        submitted_at = _escape(payload.get("submitted_at"))
        fill_time = _format_duration(fill_seconds)

        lines = [
            "🔥 <b>NTVX | Новий лід</b>",
            "",
            f"🆔 <b>ID:</b> <code>{lead_id}</code>",
            f"👤 <b>Ім'я:</b> {_escape(payload.get('name'))}",
            f"📞 <b>Контакт:</b> {_escape(payload.get('contact'))}",
            f"🧩 <b>Комплектація:</b> {need_bot}",
            f"🏷 <b>Джерело:</b> {source}",
        ]

        if submitted_at:
            lines.append(f"🕒 <b>Надіслано:</b> {submitted_at}")

        if fill_time:
            lines.append(f"⏱ <b>Заповнення форми:</b> {fill_time}")

        message = _normalize_multiline(payload.get("message"))
        if message:
            lines.extend(["", "📝 <b>Запит:</b>", message])
        else:
            lines.extend(["", "📝 <b>Запит:</b>", "<i>Клієнт не додав опис задачі.</i>"])

        return "\n".join(lines)

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

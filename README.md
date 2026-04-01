# NTVX Landing

Односторінковий landing із кастомною версткою та двома Python serverless-функціями:

- `/api/lead` приймає ліди з форми та пересилає їх у Telegram
- `/api/client_bot` обробляє webhook Telegram-бота

## Стек

- HTML, CSS, JavaScript без збірки
- Python serverless handlers
- `requests` для викликів Telegram Bot API

## Структура

- `index.html` - лендинг
- `api/lead.py` - прийом лідів із форми
- `api/client_bot.py` - меню Telegram-бота
- `assets/brand/ntvx-logo.png` - логотип NTVX
- `.env.example` - приклад env-перемінних

## Env variables

Для `api/lead.py`:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Для `api/client_bot.py`:

- `CLIENT_BOT_TOKEN`
- `NTVX_PRICE_LIST_URL`
- `NTVX_BRIEF_URL`
- `NTVX_OWNER_TG_URL`

## Що покращено

- бренд оновлено на NTVX
- форма більше не показує фальшивий успіх при падінні API
- є чесний fallback у Telegram з готовим текстом заявки
- додана серверна валідація та екранування HTML перед Telegram
- прибрані заглушки в боті, усе винесено в env

## Примітка

У цьому середовищі Python відсутній у `PATH`, тому локальний запуск або компіляційну перевірку serverless-функцій звідси виконати не вдалося.

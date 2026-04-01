# NTVX Landing

Односторінковий landing із кастомною версткою та двома Python serverless-функціями:

- `/api/lead` приймає ліди з форми та пересилає їх у Telegram
- `/api/client_bot` обробляє Telegram webhook і працює як concierge-бот студії

## Стек

- HTML, CSS, JavaScript без збірки
- Python serverless handlers
- `requests` для викликів Telegram Bot API

## Структура

- `index.html` - лендинг
- `api/lead.py` - прийом лідів із форми
- `api/client_bot.py` - сценарії Telegram-бота
- `assets/brand/ntvx-logo.png` - логотип NTVX
- `.env.example` - приклад env-перемінних

## Env variables

Для `api/lead.py`:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `TELEGRAM_MESSAGE_THREAD_ID` - опціонально, якщо ліди треба складати в окремий topic/forum thread

Для `api/client_bot.py`:

- `CLIENT_BOT_TOKEN`
- `NTVX_BRAND_NAME`
- `NTVX_PRICE_LIST_URL`
- `NTVX_BRIEF_URL`
- `NTVX_CASES_URL`
- `NTVX_BOOKING_URL`
- `NTVX_OWNER_TG_URL`
- `NTVX_SITE_URL`
- `NTVX_RESPONSE_TIME`
- `NTVX_LANDING_PAYLOAD`

## Що вже реалізовано

- бренд NTVX інтегрований у landing і bot-flow
- success-state на сайті веде в Telegram deep link бота
- concierge-бот підтримує `/start`, `/menu`, `/help`, inline menu і сценарії:
  - матеріали
  - прайс
  - бриф
  - кейси
  - дзвінок
  - прямий контакт
- при переході з лендингу бот автоматично відкриває матеріали через payload `landing_materials`
- lead-бот відправляє структуровані повідомлення з `leadId`, джерелом, комплектацією та часом заповнення форми
- є honeypot і базовий антиспам по занадто швидкому заповненню форми

## Порада по продакшену

- після зміни Telegram token оновлюйте env у Vercel
- після оновлення env робіть redeploy
- після нового token заново встановлюйте webhook

## Примітка

У цьому середовищі Python відсутній у `PATH`, тому локальний запуск або компіляційну перевірку serverless-функцій звідси виконати не вдалося.

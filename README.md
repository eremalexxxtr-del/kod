# NTVX Studio Landing

SEO-орієнтований лендинг веб-студії на Next.js App Router з Python serverless-функціями для форми та Telegram-бота.

## Стек

- Next.js 15
- React 19
- TypeScript
- Python serverless handlers
- Telegram Bot API через `requests`

## Структура

- `app/layout.tsx` — глобальна metadata-конфігурація, canonical, OG, robots
- `app/page.tsx` — основний лендинг українською мовою
- `app/globals.css` — стилі сторінки
- `components/lead-form.tsx` — клієнтська форма заявки
- `api/lead.py` — прийом заявок і доставка в Telegram
- `api/client_bot.py` — webhook Telegram-бота
- `public/robots.txt` — правила індексації
- `public/sitemap.xml` — sitemap для домену
- `assets/brand/ntvx-logo.png` — логотип NTVX
- `index.html` — legacy-версія попереднього статичного лендингу

## Команди

```bash
npm install
npm run dev
npm run build
```

## Env variables

Для `api/lead.py`:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `TELEGRAM_MESSAGE_THREAD_ID` — опціонально

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

## Деплой

Проєкт розрахований на Vercel:

- Next.js відповідає за публічний лендинг
- `api/*.py` залишаються serverless-функціями
- після зміни env у Vercel потрібно зробити redeploy
- після зміни Telegram token потрібно повторно встановити webhook

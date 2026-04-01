"use client";

import { useState, type FormEvent } from "react";

type FormValues = {
  name: string;
  contact: string;
  message: string;
  needBot: boolean;
  website: string;
};

type FieldErrors = {
  name?: string;
  contact?: string;
  message?: string;
};

type FormStatus = "idle" | "submitting" | "success" | "fallback" | "error";

const API_ENDPOINT = "/api/lead";
const OWNER_TG_URL = "https://t.me/ntvx31";
const BOT_URL = "https://t.me/DevCraft_Helper_Bot?start=landing_materials";
const EMPTY_LEAD_ID = "—";

const initialValues: FormValues = {
  name: "",
  contact: "",
  message: "",
  needBot: false,
  website: "",
};

function validateName(value: string) {
  const clean = value.trim();
  if (!clean) return "Вкажіть ім'я";
  if (clean.length < 2) return "Мінімум 2 символи";
  if (clean.length > 80) return "Максимум 80 символів";
  return "";
}

function validateContact(value: string) {
  const clean = value.trim();
  if (!clean) return "Вкажіть телефон або Telegram";

  if (clean.startsWith("@")) {
    if (!/^@[A-Za-z0-9_]{4,32}$/.test(clean)) {
      return "Telegram має бути у форматі @username";
    }
    return "";
  }

  const digits = clean.replace(/\D/g, "");
  if (digits.length < 9 || digits.length > 15) {
    return "Вкажіть коректний номер телефону";
  }

  return "";
}

function validateMessage(value: string) {
  if (value.trim().length > 1200) return "Опис занадто довгий";
  return "";
}

function buildFallbackMessage(values: FormValues) {
  const lines = [
    "Новий запит з лендингу NTVX Studio",
    "",
    `Ім'я: ${values.name.trim()}`,
    `Контакт: ${values.contact.trim()}`,
    `Потрібен бот: ${values.needBot ? "Так" : "Ні"}`,
  ];

  if (values.message.trim()) {
    lines.push(`Запит: ${values.message.trim()}`);
  }

  return lines.join("\n");
}

export function LeadForm() {
  const [values, setValues] = useState<FormValues>(initialValues);
  const [errors, setErrors] = useState<FieldErrors>({});
  const [status, setStatus] = useState<FormStatus>("idle");
  const [startedAt, setStartedAt] = useState(Date.now());
  const [leadId, setLeadId] = useState(EMPTY_LEAD_ID);
  const [fallbackMessage, setFallbackMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState(
    "Спробуйте ще раз або напишіть мені в Telegram."
  );
  const [copyState, setCopyState] = useState("Скопіювати текст");

  function updateField<K extends keyof FormValues>(key: K, value: FormValues[K]) {
    setValues((current) => ({ ...current, [key]: value }));

    if (key === "name" || key === "contact" || key === "message") {
      setErrors((current) => ({ ...current, [key]: undefined }));
    }
  }

  function resetForm() {
    setValues(initialValues);
    setErrors({});
    setStatus("idle");
    setStartedAt(Date.now());
    setLeadId(EMPTY_LEAD_ID);
    setFallbackMessage("");
    setErrorMessage("Спробуйте ще раз або напишіть мені в Telegram.");
    setCopyState("Скопіювати текст");
  }

  async function copyFallbackText() {
    try {
      await navigator.clipboard.writeText(fallbackMessage);
      setCopyState("Скопійовано");
    } catch {
      setCopyState("Скопіюйте вручну");
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (status === "submitting") return;

    const nextErrors: FieldErrors = {
      name: validateName(values.name) || undefined,
      contact: validateContact(values.contact) || undefined,
      message: validateMessage(values.message) || undefined,
    };

    const filteredErrors = Object.fromEntries(
      Object.entries(nextErrors).filter(([, value]) => Boolean(value))
    ) as FieldErrors;

    if (Object.keys(filteredErrors).length > 0) {
      setErrors(filteredErrors);
      return;
    }

    if (values.website.trim()) {
      setStatus("success");
      return;
    }

    setStatus("submitting");

    const payload = {
      name: values.name.trim(),
      contact: values.contact.trim(),
      message: values.message.trim(),
      need_bot: values.needBot,
      website: values.website.trim(),
      started_at: startedAt,
      source: "next_landing",
      submitted_at: new Date().toLocaleString("uk-UA", {
        dateStyle: "short",
        timeStyle: "short",
      }),
    };

    try {
      const response = await fetch(API_ENDPOINT, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json().catch(() => ({} as Record<string, unknown>));

      if (response.ok) {
        setLeadId(typeof data.leadId === "string" ? data.leadId : EMPTY_LEAD_ID);
        setStatus("success");
        return;
      }

      if (response.status === 422 && typeof data.fields === "object" && data.fields) {
        const fields = data.fields as FieldErrors;
        setErrors({
          name: fields.name,
          contact: fields.contact,
          message: fields.message,
        });
        setStatus("idle");
        return;
      }

      if (response.status >= 500) {
        setFallbackMessage(buildFallbackMessage(values));
        setStatus("fallback");
        return;
      }

      setErrorMessage(
        typeof data.error === "string"
          ? data.error
          : "Не вдалося надіслати форму. Спробуйте ще раз."
      );
      setStatus("error");
    } catch {
      setFallbackMessage(buildFallbackMessage(values));
      setStatus("fallback");
    }
  }

  if (status === "success") {
    return (
      <div className="form-card form-state">
        <span className="form-state__icon form-state__icon--success">✓</span>
        <h3>Заявку надіслано</h3>
        <p>Дякую. Я перегляну запит і повернуся з відповіддю найближчим часом.</p>
        <p className="form-state__meta">ID заявки: {leadId}</p>
        <div className="form-state__actions">
          <a className="button button-primary" href={BOT_URL} target="_blank" rel="noreferrer">
            Отримати консультацію
          </a>
          <button className="button button-secondary" type="button" onClick={resetForm}>
            Надіслати ще заявку
          </button>
        </div>
      </div>
    );
  }

  if (status === "fallback") {
    return (
      <div className="form-card form-state">
        <span className="form-state__icon form-state__icon--fallback">↗</span>
        <h3>Резервний сценарій</h3>
        <p>
          Сервер тимчасово не відповів, тому я вже підготував текст заявки. Його можна
          одразу надіслати в Telegram.
        </p>
        <textarea className="fallback-box" value={fallbackMessage} readOnly />
        <div className="form-state__actions">
          <a className="button button-primary" href={OWNER_TG_URL} target="_blank" rel="noreferrer">
            Обговорити проєкт
          </a>
          <button className="button button-secondary" type="button" onClick={copyFallbackText}>
            {copyState}
          </button>
          <button className="button button-secondary" type="button" onClick={resetForm}>
            Повернутися до форми
          </button>
        </div>
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className="form-card form-state">
        <span className="form-state__icon form-state__icon--error">!</span>
        <h3>Щось пішло не так</h3>
        <p>{errorMessage}</p>
        <div className="form-state__actions">
          <button className="button button-secondary" type="button" onClick={resetForm}>
            Спробувати ще раз
          </button>
          <a className="button button-primary" href={OWNER_TG_URL} target="_blank" rel="noreferrer">
            Написати в Telegram
          </a>
        </div>
      </div>
    );
  }

  return (
    <form className="form-card" onSubmit={handleSubmit} noValidate>
      <div className="form-row">
        <label className="field">
          <span>Ім&apos;я</span>
          <input
            type="text"
            name="name"
            autoComplete="name"
            value={values.name}
            onChange={(event) => updateField("name", event.target.value)}
            className={errors.name ? "field-input field-input--error" : "field-input"}
            placeholder="Ваше ім'я"
          />
          {errors.name ? <small>{errors.name}</small> : null}
        </label>

        <label className="field">
          <span>Телефон або Telegram</span>
          <input
            type="text"
            name="contact"
            autoComplete="tel"
            value={values.contact}
            onChange={(event) => updateField("contact", event.target.value)}
            className={errors.contact ? "field-input field-input--error" : "field-input"}
            placeholder="+380... або @username"
          />
          {errors.contact ? <small>{errors.contact}</small> : null}
        </label>
      </div>

      <label className="field">
        <span>Коротко про задачу</span>
        <textarea
          name="message"
          rows={5}
          value={values.message}
          onChange={(event) => updateField("message", event.target.value)}
          className={errors.message ? "field-input field-input--error" : "field-input"}
          placeholder="Ніша, продукт, дедлайн, що має робити сайт"
        />
        {errors.message ? <small>{errors.message}</small> : null}
      </label>

      <label className="checkbox">
        <input
          type="checkbox"
          checked={values.needBot}
          onChange={(event) => updateField("needBot", event.target.checked)}
        />
        <span>Потрібна інтеграція з Telegram або ботом</span>
      </label>

      <input
        type="text"
        name="website"
        value={values.website}
        onChange={(event) => updateField("website", event.target.value)}
        tabIndex={-1}
        autoComplete="off"
        className="honeypot"
        aria-hidden="true"
      />

      <div className="form-actions">
        <button className="button button-primary" type="submit" disabled={status === "submitting"}>
          {status === "submitting" ? "Надсилаю..." : "Замовити лендинг"}
        </button>
        <a className="button button-secondary" href={OWNER_TG_URL} target="_blank" rel="noreferrer">
          Отримати консультацію
        </a>
      </div>
    </form>
  );
}

export default LeadForm;

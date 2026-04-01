import Image from "next/image";

import logo from "../assets/brand/ntvx-logo.png";
import LeadForm from "../components/lead-form";

const painPoints = [
  "Немає чіткого офферу",
  "Складна структура",
  "Користувач не розуміє, що робити",
  "Слабкий дизайн",
];

const services = [
  "Аналіз ніші",
  "Структура під конверсію",
  "Сучасний дизайн",
  "Швидка розробка (Next.js)",
];

const projects = [
  {
    title: "WoodMaster",
    niche: "Преміальні меблі з масиву дерева",
    url: "https://woodmaster-lmgu.vercel.app/",
    task: "Показати майстерню як преміальний бренд, підсвітити індивідуальне виробництво та підвести клієнта до консультації.",
    solution:
      "Зібрав візуально дорогий лендинг з акцентом на атмосферу, послуги, галерею робіт та форму заявки для замовлень по Україні.",
  },
  {
    title: "AIR SOFA",
    niche: "Товарний лендинг для надувного крісла",
    url: "https://air-sofa.vercel.app/",
    task: "Швидко продати товар через мобільний трафік, акцію, відгуки, FOMO та сильний call-to-action на замовлення.",
    solution:
      "Побудував e-commerce landing з оффером у першому екрані, пакетами, доказами довіри, відгуками та формою під конверсію.",
  },
  {
    title: "РемМайстер",
    niche: "Сервіс ремонту побутової техніки",
    url: "https://landing-page-remont.vercel.app/",
    task: "Отримувати заявки на терміновий ремонт у Києві та закрити ключові заперечення: швидкість, гарантія, чесна ціна.",
    solution:
      "Зробив SEO-орієнтований service landing з локальним оффером, списком послуг, соцдоказом, контактами та сценарієм виклику майстра.",
  },
  {
    title: "LX-10 TWS",
    niche: "Товарний лендинг для бездротових навушників",
    url: "https://lx10-tws.vercel.app/",
    task: "Подати недорогий гаджет як емоційний техно-продукт і провести користувача до замовлення через Telegram.",
    solution:
      "Зібрав modern product page з яскравим hero, галереєю, блоком переваг, відгуками, таймером і формою замовлення.",
  },
];

const reasons = [
  "Фокус на конверсії, а не просто дизайн",
  "Швидкий запуск без затягування процесу",
  "Індивідуальний підхід до ніші та продукту",
  "Сучасні технології: Next.js / Vercel",
];

const seoText =
  "Розробка лендингів в Україні потрібна бізнесу, який хоче отримувати заявки системно, а не випадково. Продуманий landing page допомагає швидко донести цінність продукту, показати переваги, зняти заперечення та підвести користувача до конкретної дії. Я створюю сучасні лендинги під ключ для компаній з Києва, Львова, Дніпра, Харкова, Одеси та інших міст України. У роботі поєдную структуру під конверсію, сильний текстовий оффер, чистий дизайн, SEO-логіку та швидку розробку на Next.js. У результаті ви отримуєте не просто красивий сайт, а інструмент продажів, який працює на бізнес.";

const schema = {
  "@context": "https://schema.org",
  "@type": "Person",
  name: "NTVX Studio",
  areaServed: "Ukraine",
  service: "Web Development",
  url: "https://ntvx-studio.vercel.app/",
  email: "mailto:ntvxstudio@gmail.com",
  sameAs: ["https://t.me/ntvx31"],
};

export default function HomePage() {
  return (
    <>
      <header className="site-header">
        <div className="container site-header__inner">
          <a className="brand" href="#top">
            <Image
              src={logo}
              alt="Логотип NTVX Studio"
              width={48}
              height={48}
              priority
            />
            <span>NTVX Studio</span>
          </a>

          <nav className="site-nav" aria-label="Основна навігація">
            <a href="#problem">Проблема</a>
            <a href="#projects">Проєкти</a>
            <a href="#why">Чому я</a>
            <a href="#contact">Контакт</a>
          </nav>

          <div className="site-header__actions">
            <a
              className="button button-secondary"
              href="https://t.me/ntvx31"
              target="_blank"
              rel="noreferrer"
            >
              Отримати консультацію
            </a>
            <a className="button button-primary" href="#contact">
              Замовити лендинг
            </a>
          </div>
        </div>
      </header>

      <main id="top">
        <section className="hero section">
          <div className="container hero__grid">
            <div className="hero__content">
              <p className="eyebrow">Лендинги для бізнесу в Україні</p>
              <h1>Розробка лендингів під ключ, які приносять заявки</h1>
              <p className="hero__lead">
                Створюю сучасні сайти для бізнесу з фокусом на результат: більше
                клієнтів, більше продажів
              </p>

              <div className="hero__actions">
                <a className="button button-primary" href="#contact">
                  Отримати безкоштовний розбір
                </a>
                <a
                  className="button button-secondary"
                  href="https://t.me/ntvx31"
                  target="_blank"
                  rel="noreferrer"
                >
                  Обговорити проєкт
                </a>
              </div>

              <p className="hero__trust">Працюю з бізнесами по всій Україні</p>
            </div>

            <aside className="hero-card">
              <div className="hero-card__logo">
                <Image
                  src={logo}
                  alt="Логотип NTVX Studio у першому екрані"
                  width={88}
                  height={88}
                  priority
                />
              </div>
              <p className="hero-card__caption">Структура, текст, дизайн, запуск</p>
              <ul className="hero-card__list">
                <li>Один чіткий оффер замість розмитого меседжу</li>
                <li>Сторінка веде до CTA, а не розпорошує увагу</li>
                <li>Next.js + Vercel для швидкості та SEO</li>
              </ul>
              <div className="hero-card__actions">
                <a className="button button-dark" href="#contact">
                  Замовити лендинг
                </a>
                <a
                  className="text-link"
                  href="https://t.me/ntvx31"
                  target="_blank"
                  rel="noreferrer"
                >
                  Отримати консультацію
                </a>
              </div>
            </aside>
          </div>
        </section>

        <section className="section" id="problem">
          <div className="container">
            <div className="section-heading">
              <p className="eyebrow">Проблема</p>
              <h2>Чому сайт не приносить заявки?</h2>
            </div>

            <div className="cards-grid cards-grid--tight">
              {painPoints.map((item, index) => (
                <article className="info-card" key={item}>
                  <span className="info-card__index">0{index + 1}</span>
                  <p>{item}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section section--alt" id="solution">
          <div className="container">
            <div className="section-heading">
              <p className="eyebrow">Рішення</p>
              <h2>Що я роблю</h2>
            </div>

            <div className="cards-grid">
              {services.map((item) => (
                <article className="service-card" key={item}>
                  <h3>{item}</h3>
                  <p>
                    Кожен етап працює на одну ціль: зробити сторінку зрозумілою,
                    переконливою та зручною для заявки.
                  </p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section" id="projects">
          <div className="container">
            <div className="section-heading">
              <p className="eyebrow">Проєкти</p>
              <h2>Реальні кейси з різних ніш</h2>
              <p className="section-copy">
                Нижче вже не абстрактні приклади, а живі лендинги: преміум-послуги,
                service, товарка та direct-response сторінки під продаж і заявки.
              </p>
            </div>

            <div className="project-grid">
              {projects.map((project) => (
                <article className="project-card" key={project.title}>
                  <div className="project-card__top">
                    <p className="project-card__label">Кейс</p>
                    <h3>{project.title}</h3>
                    <p className="project-card__niche">{project.niche}</p>
                  </div>

                  <div className="project-card__body">
                    <div>
                      <strong>Завдання</strong>
                      <p>{project.task}</p>
                    </div>
                    <div>
                      <strong>Рішення</strong>
                      <p>{project.solution}</p>
                    </div>
                  </div>

                  <div className="project-card__actions">
                    <a
                      className="button button-secondary"
                      href={project.url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Переглянути кейс
                    </a>
                    <a className="text-link" href="#contact">
                      Хочу такий самий
                    </a>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section section--alt" id="why">
          <div className="container">
            <div className="section-heading">
              <p className="eyebrow">Чому я</p>
              <h2>Роблю сайт як інструмент продажів</h2>
            </div>

            <div className="cards-grid">
              {reasons.map((item) => (
                <article className="reason-card" key={item}>
                  <p>{item}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section">
          <div className="container">
            <div className="cta-panel">
              <div>
                <p className="eyebrow">CTA</p>
                <h2>Готові отримати сайт, який приносить клієнтів?</h2>
              </div>
              <a className="button button-primary" href="#contact">
                Обговорити проєкт
              </a>
            </div>
          </div>
        </section>

        <section className="section section--seo" aria-labelledby="seo-title">
          <div className="container seo-block">
            <p className="eyebrow">SEO</p>
            <h2 id="seo-title">Розробка лендингів в Україні</h2>
            <p className="section-copy section-copy--wide">{seoText}</p>
          </div>
        </section>

        <section className="section section--contact" id="contact">
          <div className="container contact-layout">
            <div className="contact-copy">
              <p className="eyebrow">Заявка</p>
              <h2>Обговоримо проєкт і підберемо структуру під вашу нішу</h2>
              <p className="section-copy">
                Якщо потрібен лендинг під рекламу, запуск продукту або лідогенерацію,
                залишайте заявку. Повернуся з безкоштовним розбором і наступними кроками.
              </p>

              <div className="contact-points">
                <div>
                  <span>Формат</span>
                  <strong>Лендинг під ключ</strong>
                </div>
                <div>
                  <span>Технології</span>
                  <strong>Next.js / Vercel</strong>
                </div>
                <div>
                  <span>Контакт</span>
                  <strong>Telegram / Email</strong>
                </div>
              </div>
            </div>

            <LeadForm />
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <div className="container site-footer__inner">
          <div className="site-footer__top">
            <a className="brand brand--footer" href="#top">
              <Image
                src={logo}
                alt="Логотип NTVX Studio у футері"
                width={44}
                height={44}
              />
              <span>NTVX Studio</span>
            </a>

            <p className="site-footer__cities">
              Працюю по всій Україні: Київ, Львів, Дніпро, Харків, Одеса
            </p>
          </div>

          <div className="site-footer__bottom">
            <a href="https://t.me/ntvx31" target="_blank" rel="noreferrer">
              Telegram
            </a>
            <a href="mailto:ntvxstudio@gmail.com">ntvxstudio@gmail.com</a>
          </div>
        </div>
      </footer>

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      />
    </>
  );
}

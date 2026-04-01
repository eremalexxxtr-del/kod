import type { Metadata } from "next";
import { Manrope, Rubik } from "next/font/google";

import "./globals.css";

const manrope = Manrope({
  subsets: ["latin", "cyrillic"],
  variable: "--font-body",
});

const rubik = Rubik({
  subsets: ["latin", "cyrillic"],
  variable: "--font-display",
});

export const metadata: Metadata = {
  metadataBase: new URL("https://ntvx-studio.vercel.app"),
  title: "Розробка лендингів під ключ | Створення сайтів Україна",
  description:
    "Розробка лендингів під ключ для бізнесу в Україні. Сучасні сайти з фокусом на заявки. Отримайте безкоштовний розбір.",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "Розробка лендингів",
    description: "Сайти, які приносять заявки",
    locale: "uk_UA",
    type: "website",
    url: "https://ntvx-studio.vercel.app/",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="uk">
      <body className={`${manrope.variable} ${rubik.variable}`}>{children}</body>
    </html>
  );
}

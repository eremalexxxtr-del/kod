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
    "Розробка продаючих лендингів на Next.js від 3500-6000 грн для перших клієнтів. Швидкість <0.5s, Pagespeed 100/100. Київ, Львів, Дніпро, Харків, Одеса.",
  
  // Google Search Console верификация
  verification: {
    google: "c2y0V7FwebiRt3WYaG7Xn3qYhdAUGUvWlztHu2SPmEE",
  },

  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "Розробка лендингів під ключ | NTVX Studio",
    description: "Продаючі лендинги на Next.js. Від 3500 грн для перших клієнтів.",
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
      <body className={`${manrope.variable} ${rubik.variable}`}>
        {children}
      </body>
    </html>
  );
}
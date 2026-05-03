import type { Metadata } from "next";
import { Inter, Playfair_Display } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

// next/font downloads fonts at build time and serves them from the same
// domain as the app — no third-party request at runtime, no layout shift.
// The `variable` option exposes each font as a CSS custom property so
// Tailwind can reference it (var(--font-inter), var(--font-playfair)).
const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-playfair" });

export const metadata: Metadata = {
  icons: { icon: "/logo.jpeg" },
  title: "CARE — Care, Aid & Rehabilitation in Emergency",
  description:
    "A non-profit organization dedicated to providing emergency medical aid, patient support and rehabilitation services to underserved communities in Pakistan.",
  keywords: ["NGO", "Pakistan", "emergency aid", "rehabilitation", "humanitarian"],
  openGraph: {
    title: "CARE — Care, Aid & Rehabilitation in Emergency",
    description: "Serving Humanity in Times of Need",
    url: "https://care-pk.com", // update to the live domain once deployed
    siteName: "CARE Pakistan",
    locale: "en_US",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  // Font CSS variables are applied at the <html> level so every component
  // in the tree can inherit them through Tailwind's font-sans / font-serif classes.
  return (
    <html lang="en" className={`${inter.variable} ${playfair.variable}`}>
      <body>
        <Navbar />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}

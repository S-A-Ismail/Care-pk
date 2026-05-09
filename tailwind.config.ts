import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // ── Primary action colour ────────────────────────────────
        // Used for CTAs, highlights, icons, borders, and links.
        primary: {
          DEFAULT: "#D32F2F",
          dark: "#B71C1C", // hover / active state
        },

        // ── Dark (headings + footer background) ─────────────────
        // Used only for text headings and the footer bg.
        // Never use as a large section background.
        dark: "#111111",

        // ── Neutral scale ────────────────────────────────────────
        "off-white": "#FAFAFA",   // page sections, alternating bg
        "light-gray": "#E5E7EB", // borders, dividers
        "mid-gray": "#6B7280",   // body text, subtitles

        // ── Soft red tint ────────────────────────────────────────
        // Used for impact strip, bank box, card highlights.
        // Keep white at 70–80 % of UI; use soft-red sparingly.
        "soft-red": "#FDECEC",
      },
      fontFamily: {
        // CSS custom properties injected by next/font in app/layout.tsx.
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        serif: ["var(--font-playfair)", "Georgia", "serif"],
      },
      borderRadius: {
        card: "12px",
      },
      boxShadow: {
        card: "0 4px 12px rgba(0,0,0,0.05)",
        "card-hover": "0 8px 24px rgba(0,0,0,0.10)",
      },
    },
  },
  plugins: [],
};

export default config;

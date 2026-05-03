import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Defining 'green' as an object inside `extend` replaces Tailwind's
        // built-in green scale (green-100, green-200, …) entirely with our
        // custom shades. That's intentional — we never want the default greens
        // on this site. DEFAULT maps to the bare class (bg-green, text-green).
        green: {
          DEFAULT: "#1a3a2a",
          dark: "#0f2318",
          mid: "#1e4530",
          light: "#2a5c3f",
        },
        gold: {
          DEFAULT: "#c9a227",
          light: "#d4b44a",
          dark: "#a88520",
        },
        // Single-value colour (no shades needed) — used as bg-cream, text-cream.
        cream: "#f8f5ef",
      },
      fontFamily: {
        // CSS custom properties injected by next/font in app/layout.tsx.
        // Tailwind reads these at runtime via var(), so fonts are never
        // embedded in the CSS bundle — they're fetched from Google CDN once
        // and then cached by the browser / Next.js font optimisation.
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        serif: ["var(--font-playfair)", "Georgia", "serif"],
      },
    },
  },
  plugins: [],
};

export default config;

"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { FaChevronLeft, FaChevronRight, FaHeart, FaUsers } from "react-icons/fa";

// IMPORTANT: Tailwind's CSS purge scans source files for class strings at
// build time. If you construct a class name dynamically (e.g. `bg-${slide.color}`)
// Tailwind won't include it in the bundle. All three bg- classes must appear
// as complete strings here so they're always included.
const slides = [
  {
    heading: "Serving Humanity",
    subheading: "in Times of Need",
    body: "CARE is a non-profit organization dedicated to providing emergency medical aid, patient support and rehabilitation services to the underserved communities.",
    bg: "bg-dark",
  },
  {
    heading: "Emergency Aid",
    subheading: "When Every Second Counts",
    body: "Our rapid response teams are on the ground 24/7, delivering life-saving medical assistance to those who need it most.",
    bg: "bg-primary",
  },
  {
    heading: "Rebuilding Lives",
    subheading: "Through Rehabilitation",
    body: "We walk alongside patients through their recovery journey — providing emotional, physical and financial support every step of the way.",
    bg: "bg-primary-dark",
  },
];

export default function Hero() {
  const [current, setCurrent] = useState(0);

  // Auto-advance every 5 seconds. The cleanup function clears the interval
  // when the component unmounts to prevent a state update on an unmounted component.
  useEffect(() => {
    const timer = setInterval(() => setCurrent((c) => (c + 1) % slides.length), 5000);
    return () => clearInterval(timer);
  }, []);

  const prev = () => setCurrent((c) => (c - 1 + slides.length) % slides.length);
  const next = () => setCurrent((c) => (c + 1) % slides.length);

  return (
    <section className={`relative min-h-[580px] flex items-center transition-colors duration-700 ${slides[current].bg}`}>
      {/* Semi-transparent overlay darkens the bg colour for better text contrast */}
      <div className="absolute inset-0 bg-black/30" />

      <div className="relative z-10 max-w-7xl mx-auto px-4 w-full py-20">
        <div className="max-w-xl">
          <p className="text-primary uppercase tracking-widest text-sm font-semibold mb-3">
            Care, Aid & Rehabilitation in Emergency
          </p>
          <h1 className="text-white text-5xl md:text-6xl font-serif leading-tight mb-2">
            {slides[current].heading}
          </h1>
          <h2 className="text-white/90 text-4xl md:text-5xl font-serif italic mb-6">
            {slides[current].subheading}
          </h2>
          <p className="text-white/80 text-lg leading-relaxed mb-8 max-w-md">
            {slides[current].body}
          </p>
          <div className="flex flex-wrap gap-4">
            <Link href="/donate" className="btn-primary flex items-center gap-2">
              <FaHeart /> Donate Now
            </Link>
            <Link href="/join-us" className="btn-outline-white flex items-center gap-2">
              <FaUsers /> Join Our Mission
            </Link>
          </div>
        </div>
      </div>

      {/* Arrow buttons sit outside the content div so they always align to the
          vertical centre of the full hero section, not just the text column. */}
      <button onClick={prev} className="absolute left-4 top-1/2 -translate-y-1/2 z-20 bg-black/30 hover:bg-black/50 text-white p-3 transition-colors" aria-label="Previous slide">
        <FaChevronLeft />
      </button>
      <button onClick={next} className="absolute right-4 top-1/2 -translate-y-1/2 z-20 bg-black/30 hover:bg-black/50 text-white p-3 transition-colors" aria-label="Next slide">
        <FaChevronRight />
      </button>

      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 flex gap-2">
        {slides.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrent(i)}
            className={`w-3 h-3 rounded-full transition-colors ${i === current ? "bg-primary" : "bg-white/50"}`}
            aria-label={`Go to slide ${i + 1}`}
          />
        ))}
      </div>
    </section>
  );
}

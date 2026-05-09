"use client";

import { useEffect, useRef, useState } from "react";
import { FaUsers, FaHandsHelping, FaClipboardList, FaCalendarAlt } from "react-icons/fa";

const stats = [
  { icon: FaUsers, value: 500, suffix: "+", label: "Patients Supported" },
  { icon: FaHandsHelping, value: 50, suffix: "+", label: "Dedicated Volunteers" },
  { icon: FaClipboardList, value: 20, suffix: "+", label: "Projects Completed" },
  { icon: FaCalendarAlt, value: 3, suffix: "+", label: "Years of Service" },
];

// Counts from 0 to `target` over ~60 increments (about 1.2 s at 20 ms intervals).
// Only starts when `active` becomes true — triggered by the IntersectionObserver below.
function useCounter(target: number, active: boolean) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!active) return;
    let start = 0;
    const step = Math.ceil(target / 60);
    const timer = setInterval(() => {
      start += step;
      if (start >= target) {
        setCount(target);
        clearInterval(timer);
      } else {
        setCount(start);
      }
    }, 20);
    return () => clearInterval(timer);
  }, [target, active]);
  return count;
}

function StatItem({ icon: Icon, value, suffix, label }: (typeof stats)[0]) {
  const ref = useRef<HTMLDivElement>(null);
  // Once true, stays true — counter fires once and stops. It doesn't reset
  // if the user scrolls away and back.
  const [active, setActive] = useState(false);
  const count = useCounter(value, active);

  useEffect(() => {
    // IntersectionObserver fires when at least 50% of the element is visible.
    // This feels more natural than triggering the moment any pixel appears.
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setActive(true); },
      { threshold: 0.5 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div ref={ref} className="flex items-center gap-4 px-8 py-6 border-r border-light-gray last:border-r-0 flex-1 justify-center">
      <Icon className="text-primary text-4xl shrink-0" />
      <div>
        <div className="text-3xl font-bold text-dark">
          {count}{suffix}
        </div>
        <div className="text-mid-gray text-sm">{label}</div>
      </div>
    </div>
  );
}

export default function Stats() {
  return (
    <section className="bg-off-white border-b border-light-gray">
      <div className="max-w-7xl mx-auto flex flex-wrap divide-y md:divide-y-0 divide-light-gray">
        {stats.map((s) => <StatItem key={s.label} {...s} />)}
      </div>
    </section>
  );
}

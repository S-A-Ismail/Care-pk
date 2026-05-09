import type { Metadata } from "next";
import Link from "next/link";
import { FaCalendarAlt, FaMapMarkerAlt, FaClock } from "react-icons/fa";

export const metadata: Metadata = { title: "Events & Workshops | CARE Pakistan" };

const upcoming = [
  {
    day: "25",
    month: "May",
    title: "Health Awareness Workshop",
    location: "Lahore",
    time: "10:00 AM",
    desc: "A free health awareness session covering preventive care, nutrition and hygiene for underserved communities.",
  },
  {
    day: "10",
    month: "Jun",
    title: "Free Medical Camp",
    location: "Faisalabad",
    time: "9:00 AM",
    desc: "General medical consultations, basic diagnostics and medicine distribution at no cost.",
  },
  {
    day: "20",
    month: "Jun",
    title: "Blood Donation Drive",
    location: "Islamabad",
    time: "11:00 AM",
    desc: "Community blood donation drive in partnership with local hospitals. All blood types needed.",
  },
];

const past = [
  { title: "Flood Relief Medical Camp 2024", date: "Sep 2024", location: "Dera Ghazi Khan" },
  { title: "Winter Rehabilitation Drive", date: "Jan 2025", location: "Lahore" },
  { title: "Community Health Fair", date: "Mar 2025", location: "Karachi" },
];

export default function EventsPage() {
  return (
    <>
      <div className="bg-dark text-white py-16 px-4 text-center">
        <h1 className="text-4xl font-serif mb-2">Events & Workshops</h1>
        <p className="text-white/60 text-sm">
          <Link href="/" className="hover:text-primary">Home</Link> / Events
        </p>
      </div>

      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="section-title">Upcoming Events</h2>
          <div className="red-divider" />

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {upcoming.map((e) => (
              <div key={e.title} className="border border-light-gray shadow-card hover:shadow-card-hover transition-shadow rounded-card overflow-hidden">
                <div className="bg-dark text-white text-center py-5">
                  <div className="text-5xl font-bold text-primary">{e.day}</div>
                  <div className="text-sm uppercase tracking-widest text-white/70">{e.month}</div>
                </div>
                <div className="p-6">
                  <h3 className="text-dark font-semibold text-lg mb-3">{e.title}</h3>
                  <div className="flex items-center gap-2 text-mid-gray text-sm mb-1">
                    <FaMapMarkerAlt className="text-primary shrink-0" /> {e.location}
                  </div>
                  <div className="flex items-center gap-2 text-mid-gray text-sm mb-4">
                    <FaClock className="text-primary shrink-0" /> {e.time}
                  </div>
                  <p className="text-mid-gray text-sm leading-relaxed">{e.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 bg-off-white">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="section-title">Past Events</h2>
          <div className="red-divider" />
          <div className="space-y-4 max-w-2xl mx-auto">
            {past.map((e) => (
              <div key={e.title} className="flex items-center gap-4 bg-white p-4 shadow-card rounded-card">
                <FaCalendarAlt className="text-primary text-xl shrink-0" />
                <div>
                  <div className="font-semibold text-dark">{e.title}</div>
                  <div className="text-mid-gray text-sm">{e.date} · {e.location}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}

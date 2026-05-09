import type { Metadata } from "next";
import Link from "next/link";
import { FaAmbulance, FaUserMd, FaHeartbeat, FaHandshake } from "react-icons/fa";
import CallToAction from "@/components/CallToAction";

export const metadata: Metadata = { title: "What We Do | CARE Pakistan" };

const services = [
  {
    id: "emergency",
    icon: FaAmbulance,
    title: "Emergency Aid",
    desc: "Our rapid response teams are on the ground 24/7, providing immediate life-saving medical care to those in critical situations. We operate ambulances and deploy trained paramedics to emergencies across our service areas.",
    achievements: ["200+ emergency calls responded", "24/7 ambulance availability", "Trained paramedic teams"],
  },
  {
    id: "patient",
    icon: FaUserMd,
    title: "Patient Support",
    desc: "Many patients cannot afford the treatments they need. CARE steps in to cover medications, diagnostics, hospital bills and follow-up care — ensuring no one is turned away due to cost.",
    achievements: ["500+ patients supported financially", "Medicine distribution drives", "Hospital bill assistance"],
  },
  {
    id: "rehab",
    icon: FaHeartbeat,
    title: "Rehabilitation",
    desc: "Recovery doesn't end at discharge. Our rehabilitation program provides physiotherapy, counselling, and long-term support to help patients regain independence and a quality life.",
    achievements: ["80+ active rehab patients", "Partnered physiotherapy centers", "Mental health support"],
  },
  {
    id: "outreach",
    icon: FaHandshake,
    title: "Community Outreach",
    desc: "We run free medical camps, health awareness sessions, and hygiene drives in underserved communities — bringing healthcare directly to people who struggle to access it.",
    achievements: ["10+ free medical camps yearly", "Health awareness workshops", "School health programs"],
  },
];

const timeline = [
  { year: "2024", event: "CARE was founded with a mission to help communities in emergency." },
  { year: "2025", event: "Expanded with dedicated medical teams and launched our first ambulance service." },
  { year: "2026", event: "Expansion of programs and community outreach initiatives." },
];

export default function WhatWeDoPage() {
  return (
    <>
      <div className="bg-dark text-white py-16 px-4 text-center">
        <h1 className="text-4xl font-serif mb-2">What We Do</h1>
        <p className="text-white/60 text-sm">
          <Link href="/" className="hover:text-primary">Home</Link> / What We Do
        </p>
      </div>

      {/* Services */}
      {services.map(({ id, icon: Icon, title, desc, achievements }, i) => (
        <section id={id} key={id} className={`py-20 ${i % 2 === 0 ? "bg-white" : "bg-off-white"}`}>
          <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            {i % 2 === 0 ? (
              <>
                <div className="h-72 bg-soft-red flex items-center justify-center text-primary/30 uppercase tracking-widest text-sm rounded-card">
                  Program Photo
                </div>
                <div>
                  <div className="w-14 h-14 bg-soft-red flex items-center justify-center rounded-full mb-4">
                    <Icon className="text-primary text-2xl" />
                  </div>
                  <h2 className="text-3xl font-serif text-dark mb-4">{title}</h2>
                  <p className="text-mid-gray leading-relaxed mb-6">{desc}</p>
                  <ul className="space-y-2">
                    {achievements.map((a) => (
                      <li key={a} className="flex items-center gap-2 text-mid-gray text-sm">
                        <span className="w-2 h-2 bg-primary rounded-full shrink-0" />
                        {a}
                      </li>
                    ))}
                  </ul>
                </div>
              </>
            ) : (
              <>
                <div>
                  <div className="w-14 h-14 bg-soft-red flex items-center justify-center rounded-full mb-4">
                    <Icon className="text-primary text-2xl" />
                  </div>
                  <h2 className="text-3xl font-serif text-dark mb-4">{title}</h2>
                  <p className="text-mid-gray leading-relaxed mb-6">{desc}</p>
                  <ul className="space-y-2">
                    {achievements.map((a) => (
                      <li key={a} className="flex items-center gap-2 text-mid-gray text-sm">
                        <span className="w-2 h-2 bg-primary rounded-full shrink-0" />
                        {a}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="h-72 bg-soft-red flex items-center justify-center text-primary/30 uppercase tracking-widest text-sm rounded-card">
                  Program Photo
                </div>
              </>
            )}
          </div>
        </section>
      ))}

      {/* Timeline */}
      <section className="py-20 bg-dark text-white">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="section-title text-white mb-10">Our Journey</h2>
          <div className="relative border-l-2 border-primary pl-10 space-y-10">
            {timeline.map(({ year, event }) => (
              <div key={year} className="relative">
                <div className="absolute -left-[2.85rem] w-5 h-5 bg-primary rounded-full border-4 border-dark" />
                <div className="text-primary font-bold text-lg mb-1">{year}</div>
                <p className="text-white/70">{event}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <CallToAction />
    </>
  );
}

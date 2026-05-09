import Link from "next/link";
import { FaAmbulance, FaUserMd, FaHeartbeat, FaHandshake } from "react-icons/fa";

const services = [
  {
    icon: FaAmbulance,
    title: "Emergency Aid",
    desc: "Providing immediate medical assistance in critical situations — rapid response, life-saving care.",
    href: "/what-we-do#emergency",
  },
  {
    icon: FaUserMd,
    title: "Patient Support",
    desc: "Supporting patients with treatment, medications and essential needs throughout their care journey.",
    href: "/what-we-do#patient",
  },
  {
    icon: FaHeartbeat,
    title: "Rehabilitation",
    desc: "Helping patients recover and regain a better quality of life through structured rehabilitation programs.",
    href: "/what-we-do#rehab",
  },
  {
    icon: FaHandshake,
    title: "Community Outreach",
    desc: "Health awareness programs and community welfare initiatives that empower underserved communities.",
    href: "/what-we-do#outreach",
  },
];

export default function WhatWeDo() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="section-title">What We Do</h2>
        <p className="section-subtitle">Comprehensive support for a healthier tomorrow</p>
        <div className="red-divider" />

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {services.map(({ icon: Icon, title, desc, href }) => (
            <Link key={title} href={href} className="card group">
              <div className="w-16 h-16 bg-soft-red rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-primary/10 transition-colors">
                <Icon className="text-primary text-3xl" />
              </div>
              <h3 className="text-dark font-semibold text-lg mb-2">{title}</h3>
              <p className="text-mid-gray text-sm leading-relaxed">{desc}</p>
            </Link>
          ))}
        </div>

        <div className="text-center mt-12">
          <Link href="/what-we-do" className="btn-primary inline-block">Explore Our Work</Link>
        </div>
      </div>
    </section>
  );
}

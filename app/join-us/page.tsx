import type { Metadata } from "next";
import Link from "next/link";
import { FaHeart, FaUsers, FaBullhorn } from "react-icons/fa";
import VolunteerForm from "@/components/VolunteerForm";

export const metadata: Metadata = { title: "Join Us | CARE Pakistan" };

export default function JoinUsPage() {
  return (
    <>
      <div className="bg-dark text-white py-16 px-4 text-center">
        <h1 className="text-4xl font-serif mb-2">Join Our Mission</h1>
        <p className="text-white/60 text-sm">
          <Link href="/" className="hover:text-primary">Home</Link> / Join Us
        </p>
      </div>

      {/* Ways to help */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="section-title">How You Can Help</h2>
          <div className="red-divider" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            {[
              { icon: FaUsers, title: "Volunteer", desc: "Give your time and skills. Join our field teams, medical camps, or administrative support." },
              { icon: FaHeart, title: "Donate", desc: "Financial support directly funds patient care, medicines, and operational costs.", link: "/donate" },
              { icon: FaBullhorn, title: "Spread the Word", desc: "Share our mission on social media. Awareness saves lives too." },
            ].map(({ icon: Icon, title, desc, link }) => (
              <div key={title} className="card text-center">
                <div className="w-16 h-16 bg-soft-red rounded-full flex items-center justify-center mx-auto mb-4">
                  <Icon className="text-primary text-3xl" />
                </div>
                <h3 className="text-dark font-semibold text-xl mb-3">{title}</h3>
                <p className="text-mid-gray text-sm leading-relaxed mb-4">{desc}</p>
                {link && <Link href={link} className="btn-primary inline-block text-xs">Donate Now</Link>}
              </div>
            ))}
          </div>

          {/* Volunteer form */}
          <div className="max-w-2xl mx-auto">
            <h2 className="section-title mb-2">Volunteer Application</h2>
            <p className="section-subtitle mb-8">Fill in the form below and our team will be in touch.</p>
            <VolunteerForm />
          </div>
        </div>
      </section>
    </>
  );
}

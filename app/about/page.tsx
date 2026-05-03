import type { Metadata } from "next";
import Link from "next/link";
import CallToAction from "@/components/CallToAction";

export const metadata: Metadata = { title: "About Us | CARE Pakistan" };

export default function AboutPage() {
  return (
    <>
      {/* Page header */}
      <div className="bg-green text-white py-16 px-4 text-center">
        <h1 className="text-4xl font-serif mb-2">About Us</h1>
        <p className="text-white/60 text-sm">
          <Link href="/" className="hover:text-gold">Home</Link> / About Us
        </p>
      </div>

      {/* About content */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Image placeholder */}
          <div className="h-96 bg-green/10 flex items-center justify-center text-green/30 uppercase tracking-widest text-sm">
            Organization Photo
          </div>

          <div>
            <p className="text-gold uppercase tracking-widest text-sm font-semibold mb-3">About CARE</p>
            <h2 className="text-3xl font-serif text-green mb-6 leading-snug">
              Care, Aid & Rehabilitation in Emergency
            </h2>
            <p className="text-gray-600 leading-relaxed mb-4">
              CARE (Care, Aid & Rehabilitation in Emergency) is a non-profit organization committed to providing immediate medical assistance, patient support, and long-term rehabilitation services to underserved communities across Pakistan.
            </p>
            <p className="text-gray-600 leading-relaxed mb-4">
              Founded with the mission to serve the most vulnerable, CARE has grown into a trusted humanitarian organization — running free medical camps, operating ambulance services, and funding treatment for those who cannot afford care.
            </p>
            <p className="text-gray-600 leading-relaxed mb-8">
              Our mission is to be brave, restore dignity and healing, and ensure that no person is denied care due to financial hardship.
            </p>
            <Link href="/what-we-do" className="btn-green inline-block">Our Mission</Link>
          </div>
        </div>
      </section>

      {/* Mission & Vision */}
      <section id="mission" className="py-20 bg-cream">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                title: "Our Mission",
                text: "To provide immediate, compassionate medical and rehabilitative care to underserved communities, regardless of financial status.",
              },
              {
                title: "Our Vision",
                text: "A Pakistan where every person has access to dignified, quality healthcare in times of crisis and beyond.",
              },
              {
                title: "Our Values",
                text: "Compassion, Transparency, Integrity, Community — the four pillars that guide every decision and action we take.",
              },
            ].map(({ title, text }) => (
              <div key={title} className="bg-white p-8 border-t-4 border-gold text-center shadow-sm">
                <h3 className="text-green font-semibold text-xl mb-4">{title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <CallToAction />
    </>
  );
}

import Link from "next/link";

export default function ImpactSection() {
  return (
    <section className="py-20 bg-cream">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="section-title">Our Impact</h2>
        <p className="section-subtitle">We are proud to make a difference in the lives of so many.</p>
        <div className="gold-divider" />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {/* Placeholder impact cards — replace images with real photos */}
          {[
            { title: "Emergency Response", year: "2024", desc: "Deployed rapid medical teams across 3 cities during monsoon flooding, reaching 200+ families." },
            { title: "Free Medical Camp", year: "2025", desc: "Hosted 10 free medical camps serving 500+ patients with zero cost consultations and medicines." },
            { title: "Rehabilitation Drive", year: "2026", desc: "Ongoing rehabilitation program supporting 80 post-surgery patients with physiotherapy." },
          ].map((item) => (
            <div key={item.title} className="bg-white shadow-sm overflow-hidden group">
              {/* Image placeholder */}
              <div className="h-48 bg-green/10 flex items-center justify-center text-green/30 text-sm uppercase tracking-widest">
                Photo Coming Soon
              </div>
              <div className="p-5">
                <div className="text-gold text-xs font-semibold uppercase tracking-wider mb-1">{item.year}</div>
                <h3 className="text-green font-semibold text-lg mb-2">{item.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center">
          <Link href="/about" className="btn-green inline-block">Read Our Story</Link>
        </div>
      </div>
    </section>
  );
}

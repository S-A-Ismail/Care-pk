import type { Metadata } from "next";
import Link from "next/link";
import { FaQuoteLeft } from "react-icons/fa";

export const metadata: Metadata = { title: "Testimonials | CARE Pakistan" };

const written = [
  {
    quote: "CARE helped us when we had lost all hope. They not only covered my father's treatment but stayed by our side through his recovery. We will never forget their kindness.",
    author: "A Patient's Family",
    location: "Lahore",
  },
  {
    quote: "The free medical camp in our village was life-changing. So many families received diagnoses and medicines they could never have afforded otherwise.",
    author: "Community Member",
    location: "Faisalabad",
  },
  {
    quote: "As a volunteer, I have seen firsthand the impact CARE has. The team is selfless, professional and genuinely committed to serving people.",
    author: "Volunteer",
    location: "Karachi",
  },
  {
    quote: "After my accident, CARE's rehabilitation program helped me walk again. I am forever grateful to every person on the team.",
    author: "Rehab Patient",
    location: "Islamabad",
  },
];

export default function TestimonialsPage() {
  return (
    <>
      <div className="bg-dark text-white py-16 px-4 text-center">
        <h1 className="text-4xl font-serif mb-2">Testimonials</h1>
        <p className="text-white/60 text-sm">
          <Link href="/" className="hover:text-primary">Home</Link> / Testimonials
        </p>
      </div>

      {/* Written testimonials */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="section-title">Written Testimonials</h2>
          <div className="red-divider" />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {written.map(({ quote, author, location }) => (
              <div key={author} className="bg-off-white p-8 relative rounded-card">
                <FaQuoteLeft className="text-primary text-3xl mb-4 opacity-50" />
                <p className="text-mid-gray italic leading-relaxed mb-6">&ldquo;{quote}&rdquo;</p>
                <div className="border-t border-primary/30 pt-4">
                  <div className="font-semibold text-dark">{author}</div>
                  <div className="text-mid-gray text-sm">{location}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Video testimonials */}
      <section className="py-20 bg-off-white">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="section-title">Video Testimonials</h2>
          <div className="red-divider" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-soft-red aspect-video flex items-center justify-center text-primary/30 text-sm uppercase tracking-widest rounded-card">
                Video {i} — Coming Soon
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}

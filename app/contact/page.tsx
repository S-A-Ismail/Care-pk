import type { Metadata } from "next";
import Link from "next/link";
import { FaPhone, FaEnvelope, FaMapMarkerAlt, FaFacebook, FaInstagram } from "react-icons/fa";
import ContactForm from "@/components/ContactForm";

export const metadata: Metadata = { title: "Contact Us | CARE Pakistan" };

export default function ContactPage() {
  return (
    <>
      <div className="bg-dark text-white py-16 px-4 text-center">
        <h1 className="text-4xl font-serif mb-2">Contact Us</h1>
        <p className="text-white/60 text-sm">
          <Link href="/" className="hover:text-primary">Home</Link> / Contact Us
        </p>
      </div>

      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-2 gap-16">

          {/* Info */}
          <div>
            <h2 className="text-3xl font-serif text-dark mb-6">Get In Touch</h2>
            <p className="text-mid-gray leading-relaxed mb-8">
              Have a question, want to volunteer, or need our help? Reach out — our team is available to assist you.
            </p>

            <div className="space-y-5 mb-8">
              <div className="flex gap-4 items-start">
                <div className="w-10 h-10 bg-soft-red rounded-full flex items-center justify-center shrink-0">
                  <FaMapMarkerAlt className="text-primary" />
                </div>
                <div>
                  <div className="font-semibold text-dark">Office Address</div>
                  <div className="text-mid-gray text-sm">115 CARE Office, Johar Town, Lahore, Pakistan</div>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <div className="w-10 h-10 bg-soft-red rounded-full flex items-center justify-center shrink-0">
                  <FaPhone className="text-primary" />
                </div>
                <div>
                  <div className="font-semibold text-dark">Phone</div>
                  <a href="tel:+923001234567" className="text-mid-gray text-sm hover:text-primary transition-colors">+92 300 1234567</a>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <div className="w-10 h-10 bg-soft-red rounded-full flex items-center justify-center shrink-0">
                  <FaEnvelope className="text-primary" />
                </div>
                <div>
                  <div className="font-semibold text-dark">Email</div>
                  <a href="mailto:carejmdc22@gmail.com" className="text-mid-gray text-sm hover:text-primary transition-colors">carejmdc22@gmail.com</a>
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              <a href="https://www.facebook.com/profile.php?id=100084957522371" target="_blank" rel="noreferrer" aria-label="Facebook" className="w-10 h-10 bg-dark flex items-center justify-center text-white hover:bg-primary transition-colors rounded"><FaFacebook /></a>
              <a href="https://www.instagram.com/care_jmdc/" target="_blank" rel="noreferrer" aria-label="Instagram" className="w-10 h-10 bg-dark flex items-center justify-center text-white hover:bg-primary transition-colors rounded"><FaInstagram /></a>
            </div>
          </div>

          {/* Contact form */}
          <div>
            <h2 className="text-3xl font-serif text-dark mb-6">Send Us a Message</h2>
            <ContactForm />
          </div>
        </div>
      </section>

      {/* Map placeholder */}
      <div className="h-64 bg-soft-red flex items-center justify-center text-primary/30 uppercase tracking-widest text-sm">
        Google Maps Embed — Add API key in .env.local
      </div>
    </>
  );
}

import type { Metadata } from "next";
import Link from "next/link";
import { FaPhone, FaEnvelope, FaMapMarkerAlt, FaFacebook, FaInstagram, FaYoutube } from "react-icons/fa";
import ContactForm from "@/components/ContactForm";

export const metadata: Metadata = { title: "Contact Us | CARE Pakistan" };

export default function ContactPage() {
  return (
    <>
      <div className="bg-green text-white py-16 px-4 text-center">
        <h1 className="text-4xl font-serif mb-2">Contact Us</h1>
        <p className="text-white/60 text-sm">
          <Link href="/" className="hover:text-gold">Home</Link> / Contact Us
        </p>
      </div>

      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-2 gap-16">

          {/* Info */}
          <div>
            <h2 className="text-3xl font-serif text-green mb-6">Get In Touch</h2>
            <p className="text-gray-500 leading-relaxed mb-8">
              Have a question, want to volunteer, or need our help? Reach out — our team is available to assist you.
            </p>

            <div className="space-y-5 mb-8">
              <div className="flex gap-4 items-start">
                <div className="w-10 h-10 bg-gold/10 rounded-full flex items-center justify-center shrink-0">
                  <FaMapMarkerAlt className="text-gold" />
                </div>
                <div>
                  <div className="font-semibold text-green">Office Address</div>
                  <div className="text-gray-500 text-sm">115 CARE Office, Johar Town, Lahore, Pakistan</div>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <div className="w-10 h-10 bg-gold/10 rounded-full flex items-center justify-center shrink-0">
                  <FaPhone className="text-gold" />
                </div>
                <div>
                  <div className="font-semibold text-green">Phone</div>
                  <a href="tel:+923001234567" className="text-gray-500 text-sm hover:text-gold transition-colors">+92 300 1234567</a>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <div className="w-10 h-10 bg-gold/10 rounded-full flex items-center justify-center shrink-0">
                  <FaEnvelope className="text-gold" />
                </div>
                <div>
                  <div className="font-semibold text-green">Email</div>
                  <a href="mailto:carejmdc22@gmail.com" className="text-gray-500 text-sm hover:text-gold transition-colors">carejmdc22@gmail.com</a>
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              <a href="https://facebook.com" target="_blank" rel="noreferrer" className="w-10 h-10 bg-green flex items-center justify-center text-white hover:bg-gold hover:text-green-dark transition-colors"><FaFacebook /></a>
              <a href="https://instagram.com" target="_blank" rel="noreferrer" className="w-10 h-10 bg-green flex items-center justify-center text-white hover:bg-gold hover:text-green-dark transition-colors"><FaInstagram /></a>
              <a href="https://youtube.com" target="_blank" rel="noreferrer" className="w-10 h-10 bg-green flex items-center justify-center text-white hover:bg-gold hover:text-green-dark transition-colors"><FaYoutube /></a>
            </div>
          </div>

          {/* Contact form */}
          <div>
            <h2 className="text-3xl font-serif text-green mb-6">Send Us a Message</h2>
            <ContactForm />
          </div>
        </div>
      </section>

      {/* Map placeholder */}
      <div className="h-64 bg-green/10 flex items-center justify-center text-green/30 uppercase tracking-widest text-sm">
        Google Maps Embed — Add API key in .env.local
      </div>
    </>
  );
}

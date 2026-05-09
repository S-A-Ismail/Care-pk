import Link from "next/link";
import Image from "next/image";
import { FaFacebook, FaInstagram } from "react-icons/fa";
import { MdEmail, MdPhone, MdLocationOn } from "react-icons/md";
import NewsletterForm from "@/components/NewsletterForm";

export default function Footer() {
  return (
    <footer className="bg-dark text-white">
      <div className="max-w-7xl mx-auto px-4 py-14 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
        {/* Brand */}
        <div>
          <div className="flex items-center gap-3 mb-4">
            <Image src="/logo.png" alt="CARE Logo" width={40} height={40} />
            <div>
              <div className="text-primary font-bold text-lg">CARE</div>
              <div className="text-white/60 text-[10px] uppercase tracking-wider">Care, Aid & Rehabilitation</div>
            </div>
          </div>
          <p className="text-white/70 text-sm leading-relaxed">
            CARE is dedicated to serving humanity with compassion, transparency and commitment. Providing emergency medical aid to those in need.
          </p>
          <div className="flex gap-3 mt-5">
            <a href="https://www.facebook.com/profile.php?id=100084957522371" target="_blank" rel="noreferrer" aria-label="Facebook" className="text-white/60 hover:text-primary transition-colors"><FaFacebook size={18} /></a>
            <a href="https://www.instagram.com/care_jmdc/" target="_blank" rel="noreferrer" aria-label="Instagram" className="text-white/60 hover:text-primary transition-colors"><FaInstagram size={18} /></a>
          </div>
        </div>

        {/* Quick links */}
        <div>
          <h4 className="text-primary font-semibold uppercase tracking-wider text-sm mb-4">Quick Links</h4>
          <ul className="space-y-2 text-sm text-white/70">
            {[
              { label: "Home", href: "/" },
              { label: "About Us", href: "/about" },
              { label: "Our Team", href: "/team" },
              { label: "What We Do", href: "/what-we-do" },
              { label: "Events", href: "/events" },
              { label: "Testimonials", href: "/testimonials" },
              { label: "Join Us", href: "/join-us" },
              { label: "Donate", href: "/donate" },
              { label: "Contact Us", href: "/contact" },
            ].map(({ label, href }) => (
              <li key={label}>
                <Link href={href} className="hover:text-primary transition-colors">
                  {label}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        {/* Contact */}
        <div>
          <h4 className="text-primary font-semibold uppercase tracking-wider text-sm mb-4">Contact Us</h4>
          <ul className="space-y-3 text-sm text-white/70">
            <li className="flex items-start gap-2">
              <MdLocationOn className="text-primary mt-0.5 shrink-0" size={16} />
              115 CARE Office, Johar Town, Lahore, Pakistan
            </li>
            <li className="flex items-center gap-2">
              <MdPhone className="text-primary shrink-0" size={16} />
              <a href="tel:+923001234567" className="hover:text-primary transition-colors">+92 300 1234567</a>
            </li>
            <li className="flex items-center gap-2">
              <MdEmail className="text-primary shrink-0" size={16} />
              <a href="mailto:carejmdc22@gmail.com" className="hover:text-primary transition-colors">carejmdc22@gmail.com</a>
            </li>
          </ul>
        </div>

        {/* Newsletter */}
        <div>
          <h4 className="text-primary font-semibold uppercase tracking-wider text-sm mb-4">Newsletter</h4>
          <p className="text-white/70 text-sm mb-4">Stay updated with our latest news and events.</p>
          <NewsletterForm />
        </div>
      </div>

      <div className="border-t border-white/10 py-4 text-center text-white/40 text-xs">
        © {new Date().getFullYear()} CARE. All Rights Reserved.
      </div>
    </footer>
  );
}

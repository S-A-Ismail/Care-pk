"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { FaFacebook, FaInstagram, FaBars, FaTimes, FaChevronDown } from "react-icons/fa";
import { MdEmail, MdPhone } from "react-icons/md";

// Single source of truth for all navigation links.
// To add or remove a nav item, edit this array only.
const navLinks = [
  { label: "Home", href: "/" },
  {
    label: "About Us",
    href: "/about",
    children: [
      { label: "Our Story", href: "/about" },
      { label: "Our Mission", href: "/about#mission" },
    ],
  },
  {
    label: "Our Team",
    href: "/team",
    children: [
      { label: "Core Team", href: "/team#core" },
      { label: "Board of Governors", href: "/team#board" },
      { label: "Advisory Board", href: "/team#advisory" },
    ],
  },
  {
    label: "What We Do",
    href: "/what-we-do",
    children: [
      { label: "Emergency Aid", href: "/what-we-do#emergency" },
      { label: "Patient Support", href: "/what-we-do#patient" },
      { label: "Rehabilitation", href: "/what-we-do#rehab" },
      { label: "Community Outreach", href: "/what-we-do#outreach" },
    ],
  },
  { label: "Events", href: "/events" },
  { label: "Testimonials", href: "/testimonials" },
  { label: "Join Us", href: "/join-us" },
  { label: "Contact Us", href: "/contact" },
];

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  // Tracks which dropdown is open by label string.
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);

  return (
    <header className="w-full z-50 sticky top-0 bg-white shadow-sm">
      {/* Top info bar — off-white, contact + socials */}
      <div className="bg-off-white border-b border-light-gray text-sm py-2.5 px-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-8 text-mid-gray">
            <a href="mailto:carejmdc22@gmail.com" className="flex items-center gap-1.5 hover:text-primary transition-colors whitespace-nowrap">
              <MdEmail className="text-primary" size={16} />
              carejmdc22@gmail.com
            </a>
            <a href="tel:+923001234567" className="flex items-center gap-1.5 hover:text-primary transition-colors whitespace-nowrap">
              <MdPhone className="text-primary" size={16} />
              +92 300 1234567
            </a>
          </div>
          <div className="flex items-center gap-4 text-mid-gray">
            <a href="https://www.facebook.com/profile.php?id=100084957522371" target="_blank" rel="noreferrer" aria-label="Facebook" className="hover:text-primary transition-colors">
              <FaFacebook size={18} />
            </a>
            <a href="https://www.instagram.com/care_jmdc/" target="_blank" rel="noreferrer" aria-label="Instagram" className="hover:text-primary transition-colors">
              <FaInstagram size={18} />
            </a>
          </div>
        </div>
      </div>

      {/* Main nav — white background */}
      <nav className="bg-white border-b border-light-gray">
        <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-16">

          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 shrink-0">
            <Image src="/logo.png" alt="CARE Logo" width={40} height={40} />
            <div className="leading-tight">
              <div className="text-primary font-bold text-lg tracking-wide">CARE</div>
              <div className="text-mid-gray text-[10px] uppercase tracking-wider">Care, Aid & Rehabilitation in Emergency</div>
            </div>
          </Link>

          {/* Desktop links */}
          <div className="hidden lg:flex items-center gap-0">
            {navLinks.map((link) =>
              link.children ? (
                // Both the trigger button AND the dropdown panel need onMouseEnter/Leave
                // to prevent the menu closing as the cursor moves between them.
                <div key={link.label} className="relative">
                  <button
                    className="nav-link flex items-center gap-1 px-2.5 py-5 whitespace-nowrap"
                    onMouseEnter={() => setOpenDropdown(link.label)}
                    onMouseLeave={() => setOpenDropdown(null)}
                  >
                    {link.label} <FaChevronDown className="text-[10px]" />
                  </button>
                  <div
                    className={`absolute top-full left-0 bg-white border border-light-gray min-w-48 shadow-lg py-2 rounded-b-lg transition-all duration-150 ${openDropdown === link.label ? "opacity-100 visible" : "opacity-0 invisible"}`}
                    onMouseEnter={() => setOpenDropdown(link.label)}
                    onMouseLeave={() => setOpenDropdown(null)}
                  >
                    {link.children.map((child) => (
                      <Link key={child.label} href={child.href} className="block px-4 py-2 text-mid-gray hover:text-primary hover:bg-off-white text-sm transition-colors">
                        {child.label}
                      </Link>
                    ))}
                  </div>
                </div>
              ) : (
                <Link key={link.label} href={link.href} className="nav-link px-2.5 py-5 whitespace-nowrap">
                  {link.label}
                </Link>
              )
            )}
            <Link href="/donate" className="ml-3 btn-primary whitespace-nowrap">
              Donate Now
            </Link>
          </div>

          {/* Mobile hamburger */}
          <button className="lg:hidden text-dark p-2" onClick={() => setMobileOpen(!mobileOpen)} aria-label="Toggle menu">
            {mobileOpen ? <FaTimes size={20} /> : <FaBars size={20} />}
          </button>
        </div>

        {/* Mobile menu — touch devices don't have hover, so all items are flat */}
        {mobileOpen && (
          <div className="lg:hidden bg-off-white border-t border-light-gray px-4 pb-4 space-y-1">
            {navLinks.map((link) => (
              <div key={link.label}>
                <Link
                  href={link.href}
                  className="block py-2 text-dark hover:text-primary text-sm uppercase tracking-wide transition-colors"
                  onClick={() => setMobileOpen(false)}
                >
                  {link.label}
                </Link>
                {link.children?.map((child) => (
                  <Link
                    key={child.label}
                    href={child.href}
                    className="block py-1 pl-4 text-mid-gray hover:text-primary text-xs transition-colors"
                    onClick={() => setMobileOpen(false)}
                  >
                    {child.label}
                  </Link>
                ))}
              </div>
            ))}
            <Link href="/donate" className="btn-primary inline-block mt-2" onClick={() => setMobileOpen(false)}>
              Donate Now
            </Link>
          </div>
        )}
      </nav>
    </header>
  );
}

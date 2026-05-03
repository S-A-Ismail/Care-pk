"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { FaFacebook, FaInstagram, FaTwitter, FaYoutube, FaLinkedin, FaBars, FaTimes, FaChevronDown } from "react-icons/fa";
import { MdEmail, MdPhone } from "react-icons/md";

// Single source of truth for all navigation links.
// To add or remove a nav item, edit this array only.
// Items with a `children` array get a dropdown on desktop and indented sub-links on mobile.
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
  { label: "Donate", href: "/donate" },
  { label: "Contact Us", href: "/contact" },
];

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  // Tracks which dropdown label is open. Using the label string (not an index)
  // makes it easy to match inside the map without tracking position.
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);

  return (
    <header className="w-full z-50 sticky top-0">
      {/* Top bar — contact info + social icons */}
      <div className="bg-green-dark text-white text-xs py-2 px-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-6">
            <a href="mailto:carejmdc22@gmail.com" className="flex items-center gap-1 hover:text-gold transition-colors">
              <MdEmail className="text-gold" />
              carejmdc22@gmail.com
            </a>
            <a href="tel:+923001234567" className="flex items-center gap-1 hover:text-gold transition-colors">
              <MdPhone className="text-gold" />
              +92 300 1234567
            </a>
          </div>
          <div className="flex items-center gap-3">
            <a href="https://facebook.com" target="_blank" rel="noreferrer" aria-label="Facebook"><FaFacebook className="hover:text-gold transition-colors" /></a>
            <a href="https://instagram.com" target="_blank" rel="noreferrer" aria-label="Instagram"><FaInstagram className="hover:text-gold transition-colors" /></a>
            <a href="https://twitter.com" target="_blank" rel="noreferrer" aria-label="Twitter"><FaTwitter className="hover:text-gold transition-colors" /></a>
            <a href="https://youtube.com" target="_blank" rel="noreferrer" aria-label="YouTube"><FaYoutube className="hover:text-gold transition-colors" /></a>
            <a href="https://linkedin.com" target="_blank" rel="noreferrer" aria-label="LinkedIn"><FaLinkedin className="hover:text-gold transition-colors" /></a>
          </div>
        </div>
      </div>

      {/* Main navigation bar */}
      <nav className="bg-green text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-3 shrink-0">
            <Image src="/logo.png" alt="CARE Logo" width={40} height={40} />
            <div className="leading-tight">
              <div className="text-gold font-bold text-lg tracking-wide">CARE</div>
              <div className="text-white/70 text-[10px] uppercase tracking-wider">Care, Aid & Rehabilitation in Emergency</div>
            </div>
          </Link>

          {/* Desktop links — hidden on mobile */}
          <div className="hidden lg:flex items-center gap-1">
            {navLinks.map((link) =>
              link.children ? (
                // Dropdown: both the trigger button AND the dropdown panel need
                // onMouseEnter/Leave. Without the panel also having these handlers,
                // moving the cursor from the button into the panel briefly leaves
                // both elements, firing onMouseLeave on the button and closing the
                // menu before the cursor reaches a dropdown item.
                <div key={link.label} className="relative group">
                  <button
                    className="nav-link flex items-center gap-1 px-3 py-5"
                    onMouseEnter={() => setOpenDropdown(link.label)}
                    onMouseLeave={() => setOpenDropdown(null)}
                  >
                    {link.label} <FaChevronDown className="text-xs" />
                  </button>
                  <div
                    className={`absolute top-full left-0 bg-green-dark min-w-48 shadow-xl py-2 transition-all duration-150 ${openDropdown === link.label ? "opacity-100 visible" : "opacity-0 invisible"}`}
                    onMouseEnter={() => setOpenDropdown(link.label)}
                    onMouseLeave={() => setOpenDropdown(null)}
                  >
                    {link.children.map((child) => (
                      <Link key={child.label} href={child.href} className="block px-4 py-2 text-white/80 hover:text-gold hover:bg-green text-sm transition-colors">
                        {child.label}
                      </Link>
                    ))}
                  </div>
                </div>
              ) : (
                <Link key={link.label} href={link.href} className="nav-link px-3 py-5">
                  {link.label}
                </Link>
              )
            )}
            <Link href="/donate" className="ml-4 btn-gold">
              Donate Now
            </Link>
          </div>

          {/* Mobile hamburger toggle */}
          <button className="lg:hidden text-white p-2" onClick={() => setMobileOpen(!mobileOpen)} aria-label="Toggle menu">
            {mobileOpen ? <FaTimes size={20} /> : <FaBars size={20} />}
          </button>
        </div>

        {/* Mobile menu — flat list, no hover dropdowns (touch devices don't have hover) */}
        {mobileOpen && (
          <div className="lg:hidden bg-green-dark px-4 pb-4 space-y-1">
            {navLinks.map((link) => (
              <div key={link.label}>
                <Link
                  href={link.href}
                  className="block py-2 text-white/80 hover:text-gold text-sm uppercase tracking-wide transition-colors"
                  onClick={() => setMobileOpen(false)}
                >
                  {link.label}
                </Link>
                {link.children?.map((child) => (
                  <Link
                    key={child.label}
                    href={child.href}
                    className="block py-1 pl-4 text-white/60 hover:text-gold text-xs transition-colors"
                    onClick={() => setMobileOpen(false)}
                  >
                    {child.label}
                  </Link>
                ))}
              </div>
            ))}
            <Link href="/donate" className="btn-gold inline-block mt-2" onClick={() => setMobileOpen(false)}>
              Donate Now
            </Link>
          </div>
        )}
      </nav>
    </header>
  );
}

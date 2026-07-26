#!/usr/bin/env python3
# ============================================================
#  CARE static-site generator (optional dev convenience)
#  ---------------------------------------------------------
#  This script assembles the flat static .html files that make
#  up the site. The OUTPUT (the .html files + assets/) is the
#  actual deliverable and needs NO build step, no Node, no npm
#  to host or view — it works as flat files on any static host
#  or straight from the filesystem (file://).
#
#  The generator exists only so the shared header/footer live
#  in ONE place at authoring time. Edit content here, then run:
#      python _generator/build.py
#  ...to regenerate every page with the header/footer inlined.
# ============================================================
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # -> static-site/

# ---- Site config -------------------------------------------
PHONE = "+92 300 1234567"
PHONE_HREF = "tel:+923001234567"
EMAIL = "carejmdc22@gmail.com"
FB = "https://www.facebook.com/profile.php?id=100084957522371"
IG = "https://www.instagram.com/care_jmdc/"
IG_HANDLE = "@CARE_JMDC"
FORMSPREE = "https://formspree.io/f/YOUR_FORM_ID"  # TODO: replace once account is set up

NAV = [
    ("Home", "index.html"),
    ("About", "about.html"),
    ("Care Programs", "programs.html"),
    ("Impact", "impact.html"),
    ("Get Involved", "get-involved.html"),
    ("Donate", "donate.html"),
    ("News &amp; Events", "news-events.html"),
    ("Resources", "resources.html"),
    ("Contact", "contact.html"),
]

# ---- Icon set (Feather-style stroke SVGs, currentColor) -----
ICONS = {
    "mail": '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "instagram": '<rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/>',
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "menu": '<line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>',
    "x": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "heart": '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>',
    "check": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
    "truck": '<rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "dollar": '<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "home": '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    "bullhorn": '<path d="M3 11l18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "plus-square": '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/>',
    "clipboard": '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>',
    "arrow-right": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    "bank": '<line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/><line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/><line x1="18" y1="18" x2="18" y2="11"/><polygon points="12 2 20 7 4 7"/>',
    "eye": '<path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z"/><circle cx="12" cy="12" r="3"/>',
    "map": '<polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/>',
}


def icon(name, cls=""):
    inner = ICONS.get(name, "")
    c = ("icon " + cls).strip()
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>') % (c, inner)


def todo(text):
    """Visible [TODO] tag + rendered note text (also carries an HTML comment)."""
    return '<!-- TODO --><span class="todo">TODO</span> ' + text


def note(text):
    return '<div class="pending-note">' + todo(text) + '</div>'


# ---- Shared chrome -----------------------------------------
def head(title, description):
    return (
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>' + title + '</title>\n'
        '<meta name="description" content="' + description + '">\n'
        '<link rel="icon" href="assets/logo.png">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&display=swap" rel="stylesheet">\n'
        '<link rel="stylesheet" href="assets/css/styles.css">'
    )


def header(active):
    # Top info bar
    top = (
        '<div class="topbar"><div class="container">'
        '<div class="topbar-contact">'
        '<a href="mailto:' + EMAIL + '">' + icon("mail") + EMAIL + '</a>'
        '<a href="' + PHONE_HREF + '">' + icon("phone") + PHONE + '</a>'
        '</div>'
        '<div class="topbar-social">'
        '<a href="' + FB + '" target="_blank" rel="noreferrer" aria-label="Facebook on Facebook">' + icon("facebook") + '</a>'
        '<a href="' + IG + '" target="_blank" rel="noreferrer" aria-label="CARE on Instagram">' + icon("instagram") + '<span class="handle">' + IG_HANDLE + '</span></a>'
        '</div>'
        '</div></div>'
    )
    # Desktop links
    links = ""
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links += '<a class="nav-link" href="' + href + '"' + cur + '>' + label + '</a>'
    # Mobile links
    mlinks = ""
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        mlinks += '<a href="' + href + '"' + cur + '>' + label + '</a>'

    nav = (
        '<nav class="navbar"><div class="container">'
        '<a class="brand" href="index.html">'
        '<img src="assets/logo.png" alt="CARE logo" width="40" height="40">'
        '<span><span class="brand-name">CARE</span><br><span class="brand-tag">Care, Aid &amp; Rehabilitation in Emergency</span></span>'
        '</a>'
        '<div class="nav-links">' + links + '</div>'
        '<div class="nav-actions">'
        '<button class="icon-btn" data-search-open aria-label="Search the site">' + icon("search") + '</button>'
        '<a class="btn btn-primary" href="donate.html">' + icon("heart") + 'Donate Now</a>'
        '</div>'
        '<div class="mobile-only-actions">'
        '<button class="icon-btn hamburger" data-search-open aria-label="Search the site">' + icon("search") + '</button>'
        '<button class="icon-btn hamburger" data-nav-toggle aria-label="Toggle menu" aria-expanded="false">' + icon("menu") + '</button>'
        '</div>'
        '</div>'
        '<div class="mobile-menu" data-mobile-menu><div class="container">' + mlinks +
        '<a class="btn btn-primary" href="donate.html">Donate Now</a>'
        '</div></div>'
        '</nav>'
    )
    # Hide desktop nav-actions duplicate on mobile handled by CSS; hide mobile actions on desktop:
    search_overlay = (
        '<div class="search-overlay" data-search-overlay>'
        '<div class="search-panel">'
        '<div class="search-panel-head">' + icon("search") +
        '<input type="search" data-search-input placeholder="Search pages…" aria-label="Search pages">'
        '<button class="icon-btn" data-search-close aria-label="Close search">' + icon("x") + '</button>'
        '</div>'
        '<div class="search-results" data-search-results></div>'
        '</div></div>'
    )
    return '<header class="site-header">' + top + nav + '</header>' + search_overlay


def footer():
    links = ""
    for label, href in NAV:
        links += '<li><a href="' + href + '">' + label + '</a></li>'
    return (
        '<footer class="site-footer"><div class="container"><div class="footer-grid">'
        # Brand
        '<div class="footer-brand">'
        '<div class="brand"><img src="assets/logo.png" alt="CARE logo" width="40" height="40">'
        '<span><span class="brand-name">CARE</span><br><span class="brand-tag">Care, Aid &amp; Rehabilitation</span></span></div>'
        '<p>CARE is dedicated to serving humanity with compassion, transparency and commitment — improving access to essential medicines and healthcare for those who need it most.</p>'
        '<div class="footer-social">'
        '<a href="' + FB + '" target="_blank" rel="noreferrer" aria-label="Facebook">' + icon("facebook") + '</a>'
        '<a href="' + IG + '" target="_blank" rel="noreferrer" aria-label="Instagram">' + icon("instagram") + '</a>'
        '</div></div>'
        # Quick links
        '<div class="footer"><h4>Quick Links</h4><ul class="footer-links">' + links + '</ul></div>'
        # Contact
        '<div class="footer"><h4>Contact Us</h4><ul class="footer-contact">'
        '<li>' + icon("pin") +
        # TODO: confirm new office address (\"STH\" floated but unconfirmed) — Lahore address stays for now.
        '<span><!-- TODO: confirm new office address -->115 CARE Office, Johar Town, Lahore, Pakistan</span></li>'
        '<li>' + icon("phone") + '<a href="' + PHONE_HREF + '">' + PHONE + '</a></li>'
        '<li>' + icon("mail") + '<a href="mailto:' + EMAIL + '">' + EMAIL + '</a></li>'
        '</ul></div>'
        # Newsletter
        '<div class="footer"><h4>Newsletter</h4>'
        '<p style="color:rgba(255,255,255,.7);font-size:.9rem;margin-bottom:1rem">Stay updated with our latest news and events.</p>'
        '<form class="newsletter" data-ajax action="' + FORMSPREE + '" method="POST">'
        '<!-- TODO: replace YOUR_FORM_ID with your Formspree (or Mailchimp) form ID -->'
        '<input type="text" name="name" placeholder="Your Name" aria-label="Your name">'
        '<input type="email" name="email" placeholder="Your Email" required aria-label="Your email">'
        '<button type="submit" class="btn btn-primary">Subscribe</button>'
        '<p class="form-status" role="status"></p>'
        '</form></div>'
        '</div></div>'
        '<div class="footer-bottom">&copy; <span data-year>2026</span> CARE. All Rights Reserved.</div>'
        '</footer>'
    )


def scripts():
    return (
        '<script src="assets/js/search-index.js"></script>'
        '<script src="assets/js/search.js"></script>'
        '<script src="assets/js/main.js"></script>'
    )


def page(filename, title, description, active, body):
    doc = (
        '<!doctype html>\n<html lang="en">\n<head>\n' + head(title, description) + '\n</head>\n<body>\n'
        + header(active) + '\n<main>\n' + body + '\n</main>\n' + footer() + '\n' + scripts() + '\n</body>\n</html>\n'
    )
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(doc)


def redirect(filename, target, label):
    doc = (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta http-equiv="refresh" content="0; url=' + target + '">\n'
        '<link rel="canonical" href="' + target + '">\n'
        '<title>Redirecting…</title>\n'
        '<link rel="stylesheet" href="assets/css/styles.css">\n</head>\n'
        '<body><div class="container" style="padding:4rem 1rem;text-align:center">'
        '<p>This page has moved. Redirecting to <a href="' + target + '">' + label + '</a>…</p>'
        '</div></body>\n</html>\n'
    )
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(doc)


def banner(title, crumb):
    return (
        '<section class="page-banner"><div class="container">'
        '<h1>' + title + '</h1>'
        '<p class="breadcrumb"><a href="index.html">Home</a> / ' + crumb + '</p>'
        '</div></section>'
    )


def cta_band():
    return (
        '<section class="cta-band"><div class="container">'
        '<h2>Ready to Make a Difference?</h2>'
        '<p>Your support &mdash; whether through donations, volunteering, or spreading the word &mdash; helps us reach more people in need.</p>'
        '<div class="cta-actions">'
        '<a class="btn btn-dark" href="donate.html">Donate Now</a>'
        '<a class="btn btn-outline-white" href="get-involved.html#volunteer">Volunteer With Us</a>'
        '</div></div></section>'
    )


# ============================================================
#  PAGE CONTENT
# ============================================================

def home():
    what_we_do_cards = [
        ("plus-square", "Essential Medicines &amp; Drug Bank", "Supporting access to prescribed medicines through our Drug Bank for patients who cannot afford them.", "programs.html#drug-bank"),
        ("truck", "Medical Outreach &amp; Health Camps", "Free medical camps and outreach that bring consultations, diagnostics and medicines to underserved communities.", "programs.html#medical-camps"),
        ("book", "Health Education &amp; Prevention", "Preventive health awareness sessions that help communities make informed decisions before problems become serious.", "programs.html#health-awareness"),
        ("activity", "Patient Support Services", "Helping patients continue and complete treatment through practical and financial support.", "programs.html#community-outreach"),
        ("users", "Volunteer &amp; Student Leadership", "Student-led volunteer initiatives that power our programs and develop the next generation of changemakers.", "programs.html#volunteer-initiatives"),
        ("heart", "Emergency Assistance", "Timely support for patients and families facing urgent medical need.", "programs.html#emergency-support"),
    ]
    cards_html = ""
    for ic, title, desc, href in what_we_do_cards:
        cards_html += ('<a class="card" href="' + href + '"><div class="card-icon">' + icon(ic) +
                       '</div><h3>' + title + '</h3><p>' + desc + '</p></a>')

    impact_labels = ["Patients Supported", "Medications Provided", "Medical Camps",
                     "Volunteers", "Partner Hospitals", "Beneficiary Families"]
    matrix = ""
    for lbl in impact_labels:
        matrix += ('<div class="card"><div class="stat-value" style="color:var(--mid-gray);font-size:1.15rem">Coming soon</div>'
                   '<div class="stat-label" style="margin-top:.35rem">' + lbl + '</div>'
                   '<div style="margin-top:.6rem">' + todo("figure pending") + '</div></div>')

    journey = ["Patient Visits Care", "Medical Assessment", "Prescription Verification",
               "Medicine Support", "Follow-up", "Improved Healthcare Outcomes"]
    flow = ""
    for i, step in enumerate(journey):
        flow += ('<div class="flow-step"><span class="num">' + str(i + 1) + '</span><span class="label">' + step + '</span></div>')
        if i < len(journey) - 1:
            flow += '<div class="flow-arrow">' + icon("arrow-right") + '</div>'

    partners = [
        ("book", "Universities"), ("home", "Hospitals"), ("users", "NGOs"),
        ("briefcase", "CSR Partners"), ("heart", "Sponsors"), ("plus-square", "Medical Suppliers"),
        ("shield", "Government Collaborations"),
    ]
    partner_html = ""
    for ic, name in partners:
        partner_html += ('<div class="partner-cat">' + icon(ic) + '<h4>' + name + '</h4>'
                         '<p>Logos coming soon</p></div>')

    transparency = [
        ("file", "Annual Report", "Yearly overview of our work and reach.", "about.html#annual-reports"),
        ("dollar", "Financial Statements", "How funds are received and used.", "about.html#annual-reports"),
        ("book", "Policies", "The standards that guide our work.", "about.html#policies"),
        ("shield", "Safeguarding", "Protecting those we serve.", "safeguarding-policy.html"),
        ("check", "Registration", "Our legal registration details.", "governance.html"),
    ]
    t_html = ""
    for ic, title, desc, href in transparency:
        t_html += ('<a class="t-card" href="' + href + '">' + icon(ic) + '<h4>' + title + '</h4><p>' + desc + '</p></a>')

    testimonials = [
        ("CARE helped us when we had lost all hope. They not only covered my father&rsquo;s treatment but stayed by our side through his recovery. We will never forget their kindness.", "A Patient&rsquo;s Family", "Lahore"),
        ("The free medical camp in our village was life-changing. So many families received diagnoses and medicines they could never have afforded otherwise.", "Community Member", "Faisalabad"),
    ]
    tcards = ""
    for quote, author, loc in testimonials:
        tcards += ('<div class="quote-card"><div class="qmark">&ldquo;</div>'
                   '<blockquote>' + quote + '</blockquote>'
                   '<div class="attr"><div class="name">' + author + '</div><div class="loc">' + loc + '</div></div></div>')

    return (
        # 1. Hero
        '<section class="hero"><div class="container"><div class="hero-inner">'
        '<p class="eyebrow">Care, Aid &amp; Rehabilitation in Emergency</p>'
        '<h1>Healthcare Within Reach</h1>'
        '<p>Improving access to essential medicines, healthcare services, and community support for underserved populations across Pakistan through student leadership, medical partnerships, and compassionate action.</p>'
        '<div class="hero-cta">'
        '<a class="btn btn-primary" href="donate.html">' + icon("heart") + 'Donate Now</a>'
        '<a class="btn btn-outline-white" href="get-involved.html#volunteer">' + icon("users") + 'Join Our Mission</a>'
        '</div></div></div></section>'

        # 2. Impact snapshot teaser
        '<section class="stat-strip"><div class="container">'
        '<div class="stat-item">' + icon("users") + '<div><div class="stat-value">500+</div><div class="stat-label">Patients Supported</div></div></div>'
        '<!-- TODO: confirm volunteer figure with CARE team -->'
        '<div class="stat-item">' + icon("heart") + '<div><div class="stat-value">50+</div><div class="stat-label">Dedicated Volunteers</div></div></div>'
        '</div></section>'

        # 3. Why CARE Exists
        '<section class="section bg-white"><div class="container">'
        '<h2 class="section-title">Why CARE Exists</h2><div class="red-divider"></div>'
        '<div class="prose max-720" style="text-align:center">'
        '<p>Access to healthcare is influenced by more than the availability of hospitals and clinics. For many individuals and families, the cost of medicines, limited health awareness, and barriers to ongoing care can make treatment difficult to complete.</p>'
        '<p>CARE was established to help bridge these gaps by supporting access to essential medicines, promoting preventive health, and working alongside healthcare institutions and community partners to improve health outcomes.</p>'
        '<p>Through collaboration, volunteer engagement, and responsible stewardship of resources, we strive to make healthcare more accessible for those who need it most.</p>'
        '</div>'
        '<div class="grid grid-3 mt-4">'
        '<div class="info-box"><h3>Barriers to Care</h3><p>Patients may face financial or practical challenges that delay or interrupt treatment.</p></div>'
        '<div class="info-box"><h3>Community Health</h3><p>Preventive education and outreach help communities make informed decisions before health problems become more serious.</p></div>'
        '<div class="info-box"><h3>Collaborative Solutions</h3><p>CARE works with healthcare professionals, volunteers, hospitals, and community partners to improve access to essential healthcare services.</p></div>'
        '</div></div></section>'

        # 4. What We Do
        '<section class="section bg-off-white"><div class="container">'
        '<h2 class="section-title">What We Do</h2>'
        '<p class="section-subtitle">Comprehensive support for a healthier tomorrow</p><div class="red-divider"></div>'
        '<div class="grid grid-3">' + cards_html + '</div>'
        '<div class="center-btn"><a class="btn btn-primary" href="programs.html">Explore Our Programs</a></div>'
        '</div></section>'

        # 5. Our Impact matrix
        '<section class="section bg-white"><div class="container">'
        '<h2 class="section-title">Our Impact</h2>'
        '<p class="section-subtitle">Verified figures are being finalised by the CARE team.</p><div class="red-divider"></div>'
        '<!-- TODO: CARE team to supply verified figures for all six -->'
        '<div class="grid grid-3">' + matrix + '</div>'
        '<div class="center-btn"><a class="btn btn-outline" href="impact.html">See Full Impact</a></div>'
        '</div></section>'

        # 6. Patient Journey
        '<section class="section bg-off-white"><div class="container">'
        '<h2 class="section-title">The Patient Journey</h2>'
        '<p class="section-subtitle">How support reaches a patient, step by step</p><div class="red-divider"></div>'
        '<div class="flow">' + flow + '</div>'
        '<div class="grid grid-3 mt-4">'
        '<!-- TODO: photos pending from Adeena -->'
        '<div class="placeholder-box">Volunteers distributing medication &mdash; photo coming soon</div>'
        '<div class="placeholder-box">Prescription verification &mdash; photo coming soon</div>'
        '<div class="placeholder-box">Zakat form being completed &mdash; photo coming soon</div>'
        '</div></div></section>'

        # 7. Partners
        '<section class="section bg-white"><div class="container">'
        '<h2 class="section-title">Our Partners</h2>'
        '<p class="section-subtitle">We work alongside a growing network of partners across sectors.</p><div class="red-divider"></div>'
        '<div class="partner-grid">' + partner_html + '</div>'
        '<p class="text-center mt-3" style="color:var(--mid-gray);font-size:.85rem">' + todo("partner logos and names pending") + '</p>'
        '</div></section>'

        # 8. Transparency
        '<section class="section transparency"><div class="container">'
        '<h2 class="section-title" style="color:#fff">Transparency &amp; Accountability</h2>'
        '<p class="section-subtitle" style="color:rgba(255,255,255,.7)">We are committed to open, responsible stewardship of every contribution.</p>'
        '<div class="red-divider"></div>'
        '<div class="t-grid">' + t_html + '</div>'
        '</div></section>'

        # 9. Testimonials
        '<section class="section bg-off-white"><div class="container">'
        '<h2 class="section-title">Testimonials</h2>'
        '<p class="section-subtitle">Words from the people and communities we serve</p><div class="red-divider"></div>'
        '<div class="grid grid-2">' + tcards + '</div>'
        '<div class="center-btn"><a class="btn btn-outline" href="testimonials.html">Read More Testimonials</a></div>'
        '</div></section>'

        # 10. Closing CTA
        + cta_band()
    )


def about():
    mv = [
        ("Our Mission", "To provide immediate, compassionate medical care and patient support to underserved communities, regardless of financial status."),
        ("Our Vision", "A Pakistan where every person has access to dignified, quality healthcare in times of crisis and beyond."),
        ("Our Values", "Compassion, Transparency, Integrity, Community &mdash; the four pillars that guide every decision and action we take."),
    ]
    mv_html = ""
    for title, text in mv:
        mv_html += '<div class="info-box"><h3>' + title + '</h3><p>' + text + '</p></div>'

    milestones = [
        ("Founding", "CARE was founded with a mission to improve access to healthcare for underserved communities."),
        ("Drug Bank Launched", "Established our Drug Bank to support access to essential, prescribed medicines."),
        ("First Medical Camp", "Held our first free medical camp, bringing consultations and medicines to the community."),
        ("First 1,000 Patients", "Reached an early milestone of supporting our first cohort of patients."),
        ("University Partnerships", "Partnered with universities to power student-led volunteer initiatives."),
        ("Expansion", "Expanded programs and community outreach to serve more people."),
    ]
    tl = ""
    for year, event in milestones:
        tl += ('<div class="timeline-item"><div class="year">' + year + '</div>'
               '<p style="color:var(--mid-gray)">' + event + '</p></div>')

    core = [("Dr. Junaid", "Founder &amp; President"), ("Sana Khan", "General Secretary"), ("Ahmad Raza", "Operations Manager")]
    board = [("Prof. Tariq Mehmood", "Chairman, Board of Governors"), ("Dr. Ayesha Siddiqui", "Board Member"),
             ("Mr. Kamran Ali", "Board Member"), ("Dr. Farrukh Nazar", "Board Member")]
    advisory = [("Dr. Sara Malik", "Medical Advisor"), ("Mr. Bilal Chaudhry", "Legal Advisor"), ("Ms. Hina Javed", "Strategy Advisor")]

    def team_grid(members):
        out = '<div class="team-grid">'
        for name, role in members:
            out += ('<div class="team-member"><div class="team-photo">Photo</div>'
                    '<div class="name">' + name + '</div><div class="role">' + role + '</div></div>')
        return out + '</div>'

    return (
        banner("About Us", "About Us") +

        # Intro / About CARE
        '<section class="section bg-white"><div class="container feature-row">'
        '<div class="feature-media"><div class="placeholder-box" style="min-height:20rem">Organization photo &mdash; coming soon</div></div>'
        '<div class="feature-body"><p class="eyebrow">About CARE</p>'
        '<h2>Care, Aid &amp; Rehabilitation in Emergency</h2>'
        '<p>CARE is a non-profit organization committed to improving access to essential medicines and healthcare for underserved communities across Pakistan &mdash; driven by student leadership, medical partnerships and compassionate action.</p>'
        '<p>We help bridge gaps in care by supporting access to medicines, promoting preventive health, and working alongside hospitals and community partners to improve health outcomes.</p>'
        '<a class="btn btn-primary" href="programs.html">Our Programs</a>'
        '</div></div></section>'

        # Mission & Vision
        '<section id="mission" class="section bg-off-white"><div class="container">'
        '<h2 class="section-title">Mission &amp; Vision</h2><div class="red-divider"></div>'
        '<div class="grid grid-3">' + mv_html + '</div>'
        '</div></section>'

        # Our Story + milestones
        '<section id="story" class="section bg-white"><div class="container">'
        '<h2 class="section-title">Our Story</h2>'
        '<p class="section-subtitle">Founded to make healthcare more accessible &mdash; and growing ever since.</p>'
        '<div class="red-divider"></div>'
        '<div class="prose max-720" style="text-align:center">'
        '<p>CARE began with a simple conviction: that no one should go without essential care because of cost or circumstance. From a small student-led effort, we have grown into an organization running a Drug Bank, medical camps and community outreach.</p>'
        '</div>'
        '<div class="max-720 mt-4"><!-- TODO: confirm founding/launch date with Junaid Bhai -->'
        + note("confirm founding / launch dates and other milestone dates with Junaid Bhai.") +
        '<div class="timeline mt-3">' + tl + '</div></div>'
        '</div></section>'

        # Leadership
        '<section id="leadership" class="section bg-off-white"><div class="container">'
        '<h2 class="section-title">Leadership</h2>'
        '<p class="section-subtitle">The people who guide and carry out our work</p><div class="red-divider"></div>'
        '<h3 style="text-align:center;margin-bottom:1.5rem">Core Team</h3>' + team_grid(core) +
        '<h3 style="text-align:center;margin:3rem 0 1.5rem">Board of Governors</h3>' + team_grid(board) +
        '<h3 style="text-align:center;margin:3rem 0 1.5rem">Advisory Board</h3>' + team_grid(advisory) +
        '<p class="text-center mt-3" style="color:var(--mid-gray);font-size:.85rem">' + todo("confirm names, roles and photos of leadership") + '</p>'
        '</div></section>'

        # Governance & Partners
        '<section id="governance" class="section bg-white"><div class="container max-720" style="text-align:center">'
        '<h2 class="section-title">Governance &amp; Partners</h2><div class="red-divider"></div>'
        '<p style="color:var(--mid-gray);line-height:1.8">CARE is governed by its Board of Governors with support from an Advisory Board, and works in partnership with universities, hospitals, NGOs and CSR partners.</p>'
        '<div class="center-btn"><a class="btn btn-outline" href="governance.html">View Governance</a></div>'
        '</div></section>'

        # Policies
        '<section id="policies" class="section bg-off-white"><div class="container max-720" style="text-align:center">'
        '<h2 class="section-title">Policies</h2><div class="red-divider"></div>'
        '<p style="color:var(--mid-gray);line-height:1.8">Our policies set the standards for how we work and safeguard the people we serve.</p>'
        '<div class="cta-actions mt-3">'
        '<a class="btn btn-outline" href="privacy-policy.html">Privacy Policy</a>'
        '<a class="btn btn-outline" href="safeguarding-policy.html">Safeguarding Policy</a>'
        '<a class="btn btn-outline" href="volunteer-policy.html">Volunteer Policy</a>'
        '</div></div></section>'

        # Annual Reports
        '<section id="annual-reports" class="section bg-white"><div class="container max-720" style="text-align:center">'
        '<h2 class="section-title">Annual Reports</h2><div class="red-divider"></div>'
        '<!-- TODO: reports pending -->'
        + note("Annual Reports and Financial Statements will be published here as downloadable PDFs once available.") +
        '</div></section>'

        + cta_band()
    )


def programs():
    sections = [
        ("drug-bank", "plus-square", "Drug Bank",
         None,  # content pending
         []),
        ("medical-camps", "truck", "Medical Camps",
         "Free medical camps bring general consultations, basic diagnostics and medicine distribution directly to underserved communities at no cost.",
         ["10+ free medical camps yearly", "Consultations, diagnostics and medicines", "Community-based locations"]),
        ("health-awareness", "book", "Health Awareness",
         "Preventive health awareness sessions help communities make informed decisions before health problems become more serious.",
         ["Preventive health education", "Nutrition and hygiene sessions", "School and community programs"]),
        ("community-outreach", "users", "Community Outreach &amp; Patient Support",
         "We support patients in continuing and completing treatment &mdash; covering medicines, diagnostics and follow-up &mdash; and run outreach that brings healthcare closer to people who struggle to access it.",
         ["500+ patients supported financially", "Medicine distribution drives", "Hospital bill assistance"]),
        ("emergency-support", "heart", "Emergency Support",
         "Timely assistance for patients and families facing urgent medical need, so critical care is not delayed by cost.",
         ["Rapid patient assistance", "Support in urgent medical need", "Coordination with hospitals"]),
        ("volunteer-initiatives", "clipboard", "Volunteer Initiatives",
         "Student-led volunteer initiatives power our programs and develop the next generation of changemakers.",
         ["Student leadership", "Medical &amp; paramedic volunteers", "Outreach and administration teams"]),
    ]
    anchors = ('<div class="anchor-nav">'
               + "".join('<a href="#' + sid + '">' + title + '</a>' for sid, _, title, _, _ in sections)
               + '</div>')

    rows = ""
    for i, (sid, ic, title, desc, bullets) in enumerate(sections):
        media = '<div class="feature-media"><div class="placeholder-box" style="min-height:18rem"><!-- TODO: photos pending from Adeena -->Program photo &mdash; coming soon</div></div>'
        if desc is None:
            body = ('<div class="feature-body"><div class="badge">' + icon(ic) + '</div>'
                    '<h2>' + title + '</h2>'
                    '<!-- TODO: content pending, CARE team is writing this one -->'
                    + note("Drug Bank programme copy is being written by the CARE team.") + '</div>')
        else:
            bl = "".join('<li>' + b + '</li>' for b in bullets)
            body = ('<div class="feature-body"><div class="badge">' + icon(ic) + '</div>'
                    '<h2>' + title + '</h2><p>' + desc + '</p>'
                    '<ul class="check-list">' + bl + '</ul></div>')
        reverse = " reverse" if i % 2 == 1 else ""
        bg = "bg-white" if i % 2 == 0 else "bg-off-white"
        inner = (media + body) if i % 2 == 0 else (body + media)
        rows += ('<section id="' + sid + '" class="section ' + bg + '"><div class="container feature-row' + reverse + '">'
                 + inner + '</div></section>')

    return (
        banner("Care Programs", "Care Programs") +
        '<section class="section--tight bg-white"><div class="container">' + anchors + '</div></section>' +
        rows +
        cta_band()
    )


def impact():
    labels = ["Patients Supported", "Medications Provided", "Medical Camps",
              "Volunteers", "Partner Hospitals", "Beneficiary Families"]
    matrix = ""
    for lbl in labels:
        matrix += ('<div class="card"><div class="stat-value" style="color:var(--mid-gray);font-size:1.15rem">Coming soon</div>'
                   '<div class="stat-label" style="margin-top:.35rem">' + lbl + '</div>'
                   '<div style="margin-top:.6rem">' + todo("figure pending") + '</div></div>')
    return (
        banner("Impact", "Impact") +
        '<section class="section bg-white"><div class="container">'
        '<h2 class="section-title">Our Impact in Numbers</h2>'
        '<p class="section-subtitle">Verified figures are being finalised by the CARE team.</p><div class="red-divider"></div>'
        '<!-- TODO: blocked on verified figures, same as homepage -->'
        '<div class="grid grid-3">' + matrix + '</div>'
        '</div></section>'
        '<section class="section bg-off-white"><div class="container">'
        '<h2 class="section-title">Impact Dashboard</h2>'
        '<p class="section-subtitle">Detailed breakdowns by programme, region and year</p><div class="red-divider"></div>'
        + '<div class="max-720">' + note("Impact Dashboard is blocked on verified figures. Once the CARE team supplies the numbers, this area will show breakdowns (e.g. patients by programme, medicines by category, camps by city).") + '</div>'
        '</div></section>'
        + cta_band()
    )


def get_involved():
    paths = [
        ("volunteer", "users", "Volunteer", "Give your time and skills across our field teams, medical camps, or administrative support."),
        ("partner", "link", "Partner", "Organisations and institutions that want to work with us on programmes and outreach."),
        ("corporate", "briefcase", "Corporate", "Companies looking to support our mission through corporate giving or employee engagement."),
        ("csr", "heart", "CSR", "Structured corporate social responsibility collaborations, including the Dearly Loved programme."),
        ("universities", "book", "Universities", "Academic partners for student-led initiatives, research and volunteering."),
        ("funders", "dollar", "Funders", "Grant-makers, donors and philanthropists funding our work at scale."),
    ]
    anchors = ('<div class="anchor-nav">'
               + "".join('<a href="#' + pid + '">' + title + '</a>' for pid, _, title, _ in paths)
               + '</div>')

    def form_block(pid, title, desc, extra_fields):
        return (
            '<section id="' + pid + '" class="section ' + ('bg-white' if paths_index[pid] % 2 == 0 else 'bg-off-white') + '">'
            '<div class="container max-720">'
            '<h2 class="section-title">' + title + '</h2>'
            '<p class="section-subtitle">' + desc + '</p><div class="red-divider"></div>'
            '<form class="form" data-ajax action="' + FORMSPREE + '" method="POST">'
            '<!-- TODO: replace YOUR_FORM_ID with your Formspree form ID -->'
            '<input type="hidden" name="_subject" value="Get Involved: ' + title + '">'
            + extra_fields +
            '<button type="submit" class="btn btn-primary">Submit</button>'
            '<p class="form-status" role="status"></p>'
            '</form></div></section>'
        )

    paths_index = {pid: i for i, (pid, _, _, _) in enumerate(paths)}

    # Volunteer (carry over existing fields incl. Area of Interest)
    volunteer_fields = (
        '<div class="form-row">'
        '<input type="text" name="first_name" placeholder="First Name" required>'
        '<input type="text" name="last_name" placeholder="Last Name" required>'
        '</div>'
        '<input type="email" name="email" placeholder="Email Address" required>'
        '<input type="tel" name="phone" placeholder="Phone Number">'
        '<select name="area_of_interest" aria-label="Area of Interest">'
        '<option value="">Area of Interest</option>'
        '<option>Medical / Paramedic</option>'
        '<option>Community Outreach</option>'
        '<option>Administration</option>'
        '<option>Fundraising</option>'
        '<option>Social Media / Communications</option>'
        '</select>'
        '<textarea name="message" placeholder="Tell us about yourself and why you want to volunteer..."></textarea>'
    )

    def org_fields(org_label, msg_label):
        return (
            '<div class="form-row">'
            '<input type="text" name="name" placeholder="Contact Name" required>'
            '<input type="email" name="email" placeholder="Email Address" required>'
            '</div>'
            '<input type="text" name="organization" placeholder="' + org_label + '" required>'
            '<textarea name="message" placeholder="' + msg_label + '"></textarea>'
        )

    fields_by_id = {
        "volunteer": volunteer_fields,
        "partner": org_fields("Organisation Name", "How would you like to partner with CARE?"),
        "corporate": org_fields("Company Name", "Tell us about your corporate giving or engagement goals."),
        "csr": org_fields("Company / Organisation", "Tell us about your CSR objectives (e.g. Dearly Loved)."),
        "universities": org_fields("University / Institution", "How would your university like to get involved?"),
        "funders": org_fields("Organisation / Foundation", "Tell us about your funding interests and focus areas."),
    }

    blocks = ""
    for pid, ic, title, desc in paths:
        blocks += form_block(pid, title, desc, fields_by_id[pid])

    cards = ""
    for pid, ic, title, desc in paths:
        cards += ('<a class="card" href="#' + pid + '"><div class="card-icon">' + icon(ic) + '</div>'
                  '<h3>' + title + '</h3><p>' + desc + '</p></a>')

    return (
        banner("Get Involved", "Get Involved") +
        '<section class="section bg-white"><div class="container">'
        '<h2 class="section-title">Six Ways to Get Involved</h2>'
        '<p class="section-subtitle">Choose the path that fits you or your organisation.</p><div class="red-divider"></div>'
        + anchors +
        '<div class="grid grid-3">' + cards + '</div>'
        '</div></section>'
        + blocks
    )


def donate():
    bank = [
        ("Account Title", "CARE"),
        ("Account No", "PK46MEZN0001230104370178"),
        ("Bank Name", "Meezan Bank"),
        ("Branch Name", "Johar Town"),
        ("Branch Code", "1234 576 9702"),
        ("IBAN", "PK46MEZN0001234567890178"),
    ]
    bank_html = ""
    for k, v in bank:
        bank_html += '<div class="bank-row"><span class="k">' + k + '</span><span class="v">' + v + '</span></div>'

    ways = [
        ("In-Person Donation", "Visit our office and contribute directly. Our team will issue an official receipt."),
        ("JazzCash / EasyPaisa", "Mobile wallet transfers accepted. Send to 0300-1234567 with reference &lsquo;CARE&rsquo;."),
        ("Standing Collection", "We can collect donations from your home or office. Contact us to arrange."),
    ]
    ways_html = ""
    for t, d in ways:
        ways_html += ('<div class="donate-way"><div><div class="w-title">' + t + '</div>'
                      '<div class="w-desc">' + d + '</div></div></div>')

    amounts = [1000, 2500, 5000, 10000, 25000]
    amt_btns = "".join('<button type="button" class="amount-btn">PKR ' + format(a, ",") + '</button>' for a in amounts)
    amt_btns += '<button type="button" class="amount-btn">Custom</button>'

    return (
        banner("Donate", "Donate") +
        '<section class="section bg-white"><div class="container grid grid-2">'
        # Bank details
        '<div><div style="display:flex;align-items:center;gap:.75rem;margin-bottom:1.5rem">' + icon("bank", "") +
        '<h2 style="font-size:1.6rem">Bank Details</h2></div>'
        '<p style="color:var(--mid-gray);font-size:.9rem;margin-bottom:1.5rem">Transfer directly to our account. All donations are used transparently for patient care and operations.</p>'
        '<div data-bank>' + bank_html + '</div>'
        '<button class="btn btn-primary mt-3" data-download-bank>' + icon("download") + 'Download Bank Details</button>'
        '</div>'
        # Other ways + amounts
        '<div><div style="display:flex;align-items:center;gap:.75rem;margin-bottom:1.5rem">' + icon("dollar") +
        '<h2 style="font-size:1.6rem">Other Ways to Donate</h2></div>'
        + ways_html +
        '<div class="amount-box mt-3" data-amounts>'
        '<div style="color:var(--primary);font-weight:600;margin-bottom:.5rem">Online Payment &mdash; Coming Soon</div>'
        '<div style="color:var(--mid-gray);font-size:.9rem">Secure online donations via card / mobile wallets will be available shortly.</div>'
        '<div class="amount-grid">' + amt_btns + '</div>'
        '</div></div>'
        '</div></section>'
        # Trust statement
        '<section class="section--tight bg-dark"><div class="container max-720" style="text-align:center">'
        '<p style="color:rgba(255,255,255,.85);font-style:italic;font-size:1.05rem">&ldquo;Your support can save lives. All donations are used transparently for patient care and operations. We are proud to share regular impact reports with all donors.&rdquo;</p>'
        '</div></section>'
    )


def news_events():
    upcoming = [
        ("25", "May", "Health Awareness Workshop", "Lahore", "10:00 AM", "A free health awareness session covering preventive care, nutrition and hygiene for underserved communities."),
        ("10", "Jun", "Free Medical Camp", "Faisalabad", "9:00 AM", "General medical consultations, basic diagnostics and medicine distribution at no cost."),
        ("20", "Jun", "Blood Donation Drive", "Islamabad", "11:00 AM", "Community blood donation drive in partnership with local hospitals. All blood types needed."),
    ]
    up_html = ""
    for day, month, title, loc, time, desc in upcoming:
        up_html += (
            '<div class="event-card"><div class="event-date"><div class="day">' + day + '</div>'
            '<div class="month">' + month + '</div></div>'
            '<div class="event-body"><h3>' + title + '</h3>'
            '<div class="event-meta">' + icon("pin") + loc + '</div>'
            '<div class="event-meta">' + icon("clock") + time + '</div>'
            '<p>' + desc + '</p></div></div>'
        )

    past = [
        ("Flood Relief Medical Camp 2024", "Sep 2024", "Dera Ghazi Khan"),
        ("Winter Medical Aid Drive", "Jan 2025", "Lahore"),
        ("Community Health Fair", "Mar 2025", "Karachi"),
    ]
    past_html = ""
    for title, date, loc in past:
        past_html += (
            '<div class="event-card"><div class="placeholder-box" style="min-height:9rem;border-radius:var(--radius) var(--radius) 0 0">'
            '<!-- TODO: photos pending from Adeena -->Photo coming soon</div>'
            '<div class="event-body"><h3>' + title + '</h3>'
            '<div class="event-meta">' + icon("calendar") + date + '</div>'
            '<div class="event-meta">' + icon("pin") + loc + '</div></div></div>'
        )

    news_cats = ["Medical Camps", "Volunteer Activities", "Outreach", "Partnership", "CSR (Dearly Loved)"]
    news_html = ""
    for cat in news_cats:
        news_html += ('<div class="card"><h3>' + cat + '</h3>'
                      '<p>' + todo("latest news content pending") + '</p></div>')

    return (
        banner("News &amp; Events", "News &amp; Events") +
        '<section class="section bg-white"><div class="container" data-tabs>'
        '<div class="tabs" role="tablist">'
        '<button class="tab-btn" data-tab="upcoming" aria-selected="true">Upcoming</button>'
        '<button class="tab-btn" data-tab="past" aria-selected="false">Past Events</button>'
        '<button class="tab-btn" data-tab="news" aria-selected="false">Latest News</button>'
        '</div>'
        # Upcoming
        '<div class="tab-panel active" data-panel="upcoming">'
        '<h2 class="section-title">Upcoming Events</h2><div class="red-divider"></div>'
        '<div class="event-grid">' + up_html + '</div></div>'
        # Past
        '<div class="tab-panel" data-panel="past">'
        '<h2 class="section-title">Past Events</h2><div class="red-divider"></div>'
        '<div class="event-grid">' + past_html + '</div></div>'
        # News
        '<div class="tab-panel" data-panel="news">'
        '<h2 class="section-title">Latest News</h2>'
        '<p class="section-subtitle">Updates across our programmes</p><div class="red-divider"></div>'
        '<div class="grid grid-3">' + news_html + '</div></div>'
        '</div></section>'
    )


def resources():
    return (
        banner("Resources", "Resources") +
        '<section class="section bg-white"><div class="container">'
        '<h2 class="section-title">Dearly Loved (CSR)</h2>'
        '<p class="section-subtitle">Our corporate social responsibility programme</p><div class="red-divider"></div>'
        '<div class="max-720"><!-- TODO: content pending -->'
        + note("Dearly Loved (CSR) programme content is pending.") + '</div>'
        '</div></section>'
        '<section class="section bg-off-white"><div class="container max-720" style="text-align:center">'
        '<h2 class="section-title">Policies &amp; Reports</h2><div class="red-divider"></div>'
        '<p style="color:var(--mid-gray);line-height:1.8">Our policies and annual reports live on the About page.</p>'
        '<div class="cta-actions mt-3">'
        '<a class="btn btn-outline" href="about.html#policies">View Policies</a>'
        '<a class="btn btn-outline" href="about.html#annual-reports">Annual Reports</a>'
        '</div></div></section>'
    )


def governance():
    board = [("Prof. Tariq Mehmood", "Chairman, Board of Governors"), ("Dr. Ayesha Siddiqui", "Board Member"),
             ("Mr. Kamran Ali", "Board Member"), ("Dr. Farrukh Nazar", "Board Member")]
    grid = '<div class="team-grid">'
    for name, role in board:
        grid += ('<div class="team-member"><div class="team-photo">Photo</div>'
                 '<div class="name">' + name + '</div><div class="role">' + role + '</div></div>')
    grid += '</div>'
    return (
        banner("Governance", "Governance") +
        '<section class="section bg-white"><div class="container">'
        '<h2 class="section-title">Governance Structure</h2>'
        '<p class="section-subtitle">How CARE is governed and held accountable</p><div class="red-divider"></div>'
        '<div class="max-720"><!-- TODO: content pending -->'
        + note("Full governance structure and registration details are pending.") + '</div>'
        '<h3 style="text-align:center;margin:3rem 0 1.5rem">Board of Governors</h3>' + grid +
        '<p class="text-center mt-3" style="color:var(--mid-gray);font-size:.85rem">' + todo("confirm board details and photos") + '</p>'
        '</div></section>'
    )


def faq():
    items = [
        ("Where does my money go?",
         'Donations support CARE&rsquo;s programmes &mdash; essential medicines and the Drug Bank, medical camps, patient support, and community outreach. ' + todo("CARE team to confirm the exact allocation breakdown.")),
        ("How secure is it?",
         'Contributions can be made by direct bank transfer to our verified account, and all donations are used transparently for patient care and operations, with regular impact reports shared with donors. ' + todo("confirm security / receipting details.")),
        ("How many people does it reach?",
         'CARE has supported hundreds of patients and dozens of volunteers to date. Verified, up-to-date figures are being finalised &mdash; see the <a href="impact.html">Impact</a> page. ' + todo("verified reach figures pending.")),
        ("[TODO] Confirm the intended 4th FAQ topic",
         '<!-- TODO: confirm the intended 4th FAQ topic --> ' + todo("one FAQ item from the original notes came through unclear &mdash; possibly about registration / legitimacy, or Zakat / tax eligibility (a Zakat form was mentioned elsewhere in the notes). Confirm the intended question and answer.")),
    ]
    acc = '<div class="accordion">'
    for q, a in items:
        acc += ('<div class="acc-item">'
                '<button class="acc-trigger" aria-expanded="false"><span>' + q + '</span>'
                '<span class="chev">' + icon("arrow-right") + '</span></button>'
                '<div class="acc-panel"><div class="acc-panel-inner">' + a + '</div></div></div>')
    acc += '</div>'
    return (
        banner("FAQ", "FAQ") +
        '<section class="section bg-white"><div class="container">'
        '<h2 class="section-title">Frequently Asked Questions</h2><div class="red-divider"></div>'
        + acc +
        '</div></section>'
    )


def policy_page(title, crumb, intro):
    return (
        banner(title, crumb) +
        '<section class="section bg-white"><div class="container max-720">'
        '<h2 class="section-title">' + title + '</h2><div class="red-divider"></div>'
        '<p style="color:var(--mid-gray);line-height:1.8;text-align:center">' + intro + '</p>'
        '<div class="mt-4"><!-- TODO: check whether the org\'s lawyer already drafted these during registration before writing from scratch -->'
        + note("Before writing this policy from scratch, check whether the organisation&rsquo;s lawyer already drafted it during registration. Final policy text is pending.") +
        '</div></div></section>'
    )


def testimonials():
    written = [
        ("CARE helped us when we had lost all hope. They not only covered my father&rsquo;s treatment but stayed by our side through his recovery. We will never forget their kindness.", "A Patient&rsquo;s Family", "Lahore"),
        ("The free medical camp in our village was life-changing. So many families received diagnoses and medicines they could never have afforded otherwise.", "Community Member", "Faisalabad"),
        ("As a volunteer, I have seen firsthand the impact CARE has. The team is selfless, professional and genuinely committed to serving people.", "Volunteer", "Karachi"),
        ("The free medical camp in Islamabad was a blessing. The doctors were thorough and the medicines were provided without any charge.", "Camp Attendee", "Islamabad"),
    ]
    w_html = ""
    for quote, author, loc in written:
        w_html += ('<div class="quote-card"><div class="qmark">&ldquo;</div>'
                   '<blockquote>' + quote + '</blockquote>'
                   '<div class="attr"><div class="name">' + author + '</div><div class="loc">' + loc + '</div></div></div>')
    videos = ""
    for i in range(1, 4):
        videos += '<div class="placeholder-box" style="aspect-ratio:16/9;min-height:0">Video ' + str(i) + ' &mdash; coming soon</div>'
    return (
        banner("Testimonials", "Testimonials") +
        '<section class="section bg-white"><div class="container">'
        '<h2 class="section-title">Written Testimonials</h2><div class="red-divider"></div>'
        '<div class="grid grid-2">' + w_html + '</div></div></section>'
        '<section class="section bg-off-white"><div class="container">'
        '<h2 class="section-title">Video Testimonials</h2><div class="red-divider"></div>'
        '<div class="grid grid-3">' + videos + '</div></div></section>'
    )


def contact():
    return (
        banner("Contact Us", "Contact Us") +
        '<section class="section bg-white"><div class="container grid grid-2">'
        # Info
        '<div><h2 style="font-size:1.8rem;margin-bottom:1rem">Get In Touch</h2>'
        '<p style="color:var(--mid-gray);line-height:1.8;margin-bottom:2rem">Have a question, want to volunteer, or need our help? Reach out &mdash; our team is available to assist you.</p>'
        '<div style="display:flex;flex-direction:column;gap:1.25rem">'
        '<div style="display:flex;gap:1rem"><div class="card-icon" style="width:2.5rem;height:2.5rem;margin:0">' + icon("pin") + '</div>'
        '<div><div style="font-weight:600">Office Address</div>'
        '<!-- TODO: confirm new office address -->'
        '<div style="color:var(--mid-gray);font-size:.9rem">115 CARE Office, Johar Town, Lahore, Pakistan</div>'
        '<div class="mt-1">' + todo("new office address pending confirmation") + '</div></div></div>'
        '<div style="display:flex;gap:1rem"><div class="card-icon" style="width:2.5rem;height:2.5rem;margin:0">' + icon("phone") + '</div>'
        '<div><div style="font-weight:600">Phone</div><a href="' + PHONE_HREF + '" style="color:var(--mid-gray);font-size:.9rem">' + PHONE + '</a></div></div>'
        '<div style="display:flex;gap:1rem"><div class="card-icon" style="width:2.5rem;height:2.5rem;margin:0">' + icon("mail") + '</div>'
        '<div><div style="font-weight:600">Email</div><a href="mailto:' + EMAIL + '" style="color:var(--mid-gray);font-size:.9rem">' + EMAIL + '</a></div></div>'
        '</div>'
        '<div class="footer-social mt-3" style="margin-top:2rem">'
        '<a href="' + FB + '" target="_blank" rel="noreferrer" aria-label="Facebook" style="color:var(--mid-gray)">' + icon("facebook") + '</a>'
        '<a href="' + IG + '" target="_blank" rel="noreferrer" aria-label="Instagram" style="color:var(--mid-gray)">' + icon("instagram") + '</a>'
        '</div></div>'
        # Form
        '<div><h2 style="font-size:1.8rem;margin-bottom:1.5rem">Send Us a Message</h2>'
        '<form class="form" data-ajax action="' + FORMSPREE + '" method="POST">'
        '<!-- TODO: replace YOUR_FORM_ID with your Formspree form ID -->'
        '<div class="form-row">'
        '<input type="text" name="name" placeholder="Your Name" required>'
        '<input type="email" name="email" placeholder="Email Address" required>'
        '</div>'
        '<input type="tel" name="phone" placeholder="Phone Number (optional)">'
        '<input type="text" name="subject" placeholder="Subject" required>'
        '<textarea name="message" placeholder="Your message..." required></textarea>'
        '<button type="submit" class="btn btn-primary">Send Message</button>'
        '<p class="form-status" role="status"></p>'
        '</form></div>'
        '</div></section>'
        # Map placeholder
        '<div class="map-placeholder placeholder-box" style="border-radius:0">'
        '<!-- TODO: Google Maps embed needs an API key; carrying over the placeholder until one is available -->'
        'Google Maps embed &mdash; pending API key</div>'
    )


# ============================================================
#  BUILD
# ============================================================
PAGES = [
    ("index.html", "CARE — Healthcare Within Reach", "Improving access to essential medicines, healthcare services, and community support for underserved populations across Pakistan.", home, "medicines drug bank medical camps volunteers donate emergency"),
    ("about.html", "About Us | CARE Pakistan", "Our mission, story, leadership, governance and policies.", about, "mission vision values story leadership board governors advisory policies annual reports"),
    ("programs.html", "Care Programs | CARE Pakistan", "Drug Bank, medical camps, health awareness, community outreach, emergency support and volunteer initiatives.", programs, "drug bank medical camps health awareness community outreach emergency volunteer"),
    ("impact.html", "Impact | CARE Pakistan", "Our impact in numbers and the impact dashboard.", impact, "impact statistics patients medicines camps volunteers hospitals families dashboard"),
    ("get-involved.html", "Get Involved | CARE Pakistan", "Volunteer, partner, corporate, CSR, universities and funders.", get_involved, "volunteer partner corporate csr universities funders join"),
    ("donate.html", "Donate | CARE Pakistan", "Bank details and other ways to donate to CARE.", donate, "donate bank meezan iban jazzcash easypaisa zakat give"),
    ("news-events.html", "News & Events | CARE Pakistan", "Upcoming and past events, plus the latest news.", news_events, "news events workshops medical camp blood donation past latest"),
    ("resources.html", "Resources | CARE Pakistan", "Dearly Loved (CSR) and links to policies and reports.", resources, "resources dearly loved csr policies reports"),
    ("governance.html", "Governance | CARE Pakistan", "CARE governance structure and board of governors.", governance, "governance board governors registration accountability"),
    ("faq.html", "FAQ | CARE Pakistan", "Frequently asked questions about donations, security and reach.", faq, "faq questions money secure reach zakat registration"),
    ("privacy-policy.html", "Privacy Policy | CARE Pakistan", "How CARE handles personal information.", lambda: policy_page("Privacy Policy", "Privacy Policy", "This policy describes how CARE collects, uses and protects personal information."), "privacy policy data personal information"),
    ("safeguarding-policy.html", "Safeguarding Policy | CARE Pakistan", "How CARE protects the people it serves.", lambda: policy_page("Safeguarding Policy", "Safeguarding Policy", "This policy sets out CARE&rsquo;s commitment to safeguarding the people it serves."), "safeguarding policy protection"),
    ("volunteer-policy.html", "Volunteer Policy | CARE Pakistan", "The standards and expectations for CARE volunteers.", lambda: policy_page("Volunteer Policy", "Volunteer Policy", "This policy sets out the standards, rights and responsibilities for CARE volunteers."), "volunteer policy standards conduct"),
    ("testimonials.html", "Testimonials | CARE Pakistan", "Written and video testimonials from those we serve.", testimonials, "testimonials stories patients volunteers reviews"),
    ("contact.html", "Contact Us | CARE Pakistan", "Get in touch with the CARE team.", contact, "contact address phone email message map"),
]

REDIRECTS = [
    ("team.html", "about.html#leadership", "About &rsaquo; Leadership"),
    ("what-we-do.html", "programs.html", "Care Programs"),
    ("events.html", "news-events.html", "News &amp; Events"),
    ("join-us.html", "get-involved.html", "Get Involved"),
]


def build():
    search_entries = []
    for filename, title, desc, fn, keywords in PAGES:
        page(filename, title, desc, filename, fn())
        # Clean title for search (strip site suffix)
        short = title.split(" | ")[0]
        search_entries.append({"title": short, "url": filename, "summary": desc, "keywords": keywords})

    for filename, target, label in REDIRECTS:
        redirect(filename, target, label)

    # Emit search index as a JS file (works from file:// — no fetch/CORS)
    import json
    idx = "window.CARE_SEARCH_INDEX = " + json.dumps(search_entries, ensure_ascii=False, indent=2) + ";\n"
    with open(os.path.join(ROOT, "assets", "js", "search-index.js"), "w", encoding="utf-8") as f:
        f.write(idx)

    print("Built %d pages + %d redirects + search index." % (len(PAGES), len(REDIRECTS)))


if __name__ == "__main__":
    build()

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
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # -> static-site/
DATA_DIR = os.path.join(ROOT, "assets", "data")

# ---- Site config -------------------------------------------
PHONE = "+92 332 3610790"
PHONE_HREF = "tel:+923323610790"
EMAIL = "info@carepk.org"
FB = "https://www.facebook.com/profile.php?id=100084957522371"
IG = "https://www.instagram.com/care_jmdc/"
IG_HANDLE = "@CARE_JMDC"
# Interim office / contact address: Jinnah Medical & Dental College, Karachi (per CARE, "for now").
# This is NOT the registered address — that is REG_ADDRESS below.
ADDRESS = "Jinnah Medical &amp; Dental College, 22-23 Shaheed-e-Millat Road, Karachi-74000"
FORMSPREE = "https://formspree.io/f/YOUR_FORM_ID"  # TODO: replace once account is set up
VERSION = "8"  # bump to cache-bust styles.css / JS after a redesign

# ---- Official identity (domain verification, e.g. Google for Nonprofits) ----
SITE_URL = "https://carepk.org"
BRAND = "CARE"
BRAND_TAG = "CARE Aid &amp; Rehabilitation in Emergency"        # body text / tags
LEGAL_NAME = "CARE AID &amp; REHABILITATION IN EMERGENCY (C.A.R.E)"  # exact legal name (HTML)
# Registration details — must match the SECP records exactly. Do not guess.
# Source: SECP licensed Section 42 companies register (secp.gov.pk/data-and-statistics/).
REG_NO = "LD/Co. 42/201/2026"
REG_AUTHORITY = "Securities and Exchange Commission of Pakistan (SECP)"
REG_ACT = "Section 42 of the Companies Act, 2017"
REG_LICENCE_TYPE = "Section 42 Company (not-for-profit)"
REG_EXPIRY = "Nil"
REG_QR_ID = "6551"
REG_VERIFY_URL = "https://www.secp.gov.pk/data-and-statistics/"
REG_DATE = "30th October 2026"
REG_ADDRESS = "S. R-6, 7/A, Street 6, Sector 7-A, Korangi Industrial Area Karachi"

# Shown ONCE above every group of policy documents on a page (never per card).
DOCS_NOTICE = "These documents are pending signatures and will be re-uploaded soon."


# ---- Data files (edit the JSON, then re-run this script) ----
def load_json(name, default):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        print("WARNING: %s missing — related blocks are skipped." % name)
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


EVENTS = load_json("events.json", [])            # inclusive dates; status computed in the browser
MEDIA = {m["id"]: m for m in load_json("media.json", [])}
OUTPUTS = load_json("media-outputs.json", {})     # written by process_media.py (published media only)
DOCS = load_json("documents.json", [])            # written by documents_meta.py
BOARD = load_json("board.json", {"confirmed": False, "members": []})
DOC_BY_STEM = {d["file"][:-4]: d for d in DOCS if d.get("publish", True)}
DOC_GROUPS = ["Governance", "Programmes &amp; patients", "People &amp; conduct",
              "Fundraising &amp; finance", "Website &amp; media"]

BOARD_PAGE = "board-of-directors.html"


def noindex(filename):
    """Pages kept out of search engines, sitemap.xml and the site search."""
    return filename == BOARD_PAGE and not BOARD.get("confirmed")


def logo_src(size=192):
    """Small logo derivative (process_media.py) if present, else the original."""
    name = "logo-192.png" if size > 48 else "favicon-48.png"
    return "assets/" + name if os.path.exists(os.path.join(ROOT, "assets", name)) else "assets/logo.png"


def esc(s):
    return html.escape(s or "", quote=True)


def page_url(filename):
    """Absolute canonical URL for a page (index -> site root)."""
    return SITE_URL + "/" if filename == "index.html" else SITE_URL + "/" + filename

# Each nav item: (label, href, [ (child_label, child_href), ... ]).
# Children render as a dropdown (desktop) / collapsible submenu (mobile),
# linking to that page's internal sections.
NAV = [
    ("Home", "index.html", []),
    ("About", "about.html", [
        ("Mission &amp; Vision", "about.html#mission"),
        ("Our Story", "about.html#story"),
        ("Leadership", "about.html#leadership"),
        ("Board of Directors", BOARD_PAGE),
        ("Governance &amp; Partners", "about.html#governance"),
        ("Policies", "about.html#policies"),
        ("Annual Reports", "about.html#annual-reports"),
    ]),
    ("Care Programs", "programs.html", [
        ("Drug Bank", "programs.html#drug-bank"),
        ("Medical Camps", "programs.html#medical-camps"),
        ("Health Awareness", "programs.html#health-awareness"),
        ("Community Outreach", "programs.html#community-outreach"),
        ("Emergency Support", "programs.html#emergency-support"),
        ("Volunteer Initiatives", "programs.html#volunteer-initiatives"),
    ]),
    ("Impact", "impact.html", [
        ("In Numbers", "impact.html#numbers"),
        ("Impact Dashboard", "impact.html#dashboard"),
    ]),
    ("Get Involved", "get-involved.html", [
        ("Volunteer", "get-involved.html#volunteer"),
        ("Partner", "get-involved.html#partner"),
        ("Corporate", "get-involved.html#corporate"),
        ("CSR", "get-involved.html#csr"),
        ("Universities", "get-involved.html#universities"),
        ("Funders", "get-involved.html#funders"),
    ]),
    ("Donate", "donate.html", []),
    ("News &amp; Events", "news-events.html", [
        ("Calendar", "news-events.html#calendar"),
        ("Upcoming", "news-events.html#upcoming"),
        ("Past Events", "news-events.html#past"),
        ("Latest News", "news-events.html#news"),
    ]),
    ("Resources", "resources.html", [
        ("Dearly Loved (CSR)", "resources.html#dearly-loved"),
        ("Policies &amp; Reports", "resources.html#policies-reports"),
    ]),
    ("Contact", "contact.html", []),
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
    "chevron-down": '<polyline points="6 9 12 15 18 9"/>',
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
def org_jsonld():
    """Organization structured data (index.html only). JSON inside <script> is raw
    text, so the legal name uses a literal '&' here, not '&amp;'."""
    import json
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND,
        "legalName": LEGAL_NAME.replace("&amp;", "&"),
        "url": SITE_URL,
        "email": EMAIL,
        "telephone": PHONE,
        "address": {
            # Office / contact address (JMDC Karachi), not the registered address.
            "@type": "PostalAddress",
            "streetAddress": "Jinnah Medical & Dental College, 22-23 Shaheed-e-Millat Road",
            "addressLocality": "Karachi",
            "postalCode": "74000",
            "addressCountry": "PK",
        },
        "sameAs": [FB, IG],
    }
    body = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return '<script type="application/ld+json">\n' + body + '\n</script>'


def head(title, description, filename):
    url = page_url(filename)
    return (
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>' + title + '</title>\n'
        '<meta name="description" content="' + description + '">\n'
        '<link rel="canonical" href="' + url + '">\n'
        '<meta property="og:url" content="' + url + '">\n'
        + ('<meta name="robots" content="noindex">\n' if noindex(filename) else '')
        + (org_jsonld() + '\n' if filename == "index.html" else '') +
        '<link rel="icon" href="' + logo_src(48) + '" sizes="48x48">\n'
        '<link rel="apple-touch-icon" href="' + logo_src(192) + '">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=Hanken+Grotesk:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'
        '<link rel="stylesheet" href="assets/css/styles.css?v=' + VERSION + '">'
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
        '<a href="' + IG + '" target="_blank" rel="noreferrer" aria-label="CARE on Instagram">' + icon("instagram") + '</a>'
        '</div>'
        '</div></div>'
    )
    # Desktop links (items with children get a hover/focus dropdown)
    links = ""
    for label, href, children in NAV:
        cur = ' aria-current="page"' if href == active else ""
        if children:
            align = " align-right" if href in ("news-events.html", "resources.html") else ""
            dd = "".join('<a href="' + chref + '">' + clabel + '</a>' for clabel, chref in children)
            links += ('<div class="nav-item">'
                      '<a class="nav-link" href="' + href + '"' + cur + '>' + label
                      + icon("chevron-down", "nav-caret") + '</a>'
                      '<div class="nav-dropdown' + align + '">' + dd + '</div></div>')
        else:
            links += '<a class="nav-link" href="' + href + '"' + cur + '>' + label + '</a>'
    # Mobile links (items with children get a collapsible submenu)
    mlinks = ""
    for label, href, children in NAV:
        cur = ' aria-current="page"' if href == active else ""
        if children:
            sub = "".join('<a href="' + chref + '">' + clabel + '</a>' for clabel, chref in children)
            mlinks += ('<div class="m-item"><div class="m-row">'
                       '<a href="' + href + '"' + cur + '>' + label + '</a>'
                       '<button class="m-toggle" aria-label="Toggle ' + label.replace("&amp;", "and") + ' submenu" aria-expanded="false">'
                       + icon("chevron-down") + '</button></div>'
                       '<div class="m-sub">' + sub + '</div></div>')
        else:
            mlinks += '<a href="' + href + '"' + cur + '>' + label + '</a>'

    nav = (
        '<nav class="navbar"><div class="container">'
        '<a class="brand" href="index.html">'
        '<img src="' + logo_src() + '" alt="CARE logo" width="40" height="40">'
        '<span><span class="brand-name">CARE</span><br><span class="brand-tag">' + BRAND_TAG + '</span></span>'
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
    for label, href, _children in NAV:
        links += '<li><a href="' + href + '">' + label + '</a></li>'
    return (
        '<footer class="site-footer"><div class="container"><div class="footer-grid">'
        # Brand
        '<div class="footer-brand">'
        '<div class="brand"><img src="' + logo_src() + '" alt="CARE logo" width="40" height="40">'
        '<span><span class="brand-name">CARE</span><br><span class="brand-tag">' + BRAND_TAG + '</span></span></div>'
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
        '<span><!-- Interim office/contact address: JMDC Karachi (per CARE). Not the registered address. -->'
        '<strong style="color:rgba(255,255,255,.85);font-weight:600">Office / Contact address</strong><br>'
        + ADDRESS + '</span></li>'
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
        '<div class="footer-bottom">'
        '<p>&copy; <span data-year>2026</span> ' + LEGAL_NAME + ' &middot; Registration No. ' + REG_NO + '</p>'
        '<p style="margin-top:.4rem">carepk.org is the official website of ' + LEGAL_NAME + '.</p>'
        '<nav class="footer-policies" aria-label="Policies">'
        '<a href="privacy-policy.html">Privacy Policy</a><span aria-hidden="true">&middot;</span>'
        '<a href="terms.html">Terms &amp; Conditions</a><span aria-hidden="true">&middot;</span>'
        '<a href="safeguarding-policy.html">Safeguarding Policy</a><span aria-hidden="true">&middot;</span>'
        '<a href="news-events.html#photography">Photography &amp; Media Consent</a>'
        '</nav>'
        '</div>'
        '</footer>'
    )


def scripts(filename=""):
    out = (
        '<script src="assets/js/search-index.js?v=' + VERSION + '"></script>'
        '<script src="assets/js/search.js?v=' + VERSION + '"></script>'
        '<script src="assets/js/main.js?v=' + VERSION + '"></script>'
    )
    if filename == "news-events.html":
        # Calendar assets load on this page only (vendored, no CDN at runtime).
        out += ('\n<script defer src="assets/vendor/fullcalendar/index.global.min.js?v=6.1.22"></script>'
                '<script defer src="assets/js/events-calendar.js?v=' + VERSION + '"></script>')
    return out


def page(filename, title, description, active, body):
    doc = (
        '<!doctype html>\n<html lang="en">\n<head>\n' + head(title, description, filename) + '\n</head>\n<body>\n'
        + header(active) + '\n<main>\n' + body + '\n</main>\n' + footer() + '\n' + scripts(filename) + '\n</body>\n</html>\n'
    )
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(doc)


def redirect(filename, target, label):
    # Redirect stubs canonicalise to the page they forward to (fragment dropped),
    # not to themselves — they are not real pages.
    canon = page_url(target.split("#")[0])
    doc = (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta http-equiv="refresh" content="0; url=' + target + '">\n'
        '<link rel="canonical" href="' + canon + '">\n'
        '<meta property="og:url" content="' + canon + '">\n'
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


# ---- Media helpers ------------------------------------------
# A slot only shows a photo when process_media.py published it (consent is not
# "required" and the file exists). Anything held or missing falls back to the
# existing placeholder box — never a broken image.
def published(mid):
    return bool(mid) and mid in OUTPUTS and MEDIA.get(mid, {}).get("consent") != "required"


def focus_pos(mid):
    fx, fy = MEDIA[mid].get("focus", [0.5, 0.5])
    return "object-position:%g%% %g%%" % (round(fx * 100, 1), round(fy * 100, 1))


def media_img(mid, kind="card", cls="media-photo"):
    o = OUTPUTS[mid][kind]
    style = focus_pos(mid)
    if MEDIA[mid].get("lowRes"):
        style += ";max-width:%dpx" % o["width"]          # never display beyond native width
    return ('<img class="' + cls + '" src="' + o["src"] + '" alt="' + esc(MEDIA[mid]["alt"]) + '" '
            'width="%d" height="%d" loading="lazy" decoding="async" style="%s">' % (o["width"], o["height"], style))


def media_slot(mid, placeholder, min_height="20rem"):
    """feature-media block: photo if published, otherwise the existing placeholder."""
    if published(mid):
        return '<div class="feature-media has-photo">' + media_img(mid) + '</div>'
    held = ('<!-- media "%s" is consent-held or not yet processed; placeholder shown -->' % mid) if mid else ''
    return ('<div class="feature-media"><div class="placeholder-box" style="min-height:' + min_height + '">'
            + held + placeholder + '</div></div>')


# ---- Policy document helpers --------------------------------
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fmt_day(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return "%d %s %d" % (d, MONTHS[m - 1], y)


def fmt_range(start, end):
    """en-GB: '17 Jun 2026', '13–16 Apr 2026', '30 Jun – 2 Jul 2026'."""
    ys, ms, ds = (int(x) for x in start.split("-"))
    ye, me, de = (int(x) for x in (end or start).split("-"))
    if (ys, ms, ds) == (ye, me, de):
        return fmt_day(start)
    if (ys, ms) == (ye, me):
        return "%d&ndash;%d %s %d" % (ds, de, MONTHS[ms - 1], ys)
    if ys == ye:
        return "%d %s &ndash; %d %s %d" % (ds, MONTHS[ms - 1], de, MONTHS[me - 1], ys)
    return fmt_day(start) + " &ndash; " + fmt_day(end)


def fmt_size(n):
    return ("%.1f MB" % (n / 1048576.0)) if n >= 1048576 else ("%d KB" % round(n / 1024.0))


def doc_badge(d):
    if d.get("status") == "signed" and d.get("signedOn"):
        return '<span class="doc-badge doc-badge--signed">Signed ' + fmt_day(d["signedOn"]) + ' &middot; v' + esc(d["version"]) + '</span>'
    return '<span class="doc-badge">' + icon("clock") + 'Pending signatures</span>'


def doc_card(stem):
    d = DOC_BY_STEM.get(stem)
    if not d:
        return ''
    href = "assets/documents/" + d["file"]
    title = esc(d["title"])
    size = fmt_size(d["bytes"])
    version = '' if d.get("status") == "signed" else '<span>v' + esc(d["version"]) + '</span><span aria-hidden="true">&middot;</span>'
    return (
        '<div class="doc-card">'
        '<div class="doc-card-icon">' + icon("file") + '</div>'
        '<div class="doc-card-body">'
        '<h4 class="doc-title">' + title + '</h4>'
        '<p class="doc-meta">' + version + doc_badge(d) + '<span aria-hidden="true">&middot;</span>'
        '<span>%d pages &middot; %s</span></p>' % (d["pages"], size) +
        '<div class="doc-actions">'
        '<a class="btn btn-outline btn-sm" href="' + href + '" target="_blank" rel="noopener">' + icon("eye") +
        'View PDF<span class="sr-only">: ' + title + ' (opens in a new tab)</span></a>'
        '<a class="btn btn-dark btn-sm" href="' + href + '" download>' + icon("download") +
        'Download<span class="sr-only">: ' + title + ' (PDF, ' + size + ')</span></a>'
        '</div></div></div>'
    )


def docs_notice():
    return '<p class="docs-notice" role="note">' + icon("clock") + DOCS_NOTICE + '</p>'


def docs_block(primary, related=(), related_label="Related documents"):
    """Notice once, then the primary card(s), then any related cards."""
    prim = "".join(doc_card(s) for s in primary)
    rel = "".join(doc_card(s) for s in related)
    if not (prim or rel):
        return '<!-- documents.json missing or all documents unpublished -->'
    out = '<div class="docs-block">' + docs_notice()
    if prim:
        out += '<div class="doc-list">' + prim + '</div>'
    if rel:
        out += '<h3 class="docs-subhead">' + related_label + '</h3><div class="doc-list">' + rel + '</div>'
    return out + '</div>'


def docs_grouped():
    """All published documents, grouped (about.html#policies, resources.html)."""
    if not DOC_BY_STEM:
        return '<!-- documents.json missing -->'
    out = '<div class="docs-block docs-block--grouped">' + docs_notice()
    for g in DOC_GROUPS:
        items = [s for s, d in DOC_BY_STEM.items() if esc(d["group"]) == g]
        if items:
            out += '<h3 class="docs-subhead">' + g + '</h3><div class="doc-list">' + "".join(doc_card(s) for s in items) + '</div>'
    return out + '</div>'


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
        ("check", "Registration", "Our legal registration details.", "governance.html#registration"),
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
        '<p class="eyebrow">' + BRAND_TAG + '</p>'
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
        + media_slot("heat-relief-camp-03", "Organization photo &mdash; coming soon") +
        '<div class="feature-body"><p class="eyebrow">About CARE</p>'
        '<h2>' + BRAND_TAG + '</h2>'
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
        '<p><a href="governance.html#registration" style="color:var(--red);text-decoration:underline;text-underline-offset:3px">'
        + LEGAL_NAME + ' is a registered nonprofit in Pakistan. carepk.org is our official website.</a></p>'
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
        '<div class="center-btn cta-actions"><a class="btn btn-outline" href="governance.html">View Governance</a>'
        '<a class="btn btn-outline" href="' + BOARD_PAGE + '">View Board of Directors</a></div>'
        '</div></section>'

        # Policies
        '<section id="policies" class="section bg-off-white"><div class="container max-720" style="text-align:center">'
        '<h2 class="section-title">Policies</h2><div class="red-divider"></div>'
        '<p style="color:var(--mid-gray);line-height:1.8">CARE&rsquo;s policy documents are available to view and download below.</p>'
        '<div class="cta-actions mt-3">'
        '<a class="btn btn-outline" href="privacy-policy.html">Privacy Policy</a>'
        '<a class="btn btn-outline" href="terms.html">Terms &amp; Conditions</a>'
        '<a class="btn btn-outline" href="safeguarding-policy.html">Safeguarding Policy</a>'
        '<a class="btn btn-outline" href="volunteer-policy.html">Volunteer Policy</a>'
        '</div></div>'
        '<div class="container max-720 mt-4">' + docs_grouped() + '</div></section>'

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

    # Photo per section (media.json id). Held / missing media keep the placeholder.
    section_media = {
        "medical-camps": "free-medical-camp-02",      # consent-held -> placeholder until "confirmed"
        "health-awareness": "derma-session-02",
        "community-outreach": "heat-relief-camp-01",
        "emergency-support": "bls-workshop",
        "volunteer-initiatives": "blood-donation-drive-03",
    }
    section_docs = {
        "drug-bank": ["care-patient-assistance-policy", "care-medical-assistance-and-referral-policy"],
        "medical-camps": ["care-patient-assistance-policy", "care-medical-assistance-and-referral-policy",
                          "care-photography-media-and-consent-policy"],
    }

    rows = ""
    for i, (sid, ic, title, desc, bullets) in enumerate(sections):
        media = media_slot(section_media.get(sid),
                           '<!-- TODO: photos pending from Adeena -->Program photo &mdash; coming soon', "18rem")
        docs = ('<div class="mt-4">' + docs_block(section_docs[sid], related_label="") + '</div>') if sid in section_docs else ''
        if desc is None:
            body = ('<div class="feature-body"><div class="badge">' + icon(ic) + '</div>'
                    '<h2>' + title + '</h2>'
                    '<!-- TODO: content pending, CARE team is writing this one -->'
                    + note("Drug Bank programme copy is being written by the CARE team.") + docs + '</div>')
        else:
            bl = "".join('<li>' + b + '</li>' for b in bullets)
            body = ('<div class="feature-body"><div class="badge">' + icon(ic) + '</div>'
                    '<h2>' + title + '</h2><p>' + desc + '</p>'
                    '<ul class="check-list">' + bl + '</ul>' + docs + '</div>')
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
        '<section id="numbers" class="section bg-white"><div class="container">'
        '<h2 class="section-title">Our Impact in Numbers</h2>'
        '<p class="section-subtitle">Verified figures are being finalised by the CARE team.</p><div class="red-divider"></div>'
        '<!-- TODO: blocked on verified figures, same as homepage -->'
        '<div class="grid grid-3">' + matrix + '</div>'
        '</div></section>'
        '<section id="dashboard" class="section bg-off-white"><div class="container">'
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
    # Bank details are placeholders pending real account information.
    bank_labels = ["Account Title", "Account No", "Bank Name", "Branch Name", "Branch Code", "IBAN"]
    bank_html = "<!-- TODO: bank details pending — empty placeholders for now -->"
    for k in bank_labels:
        bank_html += ('<div class="bank-row"><span class="k">' + k + '</span>'
                      '<span class="v" style="color:var(--muted);font-weight:400">To be provided</span></div>')

    ways = [
        ("In-Person Donation", "Visit our office and contribute directly. Our team will issue an official receipt."),
        ("JazzCash / EasyPaisa", "Mobile wallet transfers accepted. Send to 0332 3610790 with reference &lsquo;CARE&rsquo;."),
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
        '<p class="mt-2">' + todo("bank details pending confirmation") + '</p>'
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
        # Related policy documents (new block, below the existing content)
        '<section id="donation-policies" class="section bg-white"><div class="container max-720">'
        '<h2 class="section-title">Fundraising &amp; Finance Documents</h2><div class="red-divider"></div>'
        + docs_block(["care-donations-and-fundraising-policy", "care-zakat-and-sadaqah-management-policy",
                      "care-financial-management-policy"]) +
        '</div></section>'
    )


def event_media(ev):
    """Published media for an event, poster first. Held items are simply absent."""
    items = [mid for mid in ev.get("media", []) if published(mid)]
    items.sort(key=lambda mid: 0 if MEDIA[mid].get("poster") else 1)
    return items


def event_cover(ev):
    """Cover id: the event's cover if published, else the first published non-poster item."""
    if published(ev.get("cover")) and "card" in OUTPUTS[ev["cover"]]:
        return ev["cover"]
    return None


def events_client_data():
    """Resolved event data for assets/js/events-calendar.js, embedded in the page
    (works from file:// — no fetch). Status is NOT included: the browser computes it."""
    out = []
    for ev in EVENTS:
        gallery = []
        for mid in event_media(ev):
            m, o = MEDIA[mid], OUTPUTS[mid]
            if m["type"] == "video":
                gallery.append({"type": "video", "src": o["video"]["src"], "poster": o["frame"]["src"],
                                "width": o["video"]["width"], "height": o["video"]["height"], "alt": m["alt"]})
            else:
                gallery.append({"type": "image", "src": o["full"]["src"], "width": o["full"]["width"],
                                "height": o["full"]["height"], "alt": m["alt"], "poster": bool(m.get("poster"))})
        out.append({k: ev.get(k) for k in ("id", "title", "category", "start", "end", "time", "location", "summary")}
                   | {"gallery": gallery})
    return json.dumps(out, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def event_card(ev):
    cover = event_cover(ev)
    n = len(event_media(ev))
    if cover:
        media = media_img(cover, "card", "event-cover")
    else:
        media = ('<div class="placeholder-box event-cover-ph"><!-- no published cover (none supplied or consent-held) -->'
                 'Photos coming soon</div>')
    meta = ('<div class="event-meta">' + icon("calendar") + '<time datetime="' + ev["start"] + '">'
            + fmt_range(ev["start"], ev["end"]) + '</time></div>')
    if ev.get("time"):
        meta += '<div class="event-meta">' + icon("clock") + esc(ev["time"]) + '</div>'
    if ev.get("location"):
        meta += '<div class="event-meta">' + icon("pin") + esc(ev["location"]) + '</div>'
    else:
        meta += '<!-- TODO: location not supplied -->'
    summary = ('<p>' + esc(ev["summary"]) + '</p>') if ev.get("summary") else '<!-- TODO: summary not supplied -->'
    if ev.get("mediaProvisional"):
        summary += '<!-- TODO: photo-to-event link is provisional (photo metadata stripped) — confirm -->'
    label = ("View photos (%d)" % n) if n else "View details"
    return (
        '<li class="event-card" data-event-id="' + esc(ev["id"]) + '" data-start="' + ev["start"] + '" data-end="' + ev["end"] + '">'
        + media +
        '<div class="event-body"><h3>' + esc(ev["title"]) + '</h3>' + meta + summary +
        '<button type="button" class="btn btn-outline btn-sm mt-2" data-event-open="' + esc(ev["id"]) + '" hidden>'
        + label + '<span class="sr-only">: ' + esc(ev["title"]) + '</span></button>'
        '</div></li>'
    )


def news_events():
    # Events come from assets/data/events.json (newest first). Without JS they all
    # render as one plain list; events-calendar.js sorts them into Upcoming / Past
    # against today's date in Asia/Karachi, so the page can never go stale.
    events = sorted(EVENTS, key=lambda e: (e["end"], e["start"]), reverse=True)
    cards = "".join(event_card(ev) for ev in events)

    news_cats = ["Medical Camps", "Volunteer Activities", "Outreach", "Partnership", "CSR (Dearly Loved)"]
    news_html = ""
    for cat in news_cats:
        news_html += ('<div class="card"><h3>' + cat + '</h3>'
                      '<p>' + todo("latest news content pending") + '</p></div>')

    dialog = (
        '<dialog class="event-dialog" data-event-dialog aria-labelledby="event-dialog-title">'
        '<div class="event-dialog-inner">'
        '<button type="button" class="icon-btn event-dialog-close" data-dialog-close aria-label="Close">' + icon("x") + '</button>'
        '<p class="eyebrow" data-dialog-status></p>'
        '<h2 id="event-dialog-title" data-dialog-title></h2>'
        '<div class="event-dialog-meta" data-dialog-meta></div>'
        '<p class="event-dialog-summary" data-dialog-summary></p>'
        '<figure class="event-gallery" data-gallery>'
        '<div class="event-gallery-stage" data-gallery-stage></div>'
        '<figcaption class="event-gallery-caption" data-gallery-caption></figcaption>'
        '</figure>'
        '<div class="event-gallery-controls" data-gallery-controls>'
        '<button type="button" class="btn btn-outline btn-sm" data-gallery-prev>&larr; Previous</button>'
        '<span class="event-gallery-counter" data-gallery-counter aria-live="polite"></span>'
        '<button type="button" class="btn btn-outline btn-sm" data-gallery-next>Next &rarr;</button>'
        '</div></div></dialog>'
    )

    return (
        banner("News &amp; Events", "News &amp; Events") +
        '<section class="section bg-white"><div class="container" data-tabs>'
        '<div class="tabs" role="tablist">'
        '<button class="tab-btn" data-tab="calendar" aria-selected="false">Calendar</button>'
        '<button class="tab-btn" data-tab="upcoming" aria-selected="false">Upcoming</button>'
        '<button class="tab-btn" data-tab="past" aria-selected="true">Past Events</button>'
        '<button class="tab-btn" data-tab="news" aria-selected="false">Latest News</button>'
        '</div>'
        # Calendar (built by events-calendar.js)
        '<div class="tab-panel" data-panel="calendar">'
        '<h2 class="section-title">Events Calendar</h2><div class="red-divider"></div>'
        '<p class="calendar-legend"><span class="ev-key ev-key--upcoming" aria-hidden="true"></span>Upcoming'
        '<span class="ev-key ev-key--past" aria-hidden="true"></span>Past events are muted and labelled &ldquo;Past&rdquo;.</p>'
        '<div class="events-calendar" data-events-calendar></div>'
        '</div>'
        # Upcoming (filled by JS; empty state otherwise)
        '<div class="tab-panel" data-panel="upcoming">'
        '<h2 class="section-title">Upcoming Events</h2><div class="red-divider"></div>'
        '<ul class="event-grid" data-events-upcoming></ul>'
        '<p class="events-empty" data-events-empty>No events announced right now. Follow '
        '<a href="' + IG + '" target="_blank" rel="noreferrer">' + IG_HANDLE + '</a> on Instagram for updates.</p>'
        '</div>'
        # Past — server-rendered list of ALL events (no-JS / SEO fallback); JS moves upcoming ones out.
        '<div class="tab-panel active" data-panel="past">'
        '<h2 class="section-title" data-past-heading>Events</h2><div class="red-divider"></div>'
        '<ul class="event-grid" data-events-past>' + cards + '</ul>'
        '</div>'
        # News
        '<div class="tab-panel" data-panel="news">'
        '<h2 class="section-title">Latest News</h2>'
        '<p class="section-subtitle">Updates across our programmes</p><div class="red-divider"></div>'
        '<div class="grid grid-3">' + news_html + '</div></div>'
        '</div></section>'
        # Photography note
        '<section id="photography" class="section bg-off-white"><div class="container max-720">'
        '<h2 class="section-title">Photography at CARE Events</h2><div class="red-divider"></div>'
        '<p class="section-subtitle" style="margin-bottom:2rem">Photos and videos are sometimes taken at CARE events. '
        'If you would rather not appear in them, or would like a photo of you removed from this website, email '
        '<a class="text-link" href="mailto:' + EMAIL + '">' + EMAIL + '</a>.</p>'
        + docs_block(["care-photography-media-and-consent-policy"]) +
        '</div></section>'
        + dialog +
        '<script type="application/json" id="care-events-data">' + events_client_data() + '</script>'
    )


def resources():
    return (
        banner("Resources", "Resources") +
        '<section id="dearly-loved" class="section bg-white"><div class="container">'
        '<h2 class="section-title">Dearly Loved (CSR)</h2>'
        '<p class="section-subtitle">Our corporate social responsibility programme</p><div class="red-divider"></div>'
        '<div class="max-720"><!-- TODO: content pending -->'
        + note("Dearly Loved (CSR) programme content is pending.") + '</div>'
        '</div></section>'
        '<section id="policies-reports" class="section bg-off-white"><div class="container max-720" style="text-align:center">'
        '<h2 class="section-title">Policies &amp; Reports</h2><div class="red-divider"></div>'
        '<p style="color:var(--mid-gray);line-height:1.8">Our policies and annual reports live on the About page.</p>'
        '<div class="cta-actions mt-3">'
        '<a class="btn btn-outline" href="about.html#policies">View Policies</a>'
        '<a class="btn btn-outline" href="about.html#annual-reports">Annual Reports</a>'
        '</div></div>'
        '<div class="container max-720 mt-4">' + docs_grouped() + '</div></section>'
    )


def governance():
    board = [("Prof. Tariq Mehmood", "Chairman, Board of Governors"), ("Dr. Ayesha Siddiqui", "Board Member"),
             ("Mr. Kamran Ali", "Board Member"), ("Dr. Farrukh Nazar", "Board Member")]
    grid = '<div class="team-grid">'
    for name, role in board:
        grid += ('<div class="team-member"><div class="team-photo">Photo</div>'
                 '<div class="name">' + name + '</div><div class="role">' + role + '</div></div>')
    grid += '</div>'

    # Legal Registration — reuses the existing .bank-row key/value styling (no new CSS).
    reg_rows = [
        ("Legal name", LEGAL_NAME),
        ("Registration number", REG_NO),
        ("Registering authority", REG_AUTHORITY),
        ("Registered under", REG_ACT),
        ("Licence type", REG_LICENCE_TYPE),
        ("Licence expiry", REG_EXPIRY),
        ("SECP QR ID", REG_QR_ID),
        ("Date of registration", REG_DATE),
        ("Registered address", REG_ADDRESS),
        ("Official website", '<a href="' + SITE_URL + '">' + SITE_URL + '</a>'),
        ("Official email", '<a href="mailto:' + EMAIL + '">' + EMAIL + '</a>'),
        ("Verify", '<a href="' + REG_VERIFY_URL + '" target="_blank" rel="noopener">SECP data &amp; statistics</a>'),
    ]
    reg_dl = '<dl>'
    for k, v in reg_rows:
        reg_dl += '<div class="bank-row"><dt class="k">' + k + '</dt><dd class="v">' + v + '</dd></div>'
    reg_dl += '</dl>'

    return (
        banner("Governance", "Governance") +
        '<section class="section bg-white"><div class="container">'
        '<h2 class="section-title">Governance Structure</h2>'
        '<p class="section-subtitle">How CARE is governed and held accountable</p><div class="red-divider"></div>'
        '<section id="registration" class="max-720" aria-labelledby="registration-title">'
        '<h3 id="registration-title" style="text-align:center;margin-bottom:1.5rem">Legal Registration</h3>'
        + reg_dl +
        '</section>'
        '<h3 style="text-align:center;margin:3rem 0 1.5rem">Board of Governors</h3>' + grid +
        '<p class="text-center mt-3" style="color:var(--mid-gray);font-size:.85rem">' + todo("confirm board details and photos") + '</p>'
        '<div class="center-btn"><a class="btn btn-outline" href="' + BOARD_PAGE + '">View Board of Directors</a></div>'
        '</div></section>'
        '<section id="governance-documents" class="section bg-off-white"><div class="container max-720">'
        '<h2 class="section-title">Governance Documents</h2><div class="red-divider"></div>'
        + docs_block(["care-governance-policy",
                      "care-student-council-university-department-representatives-advisory-council-and-patron-governance-policy",
                      "care-financial-management-policy", "care-procurement-and-asset-management-policy"]) +
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


def policy_page(title, crumb, intro, primary, related=()):
    # The legal text lives in the PDFs only — never summarised or converted to HTML here.
    return (
        banner(title, crumb) +
        '<section class="section bg-white"><div class="container max-720">'
        '<h2 class="section-title">' + title + '</h2><div class="red-divider"></div>'
        '<p style="color:var(--mid-gray);line-height:1.8;text-align:center">' + intro + '</p>'
        '<div class="mt-4">' + docs_block(primary, related) + '</div>'
        '</div></section>'
    )


def board_of_directors():
    # Source: WhatsApp from Junaid, 11 Nov 2026 ("board of directors"). Names exactly as typed,
    # not yet confirmed with each person. Edit assets/data/board.json — never this function —
    # to add/rename a Director, add a role/bio, or flip "confirmed" (which drops noindex).
    cards = ""
    for m in BOARD.get("members", []):
        name = esc(m["name"])
        photo = m.get("photo")
        if photo and m.get("photoConsent") == "confirmed" and os.path.exists(os.path.join(ROOT, photo)):
            avatar = ('<img class="team-photo team-photo-img" src="' + esc(photo) + '" alt="Portrait of ' + name + '" '
                      'width="120" height="120" loading="lazy" decoding="async">')
        else:
            parts = m["name"].split()
            initials = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()
            avatar = ('<!-- no photo: needs the Director\'s written/electronic consent (photography policy §2.1, §5) -->'
                      '<div class="team-photo team-initials" aria-hidden="true">' + esc(initials) + '</div>')
        role = ('<div class="role">' + esc(m["role"]) + '</div>') if m.get("role") else ''
        bio = ('<p class="bio">' + esc(m["bio"]) + '</p>') if (m.get("bio") or "").strip() else ''
        cards += ('<div class="team-member">' + avatar + '<div class="name">' + name + '</div>'
                  '<div class="role">' + esc(m.get("title") or "") + '</div>' + role + bio + '</div>')
    return (
        banner("Board of Directors", '<a href="about.html">About</a> / Board of Directors') +
        '<section class="section bg-white"><div class="container">'
        '<p class="section-subtitle" style="margin-bottom:3rem">The Directors of CARE Aid &amp; Rehabilitation in Emergency.</p>'
        '<!-- TODO: names not yet confirmed with each Director; draft Governance Policy §4.1 says the Board has four Directors (three listed). Titles/roles not supplied. -->'
        '<div class="team-grid team-grid--auto">' + cards + '</div>'
        '</div></section>'
        '<section class="section bg-off-white"><div class="container max-720">'
        '<h2 class="section-title">Related Documents</h2><div class="red-divider"></div>'
        + docs_block(["care-governance-policy"]) +
        '</div></section>'
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
        '<!-- Interim address: JMDC Karachi (per CARE) -->'
        '<div style="color:var(--mid-gray);font-size:.9rem">' + ADDRESS + '</div></div></div>'
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
        # Complaints & whistleblowing document
        '<section id="complaints" class="section bg-off-white"><div class="container max-720">'
        '<h2 class="section-title">Complaints &amp; Whistleblowing</h2><div class="red-divider"></div>'
        + docs_block(["care-complaints-and-whistleblowing-policy"]) +
        '<p class="text-center mt-3">See also: <a class="text-link" href="safeguarding-policy.html">Safeguarding Policy</a></p>'
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
    ("privacy-policy.html", "Privacy Policy | CARE Pakistan", "How CARE handles personal information.", lambda: policy_page("Privacy Policy", "Privacy Policy", "This policy describes how CARE collects, uses and protects personal information.", ["care-website-privacy-notice"], ["care-photography-media-and-consent-policy"]), "privacy policy notice data personal information photography consent"),
    ("terms.html", "Terms & Conditions | CARE Pakistan", "The terms and conditions for using the CARE website.", lambda: policy_page("Terms &amp; Conditions", "Terms &amp; Conditions", "The terms and conditions for using the CARE website.", ["care-website-terms-and-conditions"], ["care-website-privacy-notice"]), "terms conditions website use legal"),
    ("safeguarding-policy.html", "Safeguarding Policy | CARE Pakistan", "How CARE protects the people it serves.", lambda: policy_page("Safeguarding Policy", "Safeguarding Policy", "This policy sets out CARE&rsquo;s commitment to safeguarding the people it serves.", ["care-safeguarding-policy"], ["care-code-of-conduct-and-ethics", "care-anti-harassment-and-non-discrimination-policy", "care-complaints-and-whistleblowing-policy", "care-photography-media-and-consent-policy"]), "safeguarding policy protection code of conduct harassment complaints whistleblowing"),
    ("volunteer-policy.html", "Volunteer Policy | CARE Pakistan", "The standards and expectations for CARE volunteers.", lambda: policy_page("Volunteer Policy", "Volunteer Policy", "This policy sets out the standards, rights and responsibilities for CARE volunteers.", ["care-volunteer-policy"], ["care-code-of-conduct-and-ethics", "care-anti-harassment-and-non-discrimination-policy", "care-student-council-university-department-representatives-advisory-council-and-patron-governance-policy"]), "volunteer policy standards conduct student council"),
    (BOARD_PAGE, "Board of Directors | CARE Pakistan", "The Directors of CARE Aid & Rehabilitation in Emergency.", board_of_directors, "board directors governance"),
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
        page(filename, title, esc(desc), filename, fn())
        if noindex(filename):
            continue   # kept out of the site search (and sitemap) until confirmed
        if filename == "news-events.html":   # index event titles/categories from events.json
            keywords += " " + " ".join(e["title"] + " " + e.get("category", "") for e in EVENTS).lower()
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

    # robots.txt (allow all) + sitemap.xml (real pages only; redirect stubs are
    # excluded because they canonicalise elsewhere and would be flagged by Search Console)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: " + SITE_URL + "/sitemap.xml\n")
    urls = "".join("  <url><loc>" + page_url(fn) + "</loc></url>\n" for fn, *_ in PAGES if not noindex(fn))
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')

    print("Built %d pages + %d redirects + search index + robots.txt + sitemap.xml." % (len(PAGES), len(REDIRECTS)))


if __name__ == "__main__":
    build()

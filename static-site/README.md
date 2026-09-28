# CARE — Static Website

A fully static rebuild of the CARE (Care, Aid & Rehabilitation in Emergency) site:
plain **HTML + CSS + vanilla JS**. No Node.js, no npm, no framework, **no build step**
required to host or view it. Every page is a flat `.html` file that works when opened
directly (`file://`) or served by any static host (Netlify, GitHub Pages, S3, Amplify,
Vercel static, a plain web server, etc.).

## How to view

- **Double-click `index.html`** — it just opens, no server needed.
- Or serve the folder over HTTP, e.g.:
  ```bash
  python -m http.server 8099
  ```
  then visit `http://localhost:8099/`.

## Structure

```
static-site/
├── index.html              Home
├── about.html              About (Mission/Vision, Story + milestones, Leadership,
│                           Governance, Policies, Annual Reports)
├── programs.html           Care Programs (Drug Bank, Medical Camps, Health Awareness,
│                           Community Outreach, Emergency Support, Volunteer Initiatives)
├── impact.html             Impact + Impact Dashboard
├── get-involved.html       Volunteer / Partner / Corporate / CSR / Universities / Funders
├── donate.html             Bank details + other ways to give
├── news-events.html        Upcoming / Past / Latest News (tabbed)
├── resources.html          Dearly Loved (CSR)
├── governance.html         Governance
├── faq.html                FAQ (accordion)
├── privacy-policy.html
├── safeguarding-policy.html
├── volunteer-policy.html
├── testimonials.html
├── contact.html
│
├── team.html               ─┐  redirect stubs for old routes so old links
├── what-we-do.html          │  don't 404:  team → about#leadership,
├── events.html              │  what-we-do → programs, events → news-events,
├── join-us.html            ─┘  join-us → get-involved
│
├── assets/
│   ├── logo.png
│   ├── css/styles.css       All styling (design tokens ported from the old Tailwind theme)
│   └── js/
│       ├── main.js          Nav toggle, FAQ accordion, tabs, donate amounts,
│       │                    bank-details download, AJAX form submit (with plain fallback)
│       ├── search.js        Client-side substring search
│       └── search-index.js  Search index (window.CARE_SEARCH_INDEX — works from file://)
│
└── _generator/
    └── build.py             OPTIONAL. See below.
```

## Design

Colors are defined as CSS variables at the top of `assets/css/styles.css`:

- Primary red `#D32F2F` (hover `#B71C1C`), dark `#111111`, off-white `#FAFAFA`
- Headings: **Fraunces**; body: **Hanken Grotesk** (loaded from Google Fonts)

The site is mobile-first responsive; the full horizontal nav collapses to a hamburger
menu below 1440px.

### Interaction components (ported from Watermelon UI)

Several interactions are hand-ported from [Watermelon UI](https://ui.watermelon.sh)
components. The originals are React + Tailwind + Motion; these are plain CSS + vanilla
JS so the site keeps its no-build setup. Each is a progressive enhancement (JS adds an
`is-*` class; without JS the plain styles apply).

| Watermelon component | Where it's used |
|---|---|
| Fluid Tabs | News & Events tabs; sliding hover pill on the desktop nav and section chips |
| Shimmer Button | All primary/dark buttons (hover sweep; idle shimmer on header "Donate Now") |
| Card Split Accordion | FAQ |
| Copy Confirm | JazzCash number (Donate), phone + email (Contact) |
| Floating Input | Every form field — real `<label>`s that float on focus |
| Scroll Island | "On this page" progress pill on About, Programs, Get Involved |
| Command Search | Site search: grouped results, ↑/↓ + Enter, opens with `/` or Ctrl/⌘+K |

Also: blur-in headlines, number ticker on the headline stats, pointer spotlight on cards.

### Pending content

Pending items show a neutral public **Coming soon** pill. The internal detail of *what*
is pending and *who* to ask lives only as `# TODO:` comments in `_generator/build.py` —
never in the published HTML.

## The generator (`_generator/build.py`) — optional

To avoid hand-editing the shared header/footer in 15+ files, the pages are assembled by
a small Python script. **You do not need it to run the site** — the generated `.html`
files are the real deliverable and are fully self-contained.

Use it only when you want to change something shared (nav, footer, `<head>`) in one place:

```bash
python _generator/build.py     # rewrites every .html with the header/footer inlined
```

Edit page *content* either directly in the `.html` files, or in `build.py` and re-run it.
(Re-running overwrites the `.html` files, so don't mix both approaches on the same page.)

## Before going live — TODOs

Search `_generator/build.py` for `TODO`. Nothing was fabricated; every unfinished item is
a marked placeholder:

- **Forms:** set `FORMSPREE` in `build.py` to a real [Formspree](https://formspree.io) form
  URL and rebuild. Until then, submitting any form opens the visitor's email app with the
  form contents pre-filled to `carejmdc22@gmail.com`, so no enquiry is lost.
- **Bank details:** fill in `BANK_DETAILS` in `build.py`. While it is `None` the Donate page
  offers "details on request" (email + copy button) instead of a table of blanks.
- **Upcoming events:** add them to `upcoming` in `news_events()` with an ISO date. Past
  events are dropped at build time and hidden in the browser, so the page never goes stale.
- **Impact figures:** move each verified figure from `PENDING_STATS` into `HEADLINE_STATS`
  (the home strip and Impact page both read from it). Confirm the "50+ volunteers" figure.
- **Content pending:** Drug Bank copy, Governance, Resources (Dearly Loved), the 4th FAQ item.
- **Policies:** Privacy / Safeguarding / Volunteer policy text (check with the lawyer first).
- **Photos/videos:** placeholders throughout (patient journey, past events, team, etc.).
- **Milestone dates**, **Annual Reports / Financial Statements** PDFs and **partner logos**.
- **Domain:** when the custom domain is live, update `SITE_URL` in `build.py` (canonical,
  Open Graph, sitemap) and rebuild.

## Hosting config

`vercel.json` (in this folder, which is the Vercel project root) sets security headers
(CSP, X-Frame-Options, nosniff, Referrer-Policy, HSTS) and asset caching. `404.html`,
`robots.txt` and `sitemap.xml` are generated by `build.py`.

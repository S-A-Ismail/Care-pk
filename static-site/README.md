# CARE — Static Website

A fully static rebuild of the CARE (CARE Aid & Rehabilitation in Emergency) site:
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

Colors and fonts are carried over verbatim from the original site (defined as CSS
variables at the top of `assets/css/styles.css`):

- Primary red `#D32F2F` (hover `#B71C1C`), dark `#111111`, off-white `#FAFAFA`
- Headings: **Playfair Display**; body: **Inter** (loaded from Google Fonts)

The site is mobile-first responsive; the full horizontal nav collapses to a hamburger
menu below 1152px.

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

Search the source for `TODO` (they're visible in the rendered pages as `[TODO]` tags and
as HTML comments). Nothing was fabricated; every unfinished item is a marked placeholder:

- **Forms:** replace `YOUR_FORM_ID` in the `action="https://formspree.io/f/YOUR_FORM_ID"`
  of every form (6 on Get Involved, plus Contact and the footer newsletter) with a real
  [Formspree](https://formspree.io) form ID — or swap for Netlify Forms / Getform / a
  Mailchimp embed. Forms already degrade gracefully without JS (plain HTML POST).
- **Registration details:** replace the `{{REG_NO}}`, `{{REG_AUTHORITY}}`, `{{REG_ACT}}`,
  `{{REG_DATE}}` and `{{REGISTERED_ADDRESS}}` tokens (constants at the top of
  `_generator/build.py`, then rebuild) with the values from the registration certificate.
  They render in every footer and in the Legal Registration section of `governance.html`.
- **Impact figures:** all six stat categories show "Coming soon" pending verified numbers.
- **Office address:** footer + contact still show the Lahore address pending confirmation
  of the new one.
- **Content pending:** Drug Bank copy, Governance, Resources (Dearly Loved), the 4th FAQ item.
- **Policies:** Privacy / Safeguarding / Volunteer policy text (check with the lawyer first).
- **Photos/videos:** placeholders throughout (patient journey, past events, team, etc.).
- **Milestone dates**, **Annual Reports / Financial Statements** PDFs, **partner logos**,
  and the **Google Maps** embed (needs an API key) are all placeholdered.

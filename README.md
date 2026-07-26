# CARE — Care, Aid & Rehabilitation in Emergency

Website for the CARE NGO (Pakistan). A **framework-free static site**: plain HTML, CSS
and vanilla JavaScript — **no Node.js, no npm, no framework, no build step**. Every page
is a flat `.html` file that works opened directly (`file://`) or served by any static host.

> **This branch (`feature/static-site`)** replaces the earlier Next.js + AWS Amplify build.
> The Next.js app has been removed; the entire site now lives in [`static-site/`](static-site/).
> (The old Next.js version is still on the `dev` branch if you need it.)

---

## Run locally

No dependencies to install. Either:

- **Just open the file** — double-click `static-site/index.html`, or
- **Serve over HTTP** (recommended, mirrors production):
  ```bash
  cd static-site
  python -m http.server 8099
  ```
  then visit **http://localhost:8099/**.

Any static file server works (`python -m http.server`, `npx serve`, VS Code Live Server, etc.).

---

## Structure

```
care-pk/
├── static-site/          ← the website (this is what you deploy)
│   ├── index.html            Home
│   ├── about.html            About (mission, story, leadership, governance, policies)
│   ├── programs.html         Care Programs
│   ├── impact.html           Impact + dashboard
│   ├── get-involved.html     Volunteer / Partner / Corporate / CSR / Universities / Funders
│   ├── donate.html           Bank details + ways to give
│   ├── news-events.html      Upcoming / Past / Latest News (tabbed)
│   ├── resources.html        Dearly Loved (CSR)
│   ├── governance.html       Governance
│   ├── faq.html              FAQ (accordion)
│   ├── privacy-policy.html · safeguarding-policy.html · volunteer-policy.html
│   ├── testimonials.html · contact.html
│   ├── team.html · what-we-do.html · events.html · join-us.html   ← redirect stubs
│   │                                                                 for old routes
│   ├── assets/               logo, css/styles.css, js/ (main, search, search-index)
│   ├── _generator/build.py   OPTIONAL — see below
│   └── README.md             full details + the pre-launch TODO checklist
│
├── docs/                 backend-architecture notes (from the earlier plan)
├── CLAUDE.md             project context
├── .mcp.json             code-graph MCP config
└── README.md             this file
```

## Editing the shared header/footer

To avoid hand-editing the nav/footer in 15+ files, the pages are assembled by a small,
**optional** Python script. You don't need it to run or deploy the site — the generated
`.html` files are self-contained. Use it only to change something shared:

```bash
cd static-site
python _generator/build.py   # rewrites every .html with the header/footer inlined
```

Edit page *content* directly in the `.html` files, **or** in `build.py` and re-run it — but
not both on the same page (re-running overwrites the `.html`).

---

## Design

Brand tokens are CSS variables at the top of `static-site/assets/css/styles.css`:

| Token | Value |
|-------|-------|
| Primary | `#D32F2F` (hover `#B71C1C`) |
| Dark | `#111111` |
| Off-white | `#FAFAFA` |
| Headings | Playfair Display |
| Body | Inter |

Mobile-first responsive; the full nav collapses to a hamburger below 1152px.

---

## Deploy

The publish directory is **`static-site/`** (or move its contents to the repo root first).
No build command is required.

- **Vercel:** framework preset **Other**, no build command, output/root directory `static-site`.
- **Netlify:** build command empty, publish directory `static-site`.
- **GitHub Pages / S3 + CloudFront / any web server:** upload the contents of `static-site/`.

---

## Before going live

Nothing was fabricated — every unfinished item is a visible `[TODO]`. The full pre-launch
checklist (Formspree form IDs, verified impact figures, office address, pending copy, policy
text, photos, partner logos, Google Maps key) is in **[`static-site/README.md`](static-site/README.md)**.

# CARE — Care, Aid & Rehabilitation in Emergency

Website for the CARE NGO (Pakistan). Built with Next.js 15 and Tailwind CSS, hosted on AWS Amplify.

---

## Table of Contents

1. [Tech Stack](#tech-stack)
2. [Quick Start (Docker)](#quick-start-docker)
3. [Project Structure](#project-structure)
4. [Pages & Routes](#pages--routes)
5. [Component Library](#component-library)
6. [Styling System](#styling-system)
7. [AWS Integration Map](#aws-integration-map)
8. [Environment Variables](#environment-variables)
9. [Deploying to AWS Amplify](#deploying-to-aws-amplify)
10. [Phase Roadmap](#phase-roadmap)

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Framework | Next.js 15 (App Router) | Server components by default, great SEO, scales from static → SSR without rewrite |
| Language | TypeScript | Catches type errors at build time, important as the codebase grows |
| Styling | Tailwind CSS v3 | Utility-first, no separate CSS files to maintain, easy to keep brand-consistent |
| Icons | react-icons (Font Awesome 5) | Huge icon set, tree-shaken, consistent style |
| Fonts | Google Fonts via `next/font` | Inter (body), Playfair Display (headings) — auto-optimised, no layout shift |
| Container | Docker + Docker Compose | Run the site without installing Node.js locally |
| Hosting | AWS Amplify | CI/CD from GitHub, auto-scales, free tier covers early traffic |

---

## Quick Start (Docker)

**Prerequisites:** Docker Desktop installed and running.

```bash
# 1. Copy the environment file (required by docker-compose)
copy .env.example .env.local        # Windows
cp .env.example .env.local          # Mac/Linux

# 2. First run — builds the Docker image and installs dependencies
docker compose up --build

# 3. Subsequent runs (image already built)
docker compose up
```

The site is available at **http://localhost:3000**

Hot reload is enabled — editing any file on your machine instantly reflects in the browser without restarting the container.

### Stopping the container

```bash
docker compose down
```

### Rebuilding after adding a new package

Any time you add a dependency to `package.json`, you must rebuild the image so the new package is installed inside the container:

```bash
docker compose up --build
```

---

## Project Structure

```
care-pk/
│
├── app/                          # Next.js App Router — one folder = one route
│   ├── layout.tsx                # Root layout: wraps every page with Navbar + Footer
│   ├── globals.css               # Tailwind base + reusable utility component classes
│   ├── page.tsx                  # Home page (/)
│   ├── about/page.tsx            # About Us (/about)
│   ├── team/page.tsx             # Our Team (/team)
│   ├── what-we-do/page.tsx       # What We Do (/what-we-do)
│   ├── events/page.tsx           # Events & Workshops (/events)
│   ├── testimonials/page.tsx     # Testimonials (/testimonials)
│   ├── join-us/page.tsx          # Join Us / Volunteer (/join-us)
│   ├── donate/page.tsx           # Donate (/donate)
│   └── contact/page.tsx          # Contact Us (/contact)
│
├── components/                   # Reusable UI components
│   ├── Navbar.tsx                # Sticky top navigation with dropdowns (client)
│   ├── Footer.tsx                # 4-column footer with newsletter form (server)
│   ├── Hero.tsx                  # Auto-advancing image slider (client)
│   ├── Stats.tsx                 # Animated counters, scroll-triggered (client)
│   ├── WhatWeDo.tsx              # Services grid — 4 programme cards (server)
│   ├── ImpactSection.tsx         # Impact story cards (server)
│   ├── CallToAction.tsx          # Green CTA banner at bottom of pages (server)
│   ├── NewsletterForm.tsx        # Footer newsletter signup form (client)
│   ├── VolunteerForm.tsx         # Volunteer application form (client)
│   ├── ContactForm.tsx           # Contact message form (client)
│   └── DonateAmounts.tsx         # Donation amount selector (client)
│
├── public/                       # Static assets served at root URL
│   └── images/                   # (add site images here)
│
├── Dockerfile                    # Multi-stage: dev → builder → production
├── docker-compose.yml            # Local dev environment (uses 'dev' stage)
├── amplify.yml                   # AWS Amplify build configuration
├── next.config.mjs               # Next.js config (webpack polling for Docker)
├── tailwind.config.ts            # Brand colours, custom fonts
├── tsconfig.json                 # TypeScript compiler options
├── postcss.config.mjs            # PostCSS (required by Tailwind)
├── .eslintrc.json                # ESLint rules (Next.js defaults)
├── .env.example                  # Template for all environment variables
├── .env.local                    # Your local secrets — NEVER commit this
├── .gitignore                    # Excludes node_modules, .next, .env.local etc.
└── CLAUDE.md                     # AI assistant context file (architecture decisions)
```

### Key architectural decision: Server vs Client Components

Next.js 15 renders components on the **server by default** — faster page loads and better SEO. Components only become client-side when they need browser APIs or interactivity.

| Marker | Runs on | Used for |
|--------|---------|---------|
| *(no directive)* | Server | Static content, metadata, SEO |
| `"use client"` at top | Browser | Forms, state, event handlers, animations |

In this project, every page is a **Server Component**. Interactive pieces (forms, the hero slider, stat counters) are extracted into separate `"use client"` components and imported into the pages.

---

## Pages & Routes

### Home (`/`)
Composed entirely of smaller components — no logic lives in `page.tsx` itself:

```
Hero          ← animated slide banner
Stats         ← 500+ patients, 50+ volunteers, etc. (scroll-triggered counters)
WhatWeDo      ← 4 programme cards linking to /what-we-do#section
ImpactSection ← 3 story cards with photo placeholders
CallToAction  ← Donate / Volunteer banner
```

### About Us (`/about`)
Two sections: a text + photo layout explaining the organisation, and three cards for Mission / Vision / Values. Has a `#mission` anchor used by the navbar dropdown.

### Our Team (`/team`)
Three sections with separate `id` anchors (`#core`, `#board`, `#advisory`) so the navbar can deep-link directly to each group. The `TeamGrid` component is defined locally in the file since it's only used on this page.

### What We Do (`/what-we-do`)
Four programme sections (Emergency Aid, Patient Support, Rehabilitation, Community Outreach) with alternating photo-left / text-right layout. Has `id` anchors for each section (`#emergency`, `#patient`, `#rehab`, `#outreach`) used by navbar dropdowns and the WhatWeDo home component. Ends with a timeline of the organisation's history.

### Events (`/events`)
Upcoming events displayed as date-card + description. Past events as a simple list. Both are currently hardcoded — when a CMS or database is added (Phase 2), this page fetches data instead.

### Testimonials (`/testimonials`)
Written quotes in a 2-column grid. Video testimonial placeholders (3 slots) ready for YouTube embeds.

### Join Us (`/join-us`)
Three "how to help" cards, then a volunteer application form (`VolunteerForm`). The form is currently a stub — see [AWS Integration Map](#aws-integration-map) for how to wire it up.

### Donate (`/donate`)
Two columns: bank transfer details on the left, alternative donation methods + the `DonateAmounts` component on the right. The amount selector is a placeholder for the Stripe/JazzCash integration (Phase 2).

### Contact Us (`/contact`)
Contact info + social icons on the left, `ContactForm` on the right. Has a Google Maps embed placeholder at the bottom.

---

## Component Library

### `Navbar.tsx` *(client)*
- Sticky header with a dark-green top bar (email/phone/socials) and a main nav below
- Desktop: dropdown menus controlled by `onMouseEnter` / `onMouseLeave` state
- Mobile: hamburger toggle showing a stacked link list
- The `navLinks` array at the top of the file is the single source of truth for all nav items and their dropdowns — update links here only

### `Footer.tsx` *(server)*
- 4-column grid: brand blurb, quick links, contact info, newsletter form
- Quick links use an explicit `{ label, href }` map — do not use string manipulation to derive paths
- Delegates the newsletter form to `NewsletterForm` (client) to keep the footer itself server-rendered

### `Hero.tsx` *(client)*
- Auto-advances every 5 seconds using `setInterval` inside `useEffect`
- Navigation: previous/next arrow buttons + dot indicators
- Background colour changes between slides using Tailwind colour classes — all three classes must be hardcoded in the `slides` array (not constructed dynamically) so Tailwind includes them in the CSS bundle

### `Stats.tsx` *(client)*
- Each stat watches itself with `IntersectionObserver` — the counter only starts when the element scrolls into view
- `useCounter` hook increments from 0 to the target over ~60 frames (1.2 seconds) using `setInterval`
- Once a stat becomes active it stays active (counter doesn't reset on scroll out)

### `WhatWeDo.tsx` *(server)*
4-column card grid linking to the four anchored sections of `/what-we-do`.

### `ImpactSection.tsx` *(server)*
3-column story cards with photo placeholders. Replace the placeholder `div`s with `<Image>` components once real photos are available.

### `CallToAction.tsx` *(server)*
Green banner with Donate and Volunteer buttons. Used at the bottom of About, What We Do, and Testimonials pages.

### Form components *(all client)*

| Component | Page | Submits to (Phase 2) |
|-----------|------|----------------------|
| `NewsletterForm` | Footer | API Gateway → Lambda → SES/Mailchimp |
| `VolunteerForm` | Join Us | API Gateway → Lambda → DynamoDB + SES |
| `ContactForm` | Contact | API Gateway → Lambda → SES |
| `DonateAmounts` | Donate | API Gateway → Lambda → Stripe |

All forms currently call `e.preventDefault()` and do nothing — they are ready to be wired to API endpoints by replacing the `handleSubmit` body.

---

## Styling System

### Brand colours

Defined in `tailwind.config.ts` and usable as Tailwind classes everywhere:

| Token | Hex | Class examples |
|-------|-----|----------------|
| `green` | `#1a3a2a` | `bg-green`, `text-green`, `border-green` |
| `green-dark` | `#0f2318` | `bg-green-dark` |
| `green-mid` | `#1e4530` | `bg-green-mid` |
| `green-light` | `#2a5c3f` | `hover:bg-green-light` |
| `gold` | `#c9a227` | `bg-gold`, `text-gold` |
| `gold-light` | `#d4b44a` | `hover:bg-gold-light` |
| `cream` | `#f8f5ef` | `bg-cream` |

Opacity modifiers work on all colours: `bg-green/10`, `text-gold/50`, etc.

### Fonts

| Variable | Font | Usage |
|----------|------|-------|
| `--font-inter` | Inter | Body text (`font-sans`) |
| `--font-playfair` | Playfair Display | Headings (`font-serif`) |

Fonts are loaded in `app/layout.tsx` via `next/font/google` — zero layout shift, automatically self-hosted by Next.js.

### Reusable utility classes (`globals.css`)

These are defined with `@layer components` so they can be used anywhere like any Tailwind class:

| Class | What it does |
|-------|-------------|
| `.btn-gold` | Gold filled button (primary CTA) |
| `.btn-green` | Green filled button (secondary CTA) |
| `.btn-outline` | Transparent button with gold border (used on dark backgrounds) |
| `.section-title` | Centred serif heading, responsive size |
| `.section-subtitle` | Muted centred paragraph below a title |
| `.gold-divider` | Renders a short gold horizontal rule via `::after` pseudo-element |
| `.nav-link` | White uppercase nav item with gold hover |
| `.card` | White bordered card with shadow hover |

---

## AWS Integration Map

The codebase is structured so each AWS service can be wired in independently. Everything marked `// AWS INTEGRATION POINT` in the source is a stub waiting to be connected.

### Phase 1 (now — cheapest)

```
GoDaddy domain → AWS Amplify (hosts the Next.js site)
Contact/Volunteer forms → API Gateway → Lambda → SES (email forwarding)
Analytics → Google Analytics 4 (add GA_ID to .env.local)
```

**To add the contact form email:**
1. Create a Lambda function that accepts `{ name, email, subject, message }` and calls AWS SES
2. Put it behind API Gateway with a POST route `/contact`
3. Set `NEXT_PUBLIC_API_URL` in Amplify environment variables
4. Replace the `handleSubmit` body in `ContactForm.tsx` with a `fetch()` call

### Phase 2 (growing)

```
User accounts → AWS Cognito (supports Google, Facebook, Apple sign-in)
Donations → Stripe (or JazzCash/EasyPaisa for Pakistan)
Dynamic content → Lambda + DynamoDB
File uploads → Lambda + S3 pre-signed URLs
```

**To add Stripe donations:**
1. Add `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` to environment
2. Install `@stripe/stripe-js` and `@stripe/react-stripe-js`
3. Replace `DonateAmounts.tsx` stub with Stripe Elements
4. Create a Lambda that creates payment intents (uses `STRIPE_SECRET_KEY` — server-side only)

### Phase 3 (scale)

```
Route 53 → CloudFront CDN → ECS/EC2 with auto-scaling
RDS Aurora (if relational data needs replace DynamoDB)
Google AdSense (once site meets traffic requirements)
```

---

## Environment Variables

Copy `.env.example` to `.env.local` and fill in values. Never commit `.env.local`.

```bash
copy .env.example .env.local
```

| Variable | Phase | Description |
|----------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | 1 | Base URL of your API Gateway (e.g. `https://abc123.execute-api.ap-south-1.amazonaws.com/prod`) |
| `NEXT_PUBLIC_GA_ID` | 1 | Google Analytics 4 Measurement ID (e.g. `G-XXXXXXXXXX`) |
| `NEXT_PUBLIC_GOOGLE_MAPS_KEY` | 1 | Google Maps embed API key for Contact page |
| `NEXT_PUBLIC_COGNITO_USER_POOL_ID` | 2 | AWS Cognito pool for user accounts |
| `NEXT_PUBLIC_COGNITO_CLIENT_ID` | 2 | Cognito app client ID |
| `NEXT_PUBLIC_COGNITO_DOMAIN` | 2 | Cognito hosted UI domain |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | 2 | Stripe publishable key (safe to expose) |
| `STRIPE_SECRET_KEY` | 2 | Stripe secret key — **never prefix with NEXT_PUBLIC_**, only used in Lambda |
| `SES_FROM_EMAIL` | 1 | Verified SES sender address |

Variables prefixed `NEXT_PUBLIC_` are bundled into the browser JavaScript. Everything else is server-side only — put those in Lambda environment variables, not in the Next.js app.

---

## Deploying to AWS Amplify

### One-time setup

1. Push the project to a GitHub repository
2. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify/) → **New App → Host web app**
3. Connect your GitHub account and select the repository
4. Amplify detects `amplify.yml` automatically — no manual build settings needed
5. Click **Save and deploy**

### Connect the custom domain

1. In Amplify Console → **Domain management → Add domain**
2. Enter `care-pk.com` (or your GoDaddy domain)
3. Amplify shows you a CNAME record — copy it
4. In GoDaddy → **DNS → Add record**:
   - Type: `CNAME`
   - Name: `www` (or `@` for root)
   - Value: the Amplify-provided URL
5. SSL certificate is provisioned automatically by Amplify via AWS Certificate Manager

Propagation takes between 5 minutes and 48 hours.

### Adding environment variables in Amplify

Go to **App settings → Environment variables** and add each key from `.env.example`. Amplify injects them at build time — you do not commit `.env.local` to the repository.

### Re-deploying

Every push to the connected branch triggers an automatic redeploy. No manual steps needed after initial setup.

---

## Phase Roadmap

### Phase 1 — Live (current)
- [x] Full static website (all 9 pages)
- [x] Mobile-responsive layout
- [x] Brand design (green/gold theme)
- [ ] Deploy to AWS Amplify
- [ ] Connect GoDaddy domain
- [ ] Wire contact form to Lambda + SES
- [ ] Add Google Analytics 4

### Phase 2 — Engagement
- [ ] User accounts via AWS Cognito (Google / Facebook sign-in)
- [ ] Online donation portal (Stripe or JazzCash)
- [ ] Volunteer application stored in DynamoDB
- [ ] Admin dashboard to view submissions
- [ ] Blog / news section with dynamic content

### Phase 3 — Scale
- [ ] Move DNS to Route 53 for advanced routing
- [ ] CloudFront CDN for edge caching
- [ ] Google AdSense integration
- [ ] AWS CloudWatch dashboards + alerting
- [ ] WhatsApp/SMS notifications via Twilio

---

## Development Notes

### Adding a new page

1. Create `app/your-page/page.tsx`
2. Export a default React component and a `metadata` export
3. Add the route to the `navLinks` array in `components/Navbar.tsx`
4. Add the route to the quick links map in `components/Footer.tsx`

### Adding a new image

1. Place the file in `public/images/`
2. Use Next.js `<Image>` component (not `<img>`) for automatic optimisation:
   ```tsx
   import Image from "next/image";
   <Image src="/images/your-photo.jpg" alt="description" width={800} height={600} />
   ```

### Replacing photo placeholders

Every `div` with text "Photo Coming Soon" or "Program Photo" is a placeholder. Replace each one with an `<Image>` component pointing to `public/images/your-file.jpg`.

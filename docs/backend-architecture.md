# CARE Pakistan — Backend Architecture Plan

## Guiding Principles
- **Google-first**: use what Workspace already gives you before buying anything extra
- **Zero backend servers now** — API calls happen at build/request time from Next.js
- **Clear GCP migration path** when traffic or complexity demands it
- **Total cost today: ~$7–8/month**

---

## Stack Overview

```
Google Workspace ($6/user/month)
├── Gmail → custom domain email (care@care-pk.org)
├── Google Calendar → events data source
├── Google Sheets → stats + form responses "database"
├── Google Drive → documents, receipts, photos
└── Apps Script → lightweight serverless glue (free)

Next.js on Vercel (free tier)
├── Events page → Google Calendar API (ISR, revalidates hourly)
├── Stats strip → Google Sheets API (ISR, revalidates daily)
└── Contact / Volunteer forms → Apps Script Web App → Gmail alert

Domain
└── Buy through Google Workspace onboarding (Squarespace-managed, ~$12/yr)
    └── DNS auto-wired to Workspace → MX records handled automatically
```

---

## Domain & Email

| What | How |
|---|---|
| **Buy domain** | During Google Workspace sign-up — it walks you through purchasing (e.g. `care-pk.org`) and auto-configures all DNS |
| **Email** | Google Workspace Business Starter → `care@care-pk.org`, `info@care-pk.org` |
| **DNS** | Google manages MX, SPF, DKIM — you get deliverability out of the box, no manual record fiddling |
| **Cost** | $6/user/month + ~$12/year for domain |

> Later you point your GoDaddy domain here too, or let the Google domain replace it entirely.

---

## Events Page — Google Calendar API

### How it works
1. Create a shared **CARE Events** calendar inside Google Workspace
2. Any admin adds an event in Google Calendar (title, date, time, location, description) — that's it, no CMS needed
3. Next.js fetches the calendar at build time using the **Google Calendar API** and renders events with ISR (revalidates every hour)
4. Events appear on the website automatically — no code deploy needed

### What you get free
- 1 million Calendar API requests/day on the free tier
- Recurring events, multi-day events, cancellations — all handled by Google
- Admins never touch the website — they just use Google Calendar like they normally would

### Credential needed
A single **API key** (public, restricted to your domain) — no server required.

### Next.js fetch pattern
```ts
// app/events/page.tsx
// ISR: page rebuilds at most once per hour without a full deploy
export const revalidate = 3600;

const res = await fetch(
  `https://www.googleapis.com/calendar/v3/calendars/${CALENDAR_ID}/events` +
  `?key=${process.env.GOOGLE_CALENDAR_API_KEY}` +
  `&timeMin=${new Date().toISOString()}` +
  `&orderBy=startTime&singleEvents=true&maxResults=20`
);
const { items } = await res.json();
```

---

## Stats Strip — Google Sheets

### How it works
1. One Google Sheet: **CARE Stats** — a simple table:

| metric | value | label |
|---|---|---|
| patients | 500 | Patients Supported |
| volunteers | 50 | Dedicated Volunteers |
| projects | 20 | Projects Completed |
| years | 3 | Years of Service |

2. When a milestone is hit, an admin opens the sheet and updates the number
3. Next.js reads this via **Google Sheets API** with ISR (revalidates every 24 hours)
4. Numbers on the homepage update automatically — no deploy needed

### Why Sheets and not a real database?
- This data changes maybe once a month — a full database is overkill
- The admin already lives in Google Workspace, no new tool to learn
- It's completely free within quota
- When you eventually move to Firestore, the migration is a single script

### Next.js fetch pattern
```ts
// components/Stats.tsx (server-side data fetch)
export const revalidate = 86400; // 24 hours

const res = await fetch(
  `https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/Stats!A2:D10` +
  `?key=${process.env.GOOGLE_SHEETS_API_KEY}`
);
const { values } = await res.json();
```

---

## Contact & Volunteer Forms — Apps Script Web App

### How it works
1. User submits the form on the website
2. Next.js POSTs to a **Google Apps Script Web App URL** (free, serverless HTTP endpoint)
3. The Apps Script:
   - Appends the submission as a new row to a Google Sheet (your lightweight CRM)
   - Sends an email notification to `care@care-pk.org` via Gmail
4. All submissions are visible in Sheets — searchable, filterable, exportable

### Why Apps Script instead of Lambda now?
- Completely free — no billing setup required
- Runs inside Google Workspace, so Gmail sending just works (no SES, no SMTP credentials)
- The Web App URL is your "API endpoint" — swap it for a Cloud Function URL in Phase 2 by changing one environment variable

### Apps Script skeleton
```js
// Code.gs — deployed as Web App (Execute as: Me, Access: Anyone)
function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName("Submissions");
  sheet.appendRow([new Date(), data.name, data.email, data.message]);

  GmailApp.sendEmail(
    "care@care-pk.org",
    "New Contact Form Submission",
    `Name: ${data.name}\nEmail: ${data.email}\nMessage: ${data.message}`
  );

  return ContentService.createTextOutput(JSON.stringify({ success: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

---

## Phase 1 Architecture Diagram

```
User Browser
    │
    ▼
Next.js on Vercel (free)
    │
    ├── GET /events
    │       └── Google Calendar API ──► CARE Events Calendar (Workspace)
    │               ISR: revalidate every 1 hour
    │
    ├── GET / (homepage stats)
    │       └── Google Sheets API ──► CARE Stats Sheet (Workspace)
    │               ISR: revalidate every 24 hours
    │
    ├── POST /api/contact
    │       └── Apps Script Web App ──► Gmail alert + Sheets log
    │
    └── POST /api/volunteer
            └── Apps Script Web App ──► Gmail alert + Sheets log

Google Workspace ($6/mo)
    ├── Gmail      (care@care-pk.org)
    ├── Calendar   (event management by admins)
    ├── Sheets     (stats + form submissions CRM)
    └── Drive      (documents, impact reports, photos)
```

---

## GCP Migration Path

Each phase adds a layer — nothing from the previous phase is thrown away.

| Trigger | What you add | Replaces |
|---|---|---|
| Forms need auto-replies, PDF receipts | **Cloud Functions** | Apps Script Web App |
| Stats need real-time updates | **Firestore** | Google Sheets |
| Need user login (donor portal) | **Firebase Auth** (Google/Social SSO) | — |
| Need online payments | **Cloud Functions** → Stripe / JazzCash | — |
| Traffic grows significantly | Move Next.js to **Cloud Run** | Vercel |
| Need a CDN + custom caching rules | **Cloud CDN** in front of Cloud Run | Vercel Edge |
| Advanced analytics / reporting | **BigQuery** + Looker Studio | — |

> **Key point:** Every Google API used today (Calendar, Sheets, Drive) already speaks GCP natively. Nothing gets thrown away — you just add layers on top.

---

## Environment Variables (to add to `.env.local` and Vercel)

```bash
# Google Calendar
GOOGLE_CALENDAR_API_KEY=         # Restricted to your domain
GOOGLE_CALENDAR_ID=              # e.g. abc123@group.calendar.google.com

# Google Sheets
GOOGLE_SHEETS_API_KEY=           # Same key works if scopes allow
GOOGLE_STATS_SHEET_ID=           # Spreadsheet ID from the URL

# Apps Script
NEXT_PUBLIC_CONTACT_FORM_URL=    # Apps Script Web App deploy URL
NEXT_PUBLIC_VOLUNTEER_FORM_URL=  # Apps Script Web App deploy URL
```

> **Note:** `NEXT_PUBLIC_` prefix exposes the variable to the browser (needed for client-side form POSTs). Calendar and Sheets keys are server-side only (no prefix) since they're used in Server Components.

---

## Cost Summary

| Phase | What's running | Monthly cost |
|---|---|---|
| **Phase 1 (now)** | Google Workspace + Vercel + free APIs | **~$7/mo** |
| **Phase 2** | + Cloud Functions + Firestore | ~$10–15/mo |
| **Phase 3** | Full Cloud Run + CDN + Auth | ~$30–50/mo (scales with traffic) |

---

## Implementation Checklist

### Immediate (Phase 1)
- [ ] Sign up for **Google Workspace Business Starter** — buy `care-pk.org` during setup
- [ ] Set up email aliases: `care@`, `info@`, `donations@`
- [ ] Create **CARE Events** calendar in Workspace, add real upcoming events
- [ ] Create **CARE Stats** Google Sheet with current numbers
- [ ] Enable **Google Calendar API** in Google Cloud Console, create API key
- [ ] Enable **Google Sheets API**, restrict both keys to your domain
- [ ] Wire Calendar API into `/app/events/page.tsx` with ISR
- [ ] Wire Sheets API into `components/Stats.tsx`
- [ ] Write and deploy the **Apps Script Web App** for form submissions
- [ ] Replace `handleSubmit` stubs in `ContactForm.tsx` and `VolunteerForm.tsx`
- [ ] Add all env vars to `.env.local` and Vercel project settings
- [ ] Point GoDaddy domain DNS → Google Workspace (or retire GoDaddy domain)

### Phase 2 (when needed)
- [ ] Set up Firebase project under same Google account
- [ ] Migrate form handling to Cloud Functions
- [ ] Add Firestore for stats (keep Sheets as admin-friendly write interface)
- [ ] Add Firebase Auth for a future donor/volunteer portal

### Phase 3 (when needed)
- [ ] Containerise Next.js and deploy to Cloud Run
- [ ] Set up Cloud CDN
- [ ] Migrate DNS fully to Cloud DNS / Google Domains

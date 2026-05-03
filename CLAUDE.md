# Project: care-pk Website

## Background
The user purchased a domain from GoDaddy (care-pk) and wants to deploy a website on it.
The site has low traffic initially but must be architected to scale as traffic grows.

NGO Name: **CARE — Care, Aid & Rehabilitation in Emergency**
Brand Colors: Dark green (#1a3a2a) and gold/amber (#c9a227)
Contact: info@care.org.pk | +92 300 1234567

---

## Problem
- Domain is on GoDaddy, need to connect it to a cloud host
- Unsure which hosting platform to use (AWS vs alternatives)
- Unsure which AWS service is the right fit (Amplify vs S3+CloudFront vs EC2)
- Unsure when and why APIs (Lambda + API Gateway) would be needed

---

## Decisions Made

### Hosting Platform
**Chosen: AWS Amplify** (recommended for this project)

Reasons:
- Supports full-stack apps (frontend + backend/APIs in one place)
- Auto-deploys from GitHub on every push (CI/CD built-in)
- Scales automatically with zero configuration
- Free tier covers low-traffic phase
- Easiest AWS option to start with and migrate away from later if needed

### Why Not the Others
- **S3 + CloudFront**: Great for purely static sites, but no backend support. Would need separate Lambda + API Gateway setup anyway.
- **EC2**: Full Linux server, too much overhead for early stage. Costs money even when idle. No auto-scaling without extra setup.

### Frontend Framework
**Chosen: Next.js (React)**
- Static export for Phase 1 (Amplify hosts it for near-free)
- Same codebase flips to SSR/API routes in Phase 2 without rewrite
- Great SEO out of the box (important for NGO discoverability)

---

## Site Pages & Sections (from design mockups)
- **Home**: Hero slider, stats counter, What We Do, impact section
- **About Us**: Mission, story
- **Our Team**: Core team, Board of Governors, Advisory Board
- **What We Do**: Emergency Aid, Patient Support, Rehabilitation, Community Outreach
- **Events**: Upcoming events & workshops
- **Testimonials**: Written + video testimonials
- **Join Us**: Volunteer/join form
- **Donate**: Bank details + online payment
- **Contact**: Contact form

---

## Planned Architecture

### Phase 1 (Now — Low Traffic)
```
GoDaddy Domain (DNS CNAME)
      ↓
AWS Amplify
  ├── Frontend (Next.js static export)
  └── Contact form → Lambda + SES
```

### Phase 2 (Growing Traffic)
```
GoDaddy Domain
      ↓
AWS Amplify (frontend)
      ↓
API Gateway + Lambda (serverless backend APIs)
      ↓
DynamoDB / RDS (database)
```

### Phase 3 (Scale)
```
Route 53 (DNS management)
      ↓
CloudFront (CDN)
      ↓
ECS / EC2 with Auto Scaling Groups
      ↓
RDS / Aurora (managed DB)
```

---

## Features Roadmap (→ Require Lambda + API Gateway)

| Feature | AWS Service | Phase |
|---|---|---|
| Contact form | Lambda + SES (email) | 1 |
| Newsletter signup | Lambda + Mailchimp/SendGrid | 1 |
| User login/signup | Cognito (Google/Social auth) | 2 |
| Dynamic content (blog, events) | Lambda + DynamoDB | 2 |
| File/image uploads | Lambda + S3 pre-signed URLs | 2 |
| Payment processing (donations) | Lambda + Stripe / JazzCash | 2 |
| SMS/WhatsApp notifications | Lambda + Twilio | 3 |
| Analytics | Google Analytics 4 + CloudWatch | 1 |
| Ads | Google AdSense | 3 |

---

## Domain Setup (GoDaddy → AWS Amplify)

1. Deploy site on AWS Amplify
2. Amplify gives you a DNS CNAME record
3. Go to GoDaddy → My Products → DNS
4. Add/update the CNAME record to point to Amplify's provided URL
5. Enable custom domain inside Amplify console (it handles SSL via ACM automatically)
6. Propagation takes 5 minutes to 48 hours

---

## Key Principle
> Start simple. Only add complexity (Lambda, EC2, Auto Scaling) when traffic or features actually demand it — not prematurely.

---

## Next Steps
- [ ] Scaffold Next.js project matching brand design (green/gold theme, all pages)
- [ ] Create AWS account and enable Amplify
- [ ] Push project to GitHub
- [ ] Connect GitHub repo to Amplify
- [ ] Configure custom domain in Amplify and update GoDaddy DNS
- [ ] Add contact form with Lambda + SES as first backend feature

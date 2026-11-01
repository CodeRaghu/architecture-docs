# HCM / Payroll / Tax for CPAs: Kickoff Notes

Status: draft for discussion (2026-10-07). Nothing here is decided yet.

## 1. Two products hiding in one idea

What you described covers two businesses with different rules. Picking which one comes first is the biggest decision you'll make.

| | **A. Tax prep for CPAs** (scan W-2s and pay stubs, fill 1040 and related forms, CPA reviews, e-file) | **B. Payroll / HCM** (run payroll for employer clients, withhold and remit taxes, file 941/940/W-2, time, benefits, talent) |
|---|---|---|
| Matches your OCR and form-filling goal | Directly | Only partly (onboarding docs, W-4, I-9) |
| Moves client money | No | Yes, unless a partner handles it |
| Main approval to go live | IRS e-file: software developer ETIN plus passing IRS ATS testing each tax year | Federal and state agency registrations, plus a banking or payroll partner for money movement |
| Texas angle | Texas has no state personal income tax, so year one is federal only | Texas has no state income tax withholding, but employers pay Texas Workforce Commission unemployment tax (quarterly C-3) |
| Rough effort for an MVP | Smaller | Much larger |

**My suggestion:** start with A (scan, extract, fill, CPA review, export or e-file), and add payroll later through a partner API instead of building money movement yourself.

## 2. What going live needs (paid public SaaS handling tax data)

**Legal and business**
- Company formation (LLC or C-corp), EIN, business bank account
- Terms of Service, Privacy Policy, Data Processing Agreement for CPA firms
- Errors and omissions plus cyber liability insurance
- Trademark search for the product name (USPTO) and domain

**Tax and payroll specific compliance**
- **FTC Safeguards Rule (GLBA):** tax preparers and their vendors must have a written information security program, MFA, encryption, and breach notification. CPA firms will ask you about it.
- **IRS Publication 4557** (safeguarding taxpayer data) and **Publication 1345** (e-file rules)
- **IRS e-file (MeF):** apply as a Software Developer for an ETIN, pass the Assurance Testing System each filing season, follow the MeF XML schemas
- **IRC section 7216:** rules on using or disclosing tax return information. This limits analytics and any AI training on client data.
- **SOC 2 Type II:** not legally required, but most CPA firms will expect it before trusting you with client SSNs. Plan for Type I first, then Type II.
- If you ever hold or move payroll funds: money transmitter licensing (Texas Department of Banking and other states). The usual way to avoid this is a payroll or embedded-payments partner.

**Taking payment for plans**
- Use Stripe Billing (or Paddle or Chargebee) with hosted checkout, so card data never touches your servers and PCI scope stays at the simplest level (SAQ A)
- Plan design: per CPA seat, per client, or per return, with a free trial
- Sales tax: Texas taxes SaaS (as data processing, 80% of the price is taxable). Stripe Tax or a similar tool can handle collection.

**Security and operations**
- Encrypt SSNs and documents at rest (KMS-managed keys), with field-level encryption for SSN and bank numbers
- MFA for every user, role-based access per CPA firm, full audit log of who viewed or edited what
- Automated backups with tested restore, a data retention and deletion policy
- Monitoring and alerting, an incident response plan, yearly penetration test
- US-only data residency

## 3. Reading scanned documents

Prebuilt models for W-2 and similar forms already exist, so you shouldn't train your own at first:
- **Azure AI Document Intelligence:** prebuilt US tax models (W-2, 1098, 1099 variants, 1040)
- **Google Document AI:** W-2 and other lending and tax parsers
- **AWS Textract:** Analyze Lending and Analyze Expense, with forms and tables
- **LLM vision models** (Claude and others): good for messy pay stubs that have no fixed layout. Pair them with validation rules and confidence scores.

The workflow: upload, then classify, extract, validate (for example, check that the W-2 box math adds up and SSN format is right), then the CPA reviews flagged fields side by side with the image, then fill the form.

Filling forms: IRS publishes fillable PDFs, which libraries like `pypdf` or `PyMuPDF` can fill. E-filing needs MeF XML instead of PDF.

## 4. Technology picks (current and widely used)

| Layer | Suggested | Alternatives |
|---|---|---|
| Backend language | **Python 3.12+** (your preference fits well) | TypeScript/Node, Go, C#/.NET, Java/Kotlin |
| Backend framework | **Django + Django REST Framework** (built-in admin, auth, ORM, mature) | FastAPI (lighter, async, very popular for APIs) |
| Frontend | **React + TypeScript with Next.js**, Tailwind CSS, shadcn/ui components | Vue/Nuxt, SvelteKit, Angular |
| Forms UI | React Hook Form + Zod validation | |
| Database | **PostgreSQL** | |
| Background jobs | Celery + Redis, or Temporal for long multi-step workflows | Dramatiq, AWS Step Functions |
| File storage | S3 (encrypted) | Azure Blob, GCS |
| Auth | Auth0, Clerk, or AWS Cognito, with MFA required | Django built-in auth with an MFA add-on |
| Payments | Stripe Billing + Stripe Tax | Paddle, Chargebee |
| Cloud | **AWS** (broadest compliance tooling) | Azure (pairs with Document Intelligence), GCP |
| Infrastructure | Docker, Terraform, GitHub Actions for CI/CD | Pulumi, AWS CDK |
| Observability | Sentry, Datadog or Grafana | |

## 5. GitHub options for private developer access

Create a **GitHub Organization** (not a personal account), make repos private, and add developers as members through teams.

| Plan | Price (per user/month, check current pricing) | What you get |
|---|---|---|
| Free | $0 | Unlimited private repos and collaborators, but branch protection and required reviews are limited on private repos |
| **Team** (recommended) | about $4 | Protected branches and rulesets on private repos, required reviewers, CODEOWNERS, more Actions minutes |
| Enterprise | about $21 | SAML single sign-on, audit log streaming, enterprise-wide policies. Worth it later, around SOC 2 time. |

Add-ons worth turning on: **Secret Protection** (blocks pushed secrets), **Code Security** (code scanning), Dependabot, required 2FA for the organization, and GitHub Actions environments with approval gates for production deploys. Never put real client data in the repo or test fixtures.

## 6. Name ideas

Check each for trademark and domain availability before falling in love with one.
- **Clearfile**: plain and says what it does
- **Formwise**: smart form filling
- **TallyDesk**: a CPA's workbench
- **Ledgerlight**: lighter bookkeeping and tax work
- **LoneStar Ledger**: Texas-first, but harder to grow beyond Texas
- **Docufile CPA**: scanned documents to filed returns
- **Wagewise**: fits if payroll becomes the main product

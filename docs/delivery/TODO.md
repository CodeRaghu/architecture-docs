# PayNTax: Project TODO List

> Working name **PayNTax** until a product name is picked (see [kickoff notes §6](../planning/01-kickoff-notes.md)).
> Source plans: [01-kickoff-notes.md](../planning/01-kickoff-notes.md), [02-draft-plan.md](../planning/02-draft-plan.md).
> How we work through this list: [delivery-plan.md](delivery-plan.md).

**Scope for 2026:** tax prep for solo CPAs, Texas clients (federal only). Scan W-2s and pay stubs, extract fields, CPA reviews them, fill the 1040, download the PDF, paid signup.
**Pilot launch:** Friday **18 Dec 2026**. E-file and business returns follow in 2027. Payroll/HCM comes later, through a partner API.

## How to use this file

- Tick `[x]` in the same PR that finishes the work. Each PR description links the item (for example `TODO S3.4`).
- **Owner** is a role until names are assigned. **PO** is the product owner (you), **BE** backend, **FE** frontend, **QA** QA and DevOps. On a 2–4 person team, one person may hold several roles.
- ⏱ marks **long-lead items**. Start them in week 1, because outside parties set their timelines.
- An item is done only when it meets the [Definition of Done](delivery-plan.md#definition-of-done).

## Milestones

| # | Milestone | Target date | Exit criteria |
|---|---|---|---|
| M0 | Foundations ready | Fri 6 Nov | Repo, CI, dev setup working for everyone; IRS e-Services and ETIN applications submitted |
| M1 | Document intake works end to end | Fri 20 Nov | Upload a synthetic W-2, see extracted fields with confidence flags |
| M2 | CPA review complete | Fri 4 Dec | CPA corrects fields side by side; every change is audit logged |
| M3 | 1040 PDF and billing | Fri 11 Dec | Reviewed data fills a 1040 PDF; Stripe subscription signup works |
| M4 | **Pilot launch** | **Fri 18 Dec** | Production live, 2–3 pilot CPAs onboarded, WISP, ToS and Privacy Policy published |
| M5 | IRS ATS passed for 1040 | Feb 2027 | MeF XML accepted in ATS; e-file goes live |
| M6 | Business returns | Q1–Q2 2027 | 1120-S, then 1065 |

---

## Phase 1: Foundations (Sprint 1, 2–6 Nov)

### Business and compliance (start now)
- [ ] ⏱ **S1.1** Create an IRS e-Services account (PO)
- [ ] ⏱ **S1.2** Submit an IRS e-file application as Software Developer to get an ETIN (can take ~45 days) (PO)
- [ ] ⏱ **S1.3** Pick the product name: USPTO trademark search plus domain check, then register the domain (PO)
- [ ] ⏱ **S1.4** Form the company (LLC or C-corp), get an EIN, open a business bank account (PO)
- [ ] ⏱ **S1.5** Get quotes for E&O and cyber liability insurance (PO)
- [ ] **S1.6** Decide pricing model (per seat, per client, or per return) and trial length; record it as an ADR (PO)

### Engineering setup
- [ ] **S1.7** Create the GitHub Organization (Team plan), add members via teams, require 2FA (PO)
- [ ] **S1.8** Create the private app repo `payntax-app` (monorepo: `backend/`, `frontend/`, `infra/`) (BE)
- [ ] **S1.9** Branch protection on `main`: PR required, 1 reviewer, passing CI, CODEOWNERS (QA)
- [ ] **S1.10** Turn on Secret Protection, Code Security (code scanning), and Dependabot (QA)
- [ ] **S1.11** Scaffold Django + DRF backend and Next.js + TypeScript frontend (BE, FE)
- [ ] **S1.12** `docker compose` local stack: Postgres, Redis, MinIO (S3 stand-in), backend, worker, frontend (BE)
- [ ] **S1.13** CI with GitHub Actions: lint, type check, unit tests, build on every PR (QA)
- [ ] **S1.14** Make [Development Setup](../setup/development-setup.md) work from a clean laptop; each team member signs off (All)
- [ ] **S1.15** Write ADRs: stack, auth provider, OCR provider, cloud region (BE)

**Sprint 1 exit = M0**

## Phase 2: Document intake and review (Sprints 2–5, 9 Nov – 4 Dec)

### Sprint 2 (9–13 Nov): infrastructure, accounts, uploads
- [ ] **S2.1** Terraform: AWS account structure (dev, staging, prod), VPC, RDS Postgres, S3 with KMS, ECS Fargate (QA)
- [ ] **S2.2** Deploy to `dev` automatically on merge to `main` (QA)
- [ ] **S2.3** Auth with MFA required; firm and user model; roles (Owner, Preparer) (BE)
- [ ] **S2.4** Screens: sign up, log in, MFA setup ([SCR-01, SCR-02](../screens/README.md)) (FE)
- [ ] **S2.5** Client list and "new client" ([SCR-04, SCR-05](../screens/README.md)) (FE, BE)
- [ ] **S2.6** Synthetic test data: W-2 generator (PDF and scanned-look image) with matching ground-truth JSON (QA)
- [ ] **S2.7** Audit log model: who viewed or edited what, and when (BE)

### Sprint 3 (16–20 Nov): extraction
- [ ] **S3.1** Document upload (PDF, JPG, PNG; size limits; virus scan) to encrypted S3 ([SCR-07](../screens/README.md)) (FE, BE)
- [ ] **S3.2** Background job pipeline (Celery): classify, then extract, then validate (BE)
- [ ] **S3.3** OCR spike: compare AWS Textract and Azure Document Intelligence on the synthetic W-2 set; record result as an ADR (BE)
- [ ] **S3.4** W-2 extraction into a typed model, with a confidence score per field (BE)
- [ ] **S3.5** Field-level encryption for SSN and EIN (BE)
- [ ] **S3.6** Extraction accuracy harness: compare against ground truth, report per-field accuracy in CI (QA)

**Sprint 3 exit = M1**

### Sprint 4 (23–27 Nov, short week for Thanksgiving)
- [ ] **S4.1** Pay stub extraction with an LLM vision model (ADP-style synthetic stubs), schema-validated output (BE)
- [ ] **S4.2** Validation rules: SSN and EIN format, W-2 box math, year-to-date totals versus W-2 (BE)
- [ ] **S4.3** Synthetic ADP-style pay stub generator with several layouts (QA)
- [ ] **S4.4** Document list with status chips ([SCR-07](../screens/README.md)) (FE)

### Sprint 5 (30 Nov – 4 Dec): CPA review
- [ ] **S5.1** Side-by-side review screen: image on the left, fields on the right, low-confidence fields highlighted ([SCR-08](../screens/README.md)) (FE)
- [ ] **S5.2** Save corrections; keep the original extracted value and the corrected value; log to audit (BE)
- [ ] **S5.3** "Mark reviewed" gate: a return can't be prepared until all its documents are reviewed (BE)
- [ ] **S5.4** E2E test: upload, extract, review (Playwright) (QA)
- [ ] **S5.5** Deploy to `staging`; first internal demo with a friendly CPA (PO)

**Sprint 5 exit = M2**

## Phase 3: Form preparation and paid launch (Sprints 6–7, 7–18 Dec)

### Sprint 6 (7–11 Dec)
- [ ] **S6.1** Return workspace per client and tax year ([SCR-06](../screens/README.md)) (FE, BE)
- [ ] **S6.2** Map reviewed W-2 data to 1040 lines (wages, withholding); common W-2-only returns (BE)
- [ ] **S6.3** Fill the IRS fillable 1040 PDF; edit and recalculate; download ([SCR-09](../screens/README.md)) (BE, FE)
- [ ] **S6.4** Stripe Billing with hosted checkout plus Stripe Tax (Texas SaaS sales tax) ([SCR-03](../screens/README.md)) (BE)
- [ ] **S6.5** Firm settings: users, MFA reset, billing portal link ([SCR-10](../screens/README.md)) (FE)
- [ ] **S6.6** Golden-return tests: known inputs must produce the expected 1040 values (QA)

**Sprint 6 exit = M3**

### Sprint 7 (14–18 Dec): hardening and launch
- [ ] **S7.1** Write the WISP (FTC Safeguards Rule), incident response plan, data retention policy (PO)
- [ ] **S7.2** Publish Terms of Service, Privacy Policy, and the DPA for CPA firms (PO)
- [ ] **S7.3** Security checks: OWASP ZAP scan, dependency audit, access review, backup restore test (QA)
- [ ] **S7.4** Production deploy with an approval gate; monitoring and alerts (Sentry, CloudWatch) (QA)
- [ ] **S7.5** UAT with 2–3 pilot CPAs on synthetic data, then on their own consenting clients (PO)
- [ ] **S7.6** Fix launch-blocking bugs only; everything else goes to the backlog (All)
- [ ] **S7.7** Go/no-go meeting Thu 17 Dec; launch Fri 18 Dec (PO)

**Sprint 7 exit = M4 🚀**

## Phase 4: E-file and business returns (2027)

- [ ] ⏱ **P4.1** ETIN approved; register for ATS for tax year 2026 (PO)
- [ ] **P4.2** Generate MeF XML for 1040 against the IRS schemas (BE)
- [ ] **P4.3** Transmit and acknowledgment handling (accepted or rejected, with reject codes) (BE)
- [ ] **P4.4** Pass ATS test scenarios for 1040 (QA)
- [ ] **P4.5** Go live with 1040 e-file (M5) (All)
- [ ] **P4.6** 1120-S, then 1065 (extraction, forms, ATS per return type) (All)
- [ ] **P4.7** SOC 2 readiness: Type I, then Type II (PO, QA)
- [ ] **P4.8** Yearly penetration test (QA)

## Later: Payroll / HCM

- [ ] **L.1** Evaluate payroll and embedded-payments partners, so we don't hold client funds (avoids money transmitter licensing)
- [ ] **L.2** Texas Workforce Commission (TWC) unemployment tax, quarterly C-3
- [ ] **L.3** Forms 941, 940, W-2 filing through the partner

## Open decisions

| # | Decision | Options | Needed by | Owner |
|---|---|---|---|---|
| D1 | Product name | See kickoff §6 | S1 | PO |
| D2 | Auth provider | Cognito, Auth0, Clerk | S2 start | BE |
| D3 | OCR provider | Textract, Azure Document Intelligence, Google Document AI | End of S3 | BE |
| D4 | Background jobs | Celery + Redis, or Temporal | S2 start | BE |
| D5 | Pricing model and trial | Per seat, per client, per return | S6 start | PO |
| D6 | Team names for each role | | S1 | PO |

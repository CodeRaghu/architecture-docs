# Draft Plan: Tax Prep for Solo CPAs (v0.1, 2026-10-07)

## Decisions so far
- First product: tax prep (payroll and HCM come later)
- Returns: both individual and business. Suggested order: 1040 first, then 1120-S and 1065.
- Filing: IRS e-file
- Users: solo CPAs, starting with Texas clients (no state income tax, so federal only at first)
- Target: third week of December 2026
- Pricing, team and budget: to be decided later
- Test data: no real documents. We'll make synthetic W-2s and ADP-style pay stubs.

## Timing reality check
- **IRS e-file approval takes a while.** You need an IRS e-Services account and an e-file application as Software Developer (it can take up to about 45 days). Then you pass Assurance Testing (ATS) for the 2026 tax year. ATS usually opens in November, and every return type (1040, 1120-S, 1065) is tested separately.
- **A full tax calculation engine is a multi-year effort.** By December, a realistic goal is: scan documents, extract data, CPA reviews it, the 1040 fills from that data for common W-2 returns, and the CPA downloads the forms. E-file and business returns follow in early 2027.

## Steps

1. **Foundations** (start now, because these have long lead times)
   - Pick the name, set up the domain, form the company and get an EIN
   - Apply for the IRS e-Services account and e-file Software Developer ETIN
   - Create the GitHub organization (Team plan) and repo, with CI and branch rules
   - Pick the stack: Django, Next.js, Postgres, AWS. Set the security baseline: MFA, encryption, audit log.

2. **Document intake and review**
   - Upload W-2s and pay stubs, sort them by type, extract fields (with an OCR service, plus an LLM for pay stubs in any layout)
   - Validation rules and confidence flags
   - Side-by-side review screen where the CPA corrects fields
   - Synthetic test set (W-2s and ADP-style pay stubs)

3. **Form preparation and paid launch** (December target)
   - Client and return workspace for each CPA
   - 1040 and common schedules filled from reviewed data, editable, downloadable as PDF
   - Stripe subscription signup, Terms of Service, privacy policy, and a written security program (WISP)
   - Pilot with a few solo CPAs

4. **E-file and business returns** (early 2027)
   - MeF XML generation, pass IRS ATS, go live with e-file for 1040
   - Then 1120-S and 1065, then SOC 2 readiness

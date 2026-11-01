# Requirements

Each requirement has an ID, a priority, acceptance criteria, and links to its screen and test cases.
Status values: `Draft` → `Ready` → `In progress` → `Done`.

**ID format:** `REQ-<AREA>-<NNN>`. Areas: `ACC` accounts and firms, `CLI` clients and returns, `DOC` document intake, `EXT` extraction and validation, `REV` CPA review, `FRM` form preparation, `BIL` billing, `SEC` security and compliance, `EFL` e-file (2027).

Priority (MoSCoW) is for the **18 Dec pilot launch**: Must, Should, Could, Won't (this release).

## Epics

| Epic | Area | Sprint | Release |
|---|---|---|---|
| Accounts, firms and MFA | ACC | S2 | Pilot |
| Clients and returns | CLI | S2, S6 | Pilot |
| Document intake | DOC | S3–S4 | Pilot |
| Extraction and validation | EXT | S3–S4 | Pilot |
| CPA review | REV | S5 | Pilot |
| 1040 preparation and PDF | FRM | S6 | Pilot |
| Billing | BIL | S6 | Pilot |
| Security and compliance | SEC | All | Pilot |
| E-file (MeF) | EFL | 2027 | Later |
| Business returns (1120-S, 1065) | — | 2027 | Later |
| Payroll / HCM | — | Later | Later |

## Functional requirements

| ID | Requirement | Priority | Screen | Status |
|---|---|---|---|---|
| REQ-ACC-001 | A CPA can sign up and create a firm | Must | SCR-01 | Draft |
| REQ-ACC-002 | Every user must set up MFA before seeing client data | Must | SCR-02 | Draft |
| REQ-ACC-003 | Firm owner can invite users and assign role Owner or Preparer | Should | SCR-10 | Draft |
| REQ-CLI-001 | CPA can create, search and edit clients | Must | SCR-04, SCR-05 | Draft |
| REQ-CLI-002 | CPA can open a return for a client and tax year | Must | SCR-06 | Draft |
| REQ-DOC-001 | Upload PDF, JPG or PNG (max 20 MB each, multiple at once) | Must | SCR-07 | Draft |
| REQ-DOC-002 | Uploads are virus scanned and stored encrypted | Must | — | Draft |
| REQ-DOC-003 | System classifies each document (W-2, pay stub, other) | Must | SCR-07 | Draft |
| REQ-EXT-001 | Extract all W-2 boxes with a confidence score per field | Must | SCR-08 | Draft |
| REQ-EXT-002 | Extract pay stub fields (employer, period, gross, taxes, YTD) | Should | SCR-08 | Draft |
| REQ-EXT-003 | Validate SSN and EIN format, W-2 box math, YTD vs W-2 | Must | SCR-08 | Draft |
| REQ-REV-001 | CPA sees the document image beside the extracted fields | Must | SCR-08 | Draft |
| REQ-REV-002 | Low-confidence and failed-validation fields are highlighted | Must | SCR-08 | Draft |
| REQ-REV-003 | Corrections keep both original and corrected values | Must | SCR-08 | Draft |
| REQ-REV-004 | A document must be marked reviewed before it feeds the return | Must | SCR-08 | Draft |
| REQ-FRM-001 | Fill 1040 from reviewed W-2 data for W-2-only returns | Must | SCR-09 | Draft |
| REQ-FRM-002 | CPA can edit 1040 lines; edits are audit logged | Must | SCR-09 | Draft |
| REQ-FRM-003 | Download the filled 1040 as PDF | Must | SCR-09 | Draft |
| REQ-BIL-001 | Subscription signup through Stripe hosted checkout with trial | Must | SCR-03 | Draft |
| REQ-BIL-002 | Texas sales tax collected through Stripe Tax | Must | SCR-03 | Draft |
| REQ-BIL-003 | Firm owner manages billing in the Stripe customer portal | Should | SCR-10 | Draft |
| REQ-SEC-001 | Audit log of every view and edit of client data, viewable by firm owner | Must | SCR-11 | Draft |
| REQ-EFL-001 | Generate MeF XML for 1040 and transmit | Won't | — | Draft |

## Non-functional requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-SEC-001 | Encryption at rest (KMS) for database and S3; field-level encryption for SSN, EIN, bank numbers | 100% |
| NFR-SEC-002 | TLS 1.2+ everywhere; HSTS | 100% |
| NFR-SEC-003 | Data stays in US AWS regions | 100% |
| NFR-SEC-004 | Tenant isolation: a firm can never see another firm's data | Tested every release |
| NFR-PRV-001 | No client data used for analytics or AI training (IRC §7216) | Policy + code review |
| NFR-PERF-001 | W-2 extraction finishes within 60 s of upload (p95) | 60 s |
| NFR-PERF-002 | Page loads under 2 s (p95) on broadband | 2 s |
| NFR-ACC-001 | Extraction accuracy on synthetic W-2 set | ≥ 98% of fields exact |
| NFR-AVL-001 | Availability during tax season | 99.5% |
| NFR-BKP-001 | Backups daily; restore tested monthly; RPO 24 h, RTO 4 h | — |
| NFR-A11Y-001 | WCAG 2.1 AA for all screens | — |

## Template for a detailed requirement

Copy into `docs/requirements/REQ-<AREA>-<NNN>.md` when a requirement needs more than one table row.

```markdown
# REQ-XXX-000: Title

- **Priority:** Must | Should | Could | Won't
- **Status:** Draft
- **Screens:** SCR-..
- **Tests:** TC-..

## User story
As a <role>, I want <capability> so that <benefit>.

## Acceptance criteria
- Given <context>, when <action>, then <result>.

## Notes / compliance
```

# ADR-0002: Application stack: Django, Next.js, PostgreSQL, AWS

- **Status:** Proposed
- **Date:** 2026-10-31
- **Deciders:** PO, BE, FE
- **TODO item:** S1.15

## Context

Small team (2–4), 7 weeks to a pilot, handling tax data under the FTC Safeguards Rule and IRS Pub 4557. Python is the preferred language. See [kickoff notes §4](../../planning/01-kickoff-notes.md).

## Options considered

| Layer | Proposed | Alternatives |
|---|---|---|
| Backend | Django + DRF (admin, auth, ORM, migrations built in) | FastAPI |
| Frontend | Next.js + TypeScript, Tailwind, shadcn/ui, React Hook Form + Zod | Vue/Nuxt, SvelteKit |
| Database | PostgreSQL | — |
| Jobs | Celery + Redis | Temporal (ADR-0005) |
| Cloud | AWS (broadest compliance tooling) | Azure, GCP |
| Infrastructure | Docker, Terraform, GitHub Actions | Pulumi, AWS CDK |

## Decision

Proposed as above, to be confirmed in sprint 1 planning.

## Consequences

- Django admin gives us internal tools for free in the pilot.
- Two languages (Python and TypeScript) across the team.
- If Azure Document Intelligence wins the OCR spike (ADR-0004), it is called from AWS; data then leaves AWS, which needs a DPA and a US region.

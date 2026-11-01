# Architecture

**Status: proposed.** Items marked "ADR pending" are open decisions in the [TODO list](../delivery/TODO.md#open-decisions).

## Diagram conventions

| Diagram type | Tool | Source |
|---|---|---|
| Cloud and infrastructure (AWS icons) | [Diagrams](https://diagrams.mingrammer.com/) (Python) | [`diagrams/*.py`](../../diagrams), rendered to `docs/assets/*.png` by `make diagrams` and CI |
| Sequences, flows, states, data model, timeline | [Mermaid](https://mermaid.js.org/) | Written inside the Markdown; GitHub and the docs site render it |
| Screen layouts | Text wireframes | [docs/screens](../screens/README.md) |

Why two tools: see [ADR-0001](adr/0001-diagrams-as-code.md).

## AWS architecture

![PayNTax AWS architecture](../assets/aws_architecture.png)

| Component | Choice | Notes |
|---|---|---|
| Edge | Route 53, WAF, CloudFront | TLS 1.2+, rate limiting, AWS managed rule sets |
| Web | Next.js on ECS Fargate | Server-side rendering; no client data cached at the CDN |
| API | Django + DRF on ECS Fargate | Tenant scoping on every query (firm ID) |
| Workers | Celery on ECS Fargate, Redis (ElastiCache) as broker | Classify, extract, validate, fill PDFs |
| Database | RDS PostgreSQL, Multi-AZ in prod, encrypted | Field-level encryption for SSN, EIN, bank numbers |
| Documents | S3 with SSE-KMS, block public access, versioning | Upload and download through short-lived pre-signed URLs |
| OCR | AWS Textract (ADR pending vs Azure Document Intelligence) | Decided by the S3.3 accuracy spike |
| Pay stubs | LLM vision model with schema-validated output | No client data retained for training (IRC §7216) |
| Auth | Cognito, Auth0 or Clerk (ADR pending) | MFA required for every user |
| Billing | Stripe Billing + Stripe Tax, hosted checkout | Card data never touches our servers (PCI SAQ A) |
| Secrets and keys | Secrets Manager, KMS | Separate keys per environment |
| Observability | CloudWatch, CloudTrail, Sentry | Logs scrubbed of SSN and EIN patterns |
| Region | US only (us-east-2 proposed) | Data residency requirement |

## CI/CD

![PayNTax CI/CD pipeline](../assets/cicd_pipeline.png)

See [delivery plan §5](../delivery/delivery-plan.md#5-branching-and-releases) for branching and environments.

## Data model (first draft)

```mermaid
erDiagram
    FIRM ||--o{ USER : has
    FIRM ||--o{ CLIENT : serves
    FIRM ||--|| SUBSCRIPTION : pays
    CLIENT ||--o{ TAX_RETURN : files
    TAX_RETURN ||--o{ DOCUMENT : uses
    DOCUMENT ||--o{ EXTRACTED_FIELD : yields
    EXTRACTED_FIELD ||--o{ FIELD_CORRECTION : "corrected by"
    TAX_RETURN ||--o{ FORM_LINE : produces
    USER ||--o{ AUDIT_EVENT : creates

    FIRM { uuid id string name string stripe_customer_id }
    USER { uuid id uuid firm_id string email string role bool mfa_enabled }
    CLIENT { uuid id uuid firm_id string name bytes ssn_encrypted string filing_status }
    TAX_RETURN { uuid id uuid client_id int tax_year string form_type string status }
    DOCUMENT { uuid id uuid return_id string s3_key string doc_type string status }
    EXTRACTED_FIELD { uuid id uuid document_id string name string value float confidence bool flagged }
    FIELD_CORRECTION { uuid id uuid field_id string old_value string new_value uuid user_id datetime at }
    FORM_LINE { uuid id uuid return_id string line string value string source }
    AUDIT_EVENT { uuid id uuid user_id string action string object_type uuid object_id datetime at }
```

The upload-to-1040 sequence and document lifecycle are in [screens](../screens/README.md#main-user-flow-from-upload-to-1040).

## Architecture Decision Records

Decisions are recorded in [`adr/`](adr). Copy [the template](adr/0000-template.md) to `adr/NNNN-short-title.md`.

| ADR | Title | Status |
|---|---|---|
| [0001](adr/0001-diagrams-as-code.md) | Diagrams as code: Diagrams for cloud, Mermaid for the rest | Accepted |
| [0002](adr/0002-application-stack.md) | Application stack: Django, Next.js, PostgreSQL, AWS | Proposed |
| 0003 | Auth provider | Pending (TODO D2) |
| 0004 | OCR provider | Pending (TODO D3) |
| 0005 | Background jobs: Celery or Temporal | Pending (TODO D4) |

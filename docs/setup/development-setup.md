# Development Setup

Two repositories:

| Repo | Purpose |
|---|---|
| `architecture-docs` (this repo) | Plans, TODO list, requirements, screens, test strategy, architecture diagrams |
| `payntax-app` (to be created, TODO S1.8) | Application code: `backend/` (Django), `frontend/` (Next.js), `infra/` (Terraform) |

## 1. Tools to install (macOS)

```bash
brew install git python@3.12 node@20 graphviz terraform awscli pre-commit
```

```bash
brew install --cask docker
```

| Tool | Version | Used for |
|---|---|---|
| Python | 3.12+ | Backend and diagrams |
| Node.js | 20 LTS | Frontend |
| Docker Desktop | latest | Local Postgres, Redis, MinIO |
| Graphviz | latest | Rendering architecture diagrams |
| Terraform | 1.9+ | AWS infrastructure |
| AWS CLI | v2 | Deploys (`dev` profile only on laptops) |
| pre-commit | latest | Lint and secret scan before each commit |

Editor: VS Code with Python, Pylance, ESLint, Prettier, Mermaid preview, and Docker extensions.

## 2. This docs repo

```bash
git clone -b feature/claude-integration https://github.com/CodeRaghu/architecture-docs.git
```

```bash
cd architecture-docs && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Render the architecture diagrams to `docs/assets/`:

```bash
make diagrams
```

Preview the docs site locally at http://localhost:8000:

```bash
make serve
```

Mermaid diagrams inside Markdown render directly on GitHub and on the docs site. Diagrams-as-code (Python) are rendered to PNG; commit the PNGs together with the `.py` changes so GitHub shows the latest picture.

## 3. Application repo (once S1.8 and S1.12 are done)

Planned layout:

```text
payntax-app/
├── backend/            Django + DRF, Celery workers
│   ├── apps/           accounts, firms, clients, documents, extraction, returns, billing, audit
│   └── tests/
├── frontend/           Next.js + TypeScript, Tailwind, shadcn/ui, React Hook Form + Zod
│   └── e2e/            Playwright tests
├── infra/              Terraform: envs/dev, envs/staging, envs/prod
├── testdata/           Synthetic W-2 and pay stub generators + ground truth (never real data)
├── docker-compose.yml  postgres, redis, minio, backend, worker, frontend
└── .github/workflows/  ci.yml, deploy.yml
```

Run the full stack locally:

```bash
cp .env.example .env && docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000/api |
| Django admin | http://localhost:8000/admin |
| MinIO console (local S3) | http://localhost:9001 |

Common commands (wrapped in a `Makefile`):

| Command | Does |
|---|---|
| `make test` | Backend (pytest) and frontend (Vitest) unit tests |
| `make e2e` | Playwright end-to-end tests against the local stack |
| `make lint` | ruff, mypy, eslint, tsc |
| `make seed` | Load synthetic firms, clients and documents |
| `make migrate` | Django migrations |

## 4. Secrets and data rules

- `.env` is git-ignored. Only `.env.example` with fake values is committed.
- Real secrets live in AWS Secrets Manager and GitHub Actions environment secrets.
- **Never** put real SSNs, tax documents or client names in the repo, tests, logs, screenshots or tickets. Use `testdata/` generators. This is required by IRS Publication 4557 and the FTC Safeguards Rule.
- `pre-commit` runs gitleaks to block secrets before they're committed; GitHub Secret Protection is the second line.
- Laptops: full-disk encryption (FileVault) on, screen lock on, OS updates on.

## 5. Access checklist for a new team member

- [ ] Added to the GitHub Organization team, 2FA on
- [ ] AWS SSO access to `dev` only (staging and prod by request)
- [ ] Sentry and monitoring access
- [ ] Read the WISP and sign the acknowledgment
- [ ] Clone both repos, run `docker compose up`, and run `make test` green
- [ ] Ship a small first PR (for example a docs fix) to learn the workflow

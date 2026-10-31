# architecture-docs

Planning, delivery and architecture docs for **PayNTax** (working name): tax prep for solo CPAs, with payroll to follow.
Start at [docs/index.md](docs/index.md).

## Layout

```text
docs/
├── index.md                 Portal home
├── planning/                Kickoff notes and draft plan (source decisions)
├── delivery/                TODO.md (task list) and delivery-plan.md (workflow)
├── setup/                   Development setup
├── requirements/            Requirements with IDs
├── screens/                 Screen inventory, flows, wireframes
├── testing/                 Test strategy
├── architecture/            Architecture overview and ADRs
└── assets/                  Rendered diagram PNGs (generated, committed)
diagrams/                    Diagrams-as-code (Python, AWS icons)
generate_diagrams.py         Renders every diagrams/*.py into docs/assets/
index.html                   Docs site (GitHub Pages), renders Markdown + Mermaid
```

## Working with diagrams

Needs Graphviz (`brew install graphviz`) and Python 3.9+.

```bash
make setup
```

```bash
make diagrams
```

```bash
make serve
```

- Cloud and infrastructure diagrams: add or edit a file in `diagrams/`, run `make diagrams`, commit the `.py` and the PNG together.
- Sequences, flows, states, ERDs, timelines: write Mermaid inside the Markdown. GitHub renders it.

## CI

`.github/workflows/render-docs.yml` renders the diagrams on every push and PR. Only `main` publishes the docs site to GitHub Pages.

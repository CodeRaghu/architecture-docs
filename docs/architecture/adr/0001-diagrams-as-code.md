# ADR-0001: Diagrams as code: Diagrams for cloud, Mermaid for the rest

- **Status:** Accepted
- **Date:** 2026-10-31
- **Deciders:** PO

## Context

We want every diagram to live in git, be reviewed in PRs, and stay current. We need AWS architecture diagrams with real service icons, plus sequence diagrams, flows, state machines, a data model, a timeline, and screen layouts.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| [Diagrams](https://diagrams.mingrammer.com/) (Python) only | Real AWS, SaaS and on-prem icons; good automatic layout | Only draws infrastructure; no sequences, states or ERDs; needs Python and Graphviz to render |
| Mermaid only | Renders directly in GitHub Markdown; many diagram types | `architecture-beta` is still beta, and GitHub doesn't load icon packs, so AWS services show as generic boxes |
| Both | Best tool for each job | Two syntaxes to learn |

## Decision

- **Diagrams** for cloud and infrastructure, in `diagrams/*.py`, rendered to `docs/assets/*.png`.
- **Mermaid** inside Markdown for sequences, flows, states, ERDs, Gantt timelines and git flows.
- **Text wireframes** for screen layouts in `docs/screens`, until higher-fidelity mock-ups are needed.

## Consequences

- Contributors need Python and Graphviz to change cloud diagrams ([development setup](../../setup/development-setup.md)); everyone else needs nothing.
- Rendered PNGs are committed so they show on GitHub; CI re-renders them for the docs site.

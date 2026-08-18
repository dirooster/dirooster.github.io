# Revenue OS

Execution-first workspace for validating three revenue tracks:

- AI Production Rescue
- Logistics Automation
- CRA Engineering Readiness

The repository is intentionally simple. The first goal is not a polished SaaS system; it is a working sales surface, qualified leads, personalized outreach drafts, and fast feedback from buyers.

## Structure

- `AGENT.md` - executable operating rules.
- `config/` - business, authorization, credentials example, experiments.
- `crm/` - companies, contacts, outreach, pipeline, suppression list.
- `offers/` - offer notes, assets, and drafts.
- `websites/main/` - static website with three landing pages and two demos.
- `prototypes/` - demo source notes and future proof-of-concepts.
- `research/` - sources, market research, daily reports.
- `sales/` - proposals, discovery notes, objections, call notes.
- `analytics/` - revenue and event tracking notes.
- `state/` - current state, next tasks, decisions, learnings.

## Local Website

Open `websites/main/index.html` in a browser.

The site is static and has no external dependencies. CTA events are stored in browser `localStorage` until a real analytics destination is authorized.

## Email

Email tooling is in `tools/`. It is dry-run first and gated by `config/authorization.yaml`.

See `tools/EMAIL_SETUP.md`.

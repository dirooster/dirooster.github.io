# Owner Review Packet 001

Date: 2026-08-18

Purpose: approve sender voice before enabling real outreach.

Status:

- SMTP: verified.
- Real sending: disabled by `send_email: false`.
- Queue status: all rows are `draft`.
- Sber/SberTech/Sberbank: suppressed.

## Ready For Review

### 1. Glean

Files:

- `content/technical-teardowns/glean-ai-production-teardown.md`
- Queue row: `O-A003`

Draft:

Hi Vishwanath,

I saw Glean's enterprise AI assistant and Work AI positioning. For this category, the recurring production questions are usually retrieval quality, permission boundaries, source grounding, and regression testing as connectors change.

I wrote a short teardown outline of how I would review an enterprise AI search/assistant workflow from the outside, based only on public information.

I run fixed-scope AI Production Audits for teams that already have a serious AI workflow and want a second engineering review of evals, tracing, failure modes, and rollout risk.

Would it be useful if I sent the teardown?

Best,
Dmitrii Petukhov

### 2. Sourcegraph

Files:

- `content/technical-teardowns/sourcegraph-ai-production-teardown.md`
- Queue row: `O-A016`

Draft:

Hi Beyang,

Sourcegraph's work around code understanding and AI coding workflows is exactly where evals across real repositories, secure context access, and regression testing matter.

I wrote a short teardown outline of how I would review an AI coding assistant workflow from the outside, based only on public information.

I help engineering teams audit AI workflows for reliability, observability, failure modes, and human approval boundaries.

Open to seeing the teardown?

Best,
Dmitrii Petukhov

## Approval Options

Selected: Option B - make it shorter and more direct.

Option A: approve tone as-is.

Option B: make it shorter and more direct.

Option C: make it more technical and include 2-3 concrete audit bullets in the first email.

Recommendation accepted: Option B for first cold outreach. Send the detailed teardown only after the recipient replies or clicks.

## Send Gate

Do not send until:

1. Recipient email is verified.
2. Owner approves message tone.
3. `config/authorization.yaml` has `send_email: true`.
4. Queue row status is changed from `draft` to `ready`.

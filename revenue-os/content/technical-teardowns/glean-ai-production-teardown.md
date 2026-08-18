# Glean - AI Production Teardown Draft

Status: draft for outreach. Based only on public information. Do not imply access to Glean systems.

## Public Trigger

Glean publicly positions itself as an enterprise AI assistant and Work AI platform that helps employees find answers, generate content, and automate work with AI. Its leadership page identifies Vishwanath T R as Co-founder and CTO.

Sources:

- https://www.glean.com/about

## Why This Is Relevant

Enterprise search and assistant products fail in production through subtle workflow issues rather than obvious crashes:

- retrieved context is incomplete or stale;
- permissions differ across connected systems;
- generated answers are plausible but weakly grounded;
- connector changes affect result quality;
- model or prompt changes alter behavior without release-level regression visibility;
- users need traceable answers for high-stakes internal decisions.

## Review Angles

1. Retrieval evals

Create a regression set covering permission-sensitive queries, stale documents, ambiguous entities, and cross-system answers.

2. Source grounding

Check whether answers expose enough evidence for a user to verify the answer without blindly trusting the model.

3. Connector failure modes

Map how the assistant behaves when Slack/Jira/Drive/CRM-style sources are delayed, unavailable, duplicated, or permission-filtered.

4. Human escalation

Identify cases where the assistant should stop, ask for clarification, cite uncertainty, or route to a human owner.

5. Observability

Track retrieval quality, answer acceptance, user correction, failed connector calls, latency, and cost by workflow.

## Suggested Offer

AI Production Audit, EUR 1,500 initial market test.

Deliverable:

- failure-mode map;
- eval strategy;
- observability gaps;
- production-risk roadmap.

## Outreach CTA

Ask whether they want the teardown outline, not a sales call first.


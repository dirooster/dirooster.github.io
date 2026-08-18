# Sourcegraph - AI Production Teardown Draft

Status: draft for outreach. Based only on public information. Do not imply access to Sourcegraph systems.

## Public Trigger

Sourcegraph publicly positions around code understanding, code search, code intelligence, and AI coding workflows. Public customer material identifies Beyang Liu as Chief Technology Officer and Co-founder.

Sources:

- https://sourcegraph.com/
- https://claude.com/customers/sourcegraph

## Why This Is Relevant

AI coding assistants and agentic code workflows fail in production through different mechanisms than normal SaaS features:

- repository context is incomplete or stale;
- code suggestions look correct but break local invariants;
- generated changes pass narrow checks but fail broader architecture constraints;
- permission boundaries differ across repositories, issues, docs, and CI systems;
- evaluation is hard because "good code" depends on project-specific rules;
- long-running agent tasks need traceability, rollback, and human approval points.

## Review Angles

1. Repository-level evals

Create task sets that reflect real multi-file changes, internal framework conventions, migration constraints, and regression-prone edge cases.

2. Context boundary checks

Review how the assistant chooses source context, handles missing files, and avoids overconfident answers when the code graph is incomplete.

3. Agent action safety

Map which actions should require human approval: edits, dependency changes, generated migrations, CI modifications, or ticket updates.

4. Observability

Track retrieval quality, patch acceptance, reverted suggestions, failed tool calls, CI failure categories, latency, and cost by workflow.

5. Release discipline

Define how prompt/model/tooling changes are tested before they affect developer workflows.

## Suggested Offer

AI Production Audit, EUR 1,500 initial market test.

Deliverable:

- failure-mode map;
- eval strategy;
- tool-call and context-access review;
- rollout-risk roadmap.

## Outreach CTA

Offer to send the teardown outline before asking for a call.


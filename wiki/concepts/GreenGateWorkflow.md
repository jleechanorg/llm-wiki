---
title: "GreenGateWorkflow"
type: concept
tags: [CI, workflow, green-gate, GitHub-actions]
date: 2026-04-16
---

## Definition
GreenGateWorkflow (`.github/workflows/green-gate.yml`) is the trigger-only + polling CI workflow for PR evaluation. It does NOT run LLM evaluation directly in GHA — instead it triggers AO workers that run skeptic evaluation and posts results back as PR comments.

## Current Flow (After PR #6325)
```
pre-check 6-green eligibility → post trigger comment →
lifecycle-manager runs: ao skeptic verify →
posts VERDICT comment → GHA polling step detects verdict → PASS/FAIL
```

## Previous Flow (Before PR #6325)
```
design_doc_gate (blocking) → skeptic_gate → post trigger comment →
lifecycle-manager runs: ao skeptic verify → VERDICT → GHA polling → PASS/FAIL
```

## Key Files
- `.github/workflows/green-gate.yml` — the workflow definition
- `.github/workflows/doc-size-check.yml` — related doc size check workflow
  - Bug fix in PR #6325: `retry-self-hosted` now correctly `needs: doc-size-check`

## Grep Gates
The workflow historically used grep patterns to check for design doc compliance in PRs touching production files (`world_logic.py`, `constants.py`, `llm_parser.py`, `llm_service.py`).

Pattern portability fix (PR #6309):
- GNU grep: `\s` matches whitespace
- BSD/mawk grep: `\s` not recognized → use `$'^[ \t]*#'` (ANSI-C quoting)

## Lite-green Bypass (2026-05-16)

For **docs-only PRs**, Green Gate times out polling for Skeptic VERDICT (10–15 min wait). Classify as lite-green and check 3 gates directly:
1. `gh api .../commits/<SHA>/status --jq '.state'` = `success`
2. `gh pr view N --json mergeable` = `MERGEABLE`
3. Latest CR review = `APPROVED`

Merge directly without waiting for Green Gate. See `feedback_2026-05-16_lite-green-merge-bypass.md`.

## Green Gate as Authoritative 6-Green Signal (2026-06-10, PR #672)

When Skeptic verdicts are SHA-locked and CodeRabbit auto-dismisses on every push (the "Sisyphean loop"), **Green Gate PASS is the authoritative deterministic merge signal**. The 6 deterministic gates (no LLM) are:

1. design-doc-gate
2. size-check
3. CR (chat `[approve]` is sufficient; REST `reviewDecision=APPROVED` not required)
4. bugbot
5. inline-threads resolved
6. evidence-gate

The 7th gate (LLM Skeptic) is non-deterministic and CAN be overridden by user/admin merge when:
- Green Gate PASS is on the current head SHA
- All other deterministic gates are clean
- The AO Skeptic chain is healthy (lifecycle-worker up, `ao skeptic verify` runs, but verdicts consistently FAIL with non-actionable reasons — e.g. codex model quirks on certain rule checks)

**Precedent**: PR #672 (`[agento] feat(doctor): doctor.sh v2 + Tier 2 watchdog-of-watchdogs`) — GHA run `27273284215` Green Gate PASS at 2026-06-10T11:39:37Z; Skeptic Gate CI timed out after 80 polls × 20 min (`27273284271`); local skeptic-cron 5+ consecutive FAIL with codex model. User admin-merged at `2026-06-10T19:30:47Z` with `gh pr merge --admin --squash --delete-branch` (or equivalent). Final head `6a6943f20`, merge commit `37ff31cda91234d6c01d7408ae7e06a2e6e1fe2c`.

**Why this works**: Green Gate evaluates the same head SHA on every push (deterministic); Skeptic verdict SHA-locks and re-dissesses on push. When Skeptic is stuck in a SHA-lock loop, Green Gate is the only signal that doesn't get invalidated by the merge preparation itself.

See [AOSkepticGateOps](AOSkepticGateOps.md) for the SHA-lock Sisyphean pattern, and [[SelfHostedRunnerInfraFlakeVsRealFailure]] for the broader "deterministic > non-deterministic" merge philosophy.

## Connections
- [SkepticGate](SkepticGate.md) — runs within green-gate workflow
- [DesignDocGate](DesignDocGate.md) — removed gate that was part of the workflow
- [[AWKCompatibility]] — POSIX grep portability fix
- [AOSkepticGateOps](AOSkepticGateOps.md) — SHA-lock Sisyphean loop pattern
- [[SelfHostedRunnerInfraFlakeVsRealFailure]] — broader deterministic-gates-first philosophy

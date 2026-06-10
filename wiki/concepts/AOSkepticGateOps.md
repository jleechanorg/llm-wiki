---
title: "AO Skeptic Gate — Operational Lessons"
type: concept
tags: [agent-orchestrator, skeptic-gate, ops, evidence, antigravity, ci]
sources: [keychain-ao-skeptic-2026-06-05.md, agent-orchestrator-pr-672-merge-2026-06-10.md]
last_updated: 2026-06-10
---

## Summary

Operational lessons for running the Agent Orchestrator (AO) Skeptic Gate as a live system — distinct
from the CI-gate mechanics in [[SkepticGate]]. Focuses on what breaks when AO workers are killed and
how to post verdicts manually.

## Killing AO Workers Has Two Side Effects

1. **Breaks the Skeptic Gate.** Killing AO workers removes the verdict-poster, so the gate gets no
   verdict and hits a **20-minute timeout** instead of resolving.
2. **Regresses the agent-antigravity dist.** AO rebuilds from the *currently checked-out branch*, so
   killing/restarting workers on a feature branch can roll the distributed build backward.

**Durable fix:** merge to `main`. A branch-local fix is undone the next time AO rebuilds the dist.

## Posting Skeptic Verdicts Manually

```bash
ao skeptic verify -n <PR> -m claude --trigger-sha <sha> --request-id <id>
```

- `--dry-run` — preview the verdict without posting.
- `--prompt` — scope the evidence to the **feasible class** for the PR. Example: a macOS-GUI fix
  cannot be CI-integration-tested, so scope the evidence prompt accordingly rather than demanding a
  CI integration artifact that can never exist.

## Evidence Discipline

- **Do NOT commit evidence `.md` files** — they trip CodeRabbit and the Evidence Gate. Publish
  evidence as **gists** and link them instead.

## SHA-Lock Sisyphean Loop (2026-06-10, PR #672)

When a PR is pushed repeatedly (e.g. 13 commits in PR #672 to address review feedback and CI fixes),
**every push invalidates prior Skeptic verdicts AND dismisses prior CodeRabbit APPROVED reviews**.
The resulting loop:

1. push → triggers Skeptic Gate CI poll (default 50 min) + CodeRabbit review
2. Skeptic verdict arrives → CI sees it → PASS, but SHA is now stale
3. push again to address review feedback → SHA changes
4. Skeptic verdict (now stale) is dismissed; CodeRabbit review (now stale) is dismissed
5. New Skeptic verdict must be re-evaluated; new CR review must be re-submitted
6. Repeat

**Result for PR #672**: 13 commits pushed → 8+ Skeptic trigger/verdict cycles → 4 CodeRabbit reviews
(3 DISMISSED, 1 CHANGES_REQUESTED) → final GHA Skeptic Gate CI run `27273284271` timed out at
80×20-min polls. PR was admin-merged at 2026-06-10T19:30:47Z with Green Gate PASS as the
authoritative signal.

**Mitigations**:
- **Reduce commit count on a PR that needs CR/Skeptic** — squash, rebase, force-push clean history
  before requesting review
- **Per-run re-evaluation on the same head** — Green Gate does this; Skeptic verdict does not
- **CodeRabbit chat `[approve]` keyword** — can be nudged in chat to re-submit when REST review
  state is stale (no formal REST re-submission required; Gate 3 PASS is "any CR approve on the head")
- **Admin-merge override** — when all 6 deterministic gates are clean and Skeptic is stuck in the
  SHA-lock loop, `gh pr merge --admin` is the documented exit (see [[GreenGateWorkflow]])

## Connections
- [[SkepticGate]] — the underlying CI-gate mechanics (evidence-over-assertion).
- [[AgentOrchestrator]] — the orchestration system whose workers post verdicts and rebuild the dist.
- [[macOS Keychain]] — the 2026-06-05 session where these ops lessons were captured.
- [[GreenGateWorkflow]] — admin-merge override pattern when Skeptic is SHA-locked.
- [[SelfHostedRunnerInfraFlakeVsRealFailure]] — broader deterministic-gates-first philosophy.
- [[StaleBeadHygiene]] — every PR-merge event should trigger a `br list --status open` audit; PR-merge does NOT auto-close linked beads.

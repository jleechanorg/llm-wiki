---
title: "Agent Orchestrator PR #672 doctor.sh v2 — MERGED 2026-06-10"
type: source
tags: [agent-orchestrator, doctor-v2, watchdog-of-watchdogs, green-gate, skeptic-gate, admin-merge, fragility-audit]
date: 2026-06-10
source_file: agent-orchestrator-pr-672-merge-2026-06-10.md
---

## Summary

PR #672 ([jleechanorg/agent-orchestrator#672](https://github.com/jleechanorg/agent-orchestrator/pull/672)) merged at 2026-06-10T19:30:47Z via admin-merge, overriding unfulfilled Skeptic verdict and CodeRabbit formal APPROVED review. Green Gate (deterministic 6-green) PASS was the authoritative merge signal. 13 files, +1345/-4. Final head `6a6943f20`, merge commit `37ff31cda91234d6c01d7408ae7e06a2e6e1fe2c` on `main`.

## Key Claims

- **Green Gate is the authoritative 6-green merge signal** — run `27273284215` PASSED at 11:39:37 with all 6 deterministic gates green. It handles CodeRabbit chat `[approve]` as Gate 3 PASS even when REST API `reviewDecision` is `REVIEW_REQUIRED`. The 7th gate (LLM Skeptic) is non-deterministic and CAN be overridden by user/admin merge.
- **Skeptic verdict SHA-lock + CodeRabbit auto-dismiss create a Sisyphean loop** — every push invalidates prior verdicts. PR #672 had 13 commits pushed, generating 8+ Skeptic trigger/verdict cycles and 4 CodeRabbit reviews (3 DISMISSED, 1 CHANGES_REQUESTED). Green Gate's per-run re-evaluation on the same head is the workaround.
- **Local skeptic-cron can be healthy but produce 5+ consecutive FAIL** — for PR 672, the AO worker chain was healthy (trigger fired, eval ran, would post verdict), but codex model consistently produced `VERDICT: FAIL` with gate-7/8/8a/8c/8d failing on "Bash `local` outside a function", "regex over-counted all indented YAML keys", and "missing TDD Red phase for Phase 1/Phase 2 scripts". These were legitimate issues that had to be fixed in code.
- **Tilde expansion is STILL unfixed** — PR #672 didn't address the 14 tilde defects across 8 files. `core/paths.ts:186` `expandHome` is canonical but unused by 5 plugin copies + 7 start.ts regexes. Bead follow-up needed.
- **/integrate flow worked correctly post-merge** — switched to main, fast-forwarded to `37ff31cda`, created fresh `dev1781119947` branch from latest main, deleted the merged `feat/doctor-sh-v2-fragility-fix-2026-06-10` branch.

## Key Quotes

> "Green Gate: PASS" — "All 6 gates passed. PR is ready to merge." — GHA run `27273284215` at 11:39:37
>
> "TIMEOUT: No fresh VERDICT after 20 minutes" — Skeptic Gate CI run `27273284271` at 12:12:38 (80×15s polls)
>
> "Re-submitting the formal `APPROVED` review now... [approve]" — CodeRabbit chat reply at 11:51:11 (no formal REST review followed)
>
> `mergedAt: "2026-06-10T19:30:47Z"`, `mergeCommitSha: "37ff31cda91234d6c01d7408ae7e06a2e6e1fe2c"` — REST API confirms admin-merge

## Files merged (13 files, +1345/-4)

| File | LOC | Purpose |
|------|-----|---------|
| `scripts/ao-doctor-v2.sh` | 213 | 6 unmonitored-signal checks (new) |
| `scripts/ai.agento.health-guardian.sh` | 201 | Tier 2 watchdog (60-min cadence, new) |
| `scripts/hermes-watchdog.sh` | 177 | Restored 110-line shim (was failing 158+ runs) |
| `launchd/ai.agento.health-guardian.plist.template` | 70 | plist with sed-substitutable placeholders |
| `scripts/setup-launchd.sh` | 87 (mod) | Added Tier 2 plist install step |
| `docs/doctor-sh-v2.md` | 169 | Design doc |
| `docs/evidence/pr-672/{README,cast.cast,cast.gif,cast.mp4,cast.vtt,raw-typer.txt,checksum.txt}` | 7 files | TDD Red→Green evidence bundle |

## Connections

- [[AgentOrchestratorDoctorShV2]] — design + architecture (3-tier watchdog, log mtime > launchd state, frozen-plist rebootstrap)
- [[SilentFailurePathPattern]] — root cause class for 8/11 fragility categories
- [[AOSkepticGateOps]] — Skeptic Gate CI polling timeout behavior
- [[skeptic-gate-7]] — Skeptic Rule 7 that triggered the CodeRabbit review check
- [[agent-orchestrator-fragility-2026-06-10]] — original audit findings (this source is the merge outcome)
- [[self-hosted-runner-infra-flake-vs-real-failure]] — the lesson that user/admin merge can override Skeptic FAIL when deterministic gates are clean

---
name: green-gate-6-gate-deterministic-ci-pattern
description: "Green Gate workflow: 6-gate deterministic PR merge eligibility with no LLM, no polling, self-hosted runner fallback"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5e846711-556f-4eab-85b3-0883dbc44f75
---

Green Gate (`.github/workflows/green-gate.yml`, 479 lines) implements 6 deterministic gates for PR merge eligibility:

| Gate | Check | Pass condition |
|------|-------|---------------|
| 1 | CI green | Required core jobs pass; fallback: STAGING_CANARY_OK>=1 and 0 failures |
| 2 | No merge conflicts | `mergeable=true` or already merged |
| 3 | CR APPROVED | Latest CodeRabbit review state is APPROVED |
| 4 | Bugbot clean | Cursor Bugbot check-run not "failure" |
| 5 | Comments resolved | Zero unresolved non-nit inline comments (waived if CR APPROVED) |
| 6 | Evidence format | Advisory only (WARN, never FAIL) |

**Why:** Eliminates subjective/LLM-based merge decisions. Self-hosted runners go offline frequently; the staging canary fallback (Gate 1) prevents Gate from blocking when all runners are down.

**How to apply:** When adding new gates: (1) never make them LLM-evaluated, (2) always define a deterministic pass/fail condition, (3) Gate 6 is the only advisory gate — all others are hard blockers, (4) the staging canary fallback must count distinct run IDs (not raw success count) to avoid over-counting from multiple runs, (5) cancelled core jobs should NOT be treated as green (line 95 bug — cancelled ≠ passed).

Related: [[green-gate-6-gate-deterministic-ci-pattern]]

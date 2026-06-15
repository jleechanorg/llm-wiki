---
name: project_2026-06-15_pr7564_7565_merged_after_review
description: PR #7564 + #7565 merged after inline 7-green drive + adversarial code review — captured subagent gotchas, skeptic self-verify trigger mechanism, and per-SHA check-runs API
type: project
bead: rev-6wtuj
metadata:
  node_type: memory
  type: project
  originSessionId: f31deb23-62a1-4ab2-8fbe-46806e1539fb
---

## 2026-06-15 — #7564 + #7565 merged (7-green, adversarial-reviewed)

User said "fanout subagents and /green PRs then MERGE APPROVED once they are good" then followed up with "MERGE APPROVED but use adversarial reviewer to confirm its only logging code for second PR and no prod changes".

### Outcomes
- #7564 (test fix: echo no-op hooks) MERGED 20:41:48Z — commit `d9bc9a764de81481df9dc47c05a13b60529536eb`
- #7565 (OpenAI proxy BQ instrumentation) MERGED 20:45:40Z — commit `e8ffde8a8a43b46a728a5c300476cbbbe6208212` — after adversarial code-review agent confirmed LOGGING_ONLY across 4 files (0 prod behavior changes)

### Path to 7-green (lessons)

**Subagent gotchas (NOT a good fit for 7-green drive):**
- Subagent dispatched 2+ smoke runs and 2+ GG runs per PR, wasting CI capacity — I had to cancel redundant queued runs (id 27573120508 + 27573119800)
- Subagent got stuck in `gh run watch` loop reporting "Still queued" for 30+ min while runner pool was saturated
- Subagent reported "skeptic-cron is queued" but actually never produced a new verdict (skeptic-cron runs on main, doesn't post verdicts for PRs)
- Eventually killed both subagents via TaskStop and took over directly

**Skeptic self-verify trigger (key finding):**
- `SKEPTIC_GATE_TRIGGER` comment alone does NOT auto-trigger skeptic-self-verify.yml
- Must explicitly trigger via `gh workflow run skeptic-self-verify.yml -f pr_number=<N> --ref <branch>`
- The OLD skeptic verdict (FAIL) was 18h stale and was blocking GG even after smoke+body fixes
- New verdicts: #7564 verdict at 20:20:58Z (PASS), #7565 verdict at 20:25:55Z (PASS)

**GG mechanism (verified):**
- `green-gate.yml` workflow_dispatch with `pr_number` and `head_sha` inputs produces check runs tagged to the PR's head SHA even though `head_branch`/`head_sha` in the run metadata show the workflow default (main)
- New GG runs for the current head SHA post status back via the check-runs API
- BUT `gh pr view --json statusCheckRollup` shows STALE entries from previous SHAs — must use `gh api .../commits/<sha>/check-runs` for the authoritative per-SHA view

**Cancel API gotcha:**
- `/actions/runs` endpoint returns `databaseId: null` (broken for jq); use `/actions/workflows/<wf>/runs` endpoint which has real `id` values
- Cancel via `gh api -X POST repos/.../actions/runs/<id>/cancel` works with the workflow-endpoint `id`

### Adversarial review of #7565 (verdict)
- 4 files: 2 prod (LOGGING_ONLY), 2 tests (TEST_ONLY)
- Key validation: new `user_id: str | None = None` param on `invoke_openclaw_gateway*` defaults to None; existing Flask call sites in `mvp_site/main.py:1954, :2040` don't pass it (verified at head SHA) — backward compatible
- BQ helper `_bq_log_openai_proxy` fails open (try/except) + double-gated by `bq_logging_enabled()` and `provider_logging_suppressed()`
- Known limitation (disclosed in PR body): `user_id` not yet wired to Flask call sites

### Memory rules to apply
- When the user says "fanout subagents and /green PRs", that's a 7-green drive. Subagent approach has bad failure modes here; consider taking over directly OR using a single monitor agent that explicitly delegates to Bash for cancellations.
- For ANY PR stuck on gate-8, always check: is there a real-mode smoke pass comment with the right SHA? If not, dispatch `gh workflow run mcp-smoke-tests.yml -f pr_number=N -f test_mode=real`.
- For ANY PR stuck on skeptic verdict FAIL, check if the verdict is stale (>4h old). If yes, re-trigger via `gh workflow run skeptic-self-verify.yml -f pr_number=N`.
- ALWAYS verify per-SHA check-runs via `gh api .../commits/<sha>/check-runs`, not `gh pr view --json statusCheckRollup`.
- For BQ-logging PRs, the user's first instinct is "adversarial review to confirm logging-only" — preempt with code-review agent classification of every change as LOGGING_ONLY / LOGGING_INFRASTRUCTURE / TEST_ONLY / PROD_BEHAVIOR_CHANGE / NEEDS_HUMAN.

---
name: green-gate-first-run-after-push-false-negative
description: The first Green Gate run on a PR immediately after a push always FAILS with GATE-1 CI=pending and GATE-3 CR=FAIL(status=pending) — the second run on the same head SHA passes. Treat the first run as a known false-negative.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 11b18814-6b01-49a8-a167-12c66b99835e
---

# Green Gate first-run-after-push is a known false-negative

When a new push lands on a PR, the Green Gate workflow's first run almost always FAILS with the same exact failure pattern:

```
GATE-1 FAIL: CI=pending
GATE-3 FAIL: CR=FAIL(status=pending comment=none)
GATE-4 WAIT: Bugbot runs=1 status=in_progress conclusion=none (poll 1/40) ... poll 11/40
GATE-4 PASS: Bugbot=neutral (clean)
GATE-5 PASS: all comments resolved
GATE-6 PASS: evidence present
7-green eligibility: false
```

**Root cause:** The Green Gate checks *current* state of the PR at evaluation time. The first run after a push happens *before*:
- The push-triggered CI workflow has posted its conclusion (CI is `pending`)
- The push-triggered `ping-coderabbit` workflow has completed (CR status is `pending` and there is no APPROVED comment yet)

**Pattern: first run FAILS, second run PASSES (same head SHA).**

**Evidence (Dice-audit PRs #7352 and #7353, 2026-06-10):**

| PR | First run | Conclusion | Second run | Conclusion |
|----|-----------|------------|------------|------------|
| #7352 | 27264447832 at 08:45:28Z | ❌ FAILURE | 27264478259 at 08:46:01Z | ✅ SUCCESS (09:32:31Z) |
| #7353 | 27268328475 at 09:56:11Z | ❌ FAILURE | 27268352388 at 09:59:16Z | IN_PROGRESS (10:18Z) |

Both runs on the same head SHA; the second run is auto-triggered by the GitHub Actions concurrency settings.

**Implications for monitoring and reporting:**

1. **Don't treat the first Green Gate FAILURE as a real failure.** Wait for the next run (~6 minutes later) before declaring a state change. `gh pr checks` will show a stale `FAILURE` from the first run until the second run completes.

2. **For 7-green reporting, use the LATEST Green Gate run on the current head SHA** (not `gh pr checks`, which shows ALL runs including stale failures). Find the latest via:
   ```bash
   gh pr view <PR> --json statusCheckRollup --jq '.statusCheckRollup[] | select(.name == "Green Gate") | {completedAt, conclusion, detailsUrl}'
   ```
   Then check the workflow run details (`detailsUrl` → `actions/runs/<id>`) for the run that actually evaluated the current head.

3. **Bugbot polling takes ~4-5 min** (polls 11/40 at 21s intervals before Bugbot completes). The first run usually has GATE-4 WAIT, GATE-4 PASS at the end. The second run has GATE-4 PASS immediately because Bugbot has already finished by then.

4. **When timing the wait:** 30-min Green Gate budget per the monitor subagent is plenty because the second run starts ~3-5 min after the first completes, and the second run completes ~5-7 min after that. Total: ~10-15 min for a fresh push to be 7-green-confirmed.

**How to apply:**

- When polling a Green Gate on a freshly-pushed PR, the first failure is a known false-negative. Do not update the handoff doc or post a status comment declaring a failure until the second run completes.
- When using `gh pr checks` for 7-green reporting, filter to the latest run only: `gh pr view <PR> --json statusCheckRollup --jq '.statusCheckRollup[] | select(.name == "Green Gate")' | head -1`.
- When CodeRabbit is "pending" on a freshly-pushed PR, the Green Gate is expected to FAIL on the first run regardless of how clean the diff is.

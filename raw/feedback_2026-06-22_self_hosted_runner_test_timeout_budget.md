---
name: feedback-2026-06-22-self-hosted-runner-test-timeout-budget
description: Mobile Auth Same-Origin Regression test on self-hosted runners needs 90s Flask-startup + 60s Playwright page.goto budgets. Default 20s budgets flake on memory-pressured runners where gunicorn FastEmbed load + auth.js fetch exceed 20s.
metadata:
  node_type: memory
  type: feedback
  originSessionId: 79a12801-6187-4144-846a-f1b1d003e14d
  bead: rev-mfcp4
---

Drove PR [#7815](https://github.com/jleechanorg/worldarchitect.ai/pull/7815) (merged 2026-06-23) to fix the Mobile Auth Same-Origin Regression test that was flaking on CI run [27991914172 / job 82845940066](https://github.com/jleechanorg/worldarchitect.ai/actions/runs/27991914172/job/82845940066) on PR [#7810](https://github.com/jleechanorg/worldarchitect.ai/pull/7810).

**Why:** Self-hosted GitHub Actions runners are memory-pressured; the default 20s budgets are too tight for two distinct phases:

1. **Flask boot (`start_flask` deadline)** — gunicorn worker must import `mvp_site.main`, initialize Firebase, AND load the FastEmbed classifier model `BAAI/bge-small-en-v1.5` before `/health` responds. Model load alone can take ~20s; a slow first worker killed by gunicorn master forces a fresh worker to redo the full boot. **Budget: 90s.**
2. **Browser load (`page.goto` timeout)** — `domcontentloaded` waits for the parser to hit `</html>` after fetching blocking scripts (auth.js). On the same memory-pressured runner, auth.js fetch can take 10s+. **Budget: 60s.**

The substantive PASS/FAIL signal is in the **test cases**, not in startup/load time. Tightening the budgets to detect "actually broken" faster is not worth the false-positive flake rate.

**How to apply:**
- For any new `testing_ui/**` test that boots Flask via gunicorn and exercises the live server, default to 90s Flask-start + 60s page.goto. Add inline comments naming the observed run + the FastEmbed model name so the next person who hits this can find the precedent.
- Do NOT use `wait_until="load"` — `domcontentloaded` is the right event for our SPA (auth.js + first-paint; full load is overkill for smoke tests).
- If model load grows beyond 90s, bump the deadline — don't shorten it. If auth.js fetch grows beyond 60s, bump the page.goto timeout.
- The "real fix" is reducing runner memory pressure (lower containerConcurrency + raise minScale), not tightening the test budgets. That's an infra matter.

**Verification:**
- Pre-fix Layer A startup FAIL: run [27991914172 / job 82845940066](https://github.com/jleechanorg/worldarchitect.ai/actions/runs/27991914172/job/82845940066) on PR #7810 (Flask startup died at 20s).
- Post-90s-Flask, pre-60s-page.goto Layer B FAIL: run [27992750133](https://github.com/jleechanorg/worldarchitect.ai/actions/runs/27992750133) on PR #7815 (page.goto died at 20s).
- Post-fix PASS: run [27992975784 / job 82849096053](https://github.com/jleechanorg/worldarchitect.ai/actions/runs/27992975784/job/82849096053) on PR #7815 — Layer A 4/4, Layer B 2/2 (1m30s).

**References:**
- Code: `testing_ui/mobile_auth_same_origin/test_auth_same_origin.py:84-92` (start_flask 90s budget + FastEmbed comment) and `testing_ui/mobile_auth_same_origin/test_auth_same_origin.py:283-289` (page.goto 60s budget + auth.js-fetch comment).
- PR: [#7815](https://github.com/jleechanorg/worldarchitect.ai/pull/7815), merged 2026-06-23T02:21:20Z, commit `e08abf3215`.
- Companion memory: [[feedback-2026-06-22-pr-evidence-gate-requires-anchor-url]] — the GATE-6 anchor-URL + `gh pr edit --body "$()"` wipe bug surfaced while driving the same PR.

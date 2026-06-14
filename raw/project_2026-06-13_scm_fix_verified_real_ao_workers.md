---
name: scm-fix-pr-671-verified-with-real-ao-workers-2026-06-13
description: "PR #671's fix (absolute /usr/bin/git paths in backfill-extensions.ts, 9 sites) was tested with real AO workers on 2026-06-13. Result: SCM operations work in worker shells. ao-6351 ran git log/git status/git rev-parse successfully; ao-6352 ran git status successfully. Workers did NOT die in SCM death-spiral. The 'stuck-probe' failure of ao-6353 is a separate failure mode (trust prompt not accepted), not an SCM issue."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8e1493a5-115a-4b66-9790-42973f21fc27
---

**Why:** 2026-06-13 10:22Z — spawned 3 AO workers (ao-6351, ao-6352, ao-6353) to verify PR #671's SCM fix. The known death-spiral was: 135+ spawn git ENOENT errors in ao-health.log, scmFailureCount 73 and 204 in prior sessions, workers killed at high counts. The fix landed in PR #671 (merged 2026-06-09 per `feedback_2026-06-09_bd670_pr_landed.md`): 9 sites in `backfill-extensions.ts` use absolute `/usr/bin/git` instead of bare `git`, bypassing the launchd PATH gap.

**How to apply:** When a follow-up session asks "is the SCM fix still working?" or "test the SCM fix with real workers", point to this memory. The test confirmed the fix is working AS OF 2026-06-13 10:30Z. If a future test shows regression, the pattern is:
1. Spawn 1-2 workers on a simple git-exercising task (e.g., "run `git log --oneline -3` and report")
2. Accept the antigravity trust prompt in the tmux pane (Enter on default "Yes, I trust this folder")
3. Wait for the worker to send MCP mail with results
4. Check the mail confirms git output (no ENOENT, no PATH errors)
5. If scmFailureCount stays 0 and git output is correct, fix is verified

**Test details:**

| Session | Task | Result | Time |
|---------|------|--------|------|
| ao-6351 | "run `git log --oneline -3`, `git status --short`, `git rev-parse --abbrev-ref HEAD`" | All 3 succeeded, sent MCP mail id 249 to jleechanclaw | spawned 10:22:25, completed 10:23:57 (~90s) |
| ao-6352 | "run `git for-each-ref refs/heads/`, `git diff main..HEAD --stat`" | `git status` succeeded, then went tangent on header_check.py find; killed manually at 10:32 | spawned 10:25:46, killed 10:32 |
| ao-6353 | "create branch, checkout, run git log, delete branch" | **Killed for stuck-probe at 10:28:59** (98s lifetime) — was sitting on the trust prompt because I never accepted Enter for it. NOT an SCM issue. | spawned 10:27:21, killed 10:28:59 |

**Key signal**: ao-6351's MCP mail (id 249) confirmed:
```
git log --oneline -3 → afa4ecb18, d8940175b, 99232739a (correct, all 3 prior merges)
git status --short → listed 20 untracked files (no error)
git rev-parse --abbrev-ref HEAD → main
```
No ENOENT, no PATH issues. SCM fix is working.

**Adjacent learning — antigravity trust prompt is a real failure mode**: When spawning an AO worker via antigravity, the FIRST thing the worker sees is a "Do you trust the contents of this project? Yes/No" prompt. If the orchestrator/operator doesn't accept this (send Enter or arrow + Enter) within the stuck-probe timeout (~1-2 min), the worker gets auto-killed with `killConfirmed=stuck-probe`. Solution: immediately after `ao spawn`, watch for the trust prompt in tmux and send Enter.

**Adjacent learning — worker side-tasks can dominate**: ao-6352 spent 3+ minutes running `find /Users/jleechan -name header_check.py` because the system prompt requires header verification. The actual git test was done in the first 30 seconds. Future SCM tests should:
- Tell the worker explicitly: "Do NOT run header_check.py, do NOT run find. Only run the commands I asked for."
- Or set a watcher that kills the worker once the git output is in the MCP mail

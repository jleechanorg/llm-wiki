---
name: live-pr-head-staleness-fetch-and-verify-before-claiming
description: "When assuming local state matches the live PR, ALWAYS `git fetch` + `git rev-parse origin/<branch>` first. PRs have multiple writers (other agents, human); commits can land between local work and the user's view of the PR. Treating local HEAD as the live PR is a hallucination."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 65fcb9f7-3fca-4299-aafa-89506240a1a1
---

Multi-writer PRs accumulate commits from any agent or human who pushes. Local `git log` shows the local HEAD; the live PR head is the most recent commit on `origin/<branch>`. They diverge routinely.

**Anti-pattern (what I did wrong, 2026-06-12, PR #7467):**
- The real-LLM organic test ran on local HEAD `31aaceb8` at 12:06-12:26Z. While the test ran, the `.dot` chart commit `e619e882` landed at 12:08:46, then my prompt fix `7610402` at 12:35, then a production routing/auth commit `212b0133` after that.
- I claimed "the test's git commit drift was benign because it was only the .dot file" — wrong, because the drift continued past the .dot, including a real production logic change (`212b0133`) I had no visibility into.
- I described the live PR head as `e619e882` (my then-local HEAD) when the user's view of the PR was actually at `212b0133`.
- I dismissed the user's concerns about CodeRabbit/threads/CI by implicitly treating local state as authoritative for "what's in the PR."

**The right pattern:**
1. Before any "the PR is at SHA X" or "the test ran on head X" claim, run:
   ```bash
   git fetch origin
   git rev-parse origin/<branch>
   ```
2. The "live head" = `origin/<branch>` HEAD, not local HEAD.
3. Multi-commit drift is normal; do not dismiss it as benign.
4. Re-test at the live head, not the local head, when the user references "current head" or "live head" or "what's in the PR."
5. If local and origin diverge, decide explicitly: rebase local onto origin? Fetch and merge? Just accept the new live head as ground truth?

**Verification:**
- User's exact words: "Live PR head is now 212b0133..., not e619e882..., and not the tested 31aaceb8... or evidence-listed a558732..."
- User's specific concerns that depended on live head: PR body evidence SHA mismatch, CI not green at current head, 5 unresolved review threads, CodeRabbit skipped, `is_level_up_route_active()` still exists (because 212b0133 added more production logic, not a thinning).

**Reusable pattern:**
- **Pre-claim check**: `git fetch origin && git rev-parse origin/<branch>` before any "the PR is at X" assertion.
- **PR evidence body**: must reference `origin/<branch>` HEAD, not local HEAD. Update when new commits land.
- **Re-test scope**: at the live head, not the test-time local head.
- **Treating "the PR" as a single writer's state**: wrong on multi-agent PRs. Always verify.

**Related:**
- `feedback_2026-06-12_generic_prompt_fixes.md` (the prompt-content lesson from the same review)
- `feedback_2026-06-11_rebase_clears_presubmit_base_drift.md` (related: long-lived branches drift; rebasing is the fix)
- `feedback_2026-06-11_10pr_rebase_sweep.md` (10-PR rebase sweep precedent)

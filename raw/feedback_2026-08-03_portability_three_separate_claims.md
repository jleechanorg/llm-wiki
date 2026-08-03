---
name: portability-three-separate-claims
description: "committed", "pushed", and "portable" are three distinct claims that each need independent verification — a clean git status only proves the first
metadata:
  type: feedback
  bead: disk_magician-qb0 (closed)
---

A routine "make sure everything is in the repo and machine portable" ask
surfaced three real, independent gaps across three repos (disk_magician,
~/roadmap, ~/llm_wiki), none of which a plain `git status` would catch:

1. **llm_wiki**: a fully-committed, correctly-authored commit had been
   silently failing `git push` since 2026-07-11 — GitHub push protection
   blocked it because real API keys (Slack/DeepSeek/Groq/RunPod/GitHub PAT)
   were captured verbatim into `artifacts/ao-minimax-user-scope-*` test-run
   dumps. "Commit succeeded" was never checked against "push succeeded" for
   3+ weeks. Fixed via `git filter-repo --path artifacts/ --invert-paths`
   (only one commit touched that path) + user-approved
   `git push --force-with-lease` (old SHA `dc1bae69` → new `f79f556f`,
   verified via `git ls-remote`, not just push-command output).

2. **disk_magician**: the top-level `.gitignore` had a blanket `.beads/`
   rule that shadowed a correctly-scoped nested `.beads/.gitignore` (which
   only excluded `*.db`/`*.lock`/`.br_history/` etc). This made the repo's
   **entire bead database — 38 issues, since repo inception — machine-local-
   only**, invisible to `git log`, while `br sync --status` happily reported
   "In sync" (that only compares local jsonl vs local sqlite db, both
   equally invisible to git). Fixed: track `.beads/issues.jsonl`,
   `config.yaml`, `metadata.json`; keep db/lock files ignored via the
   nested file (commit `48c31a1`).

3. **~/roadmap**: a real branch divergence from a concurrent session's
   unrelated work (`ios-web-visual-parity`) blocked any push at all. One
   trivial append-only conflict (both sides added distinct dated entries to
   the tail of `learnings-2026-08.md`) — confirmed zero header overlap via
   `comm -12`, merged by keeping both sides, pushed as a clean fast-forward.

**Why:** All three gaps were invisible to every "does this look done?" signal
I'd normally trust (clean `git status`, "in sync" tool output, no error on
`git add`+`git commit`). Only checking `git ls-remote origin <branch>` against
local `HEAD` — for every repo, after every commit — surfaced the push
failures. Only `git log --all -- <path>` (not `git status`, not `br sync`)
surfaced the beads-never-tracked bug.

**How to apply:** When asked to verify work is "in the repo" or "portable":
- Check local commit AND `git ls-remote origin <branch>` == local `HEAD`,
  per repo touched — never trust push-command exit code alone if a push can
  silently be rejected upstream (secret scanning, branch protection).
- For any `.beads/` or similar local-state directory: verify with
  `git log --all -- <path>/issues.jsonl` (or equivalent portable-state file)
  that it has EVER been committed, not just that the local tool reports
  itself healthy.
- A destructive fix (history rewrite + force-push) found this way still
  needs the standing force-push approval gate — get it explicitly before
  acting, even when the fix is clearly correct.

See also [[dirs-cleaner-225gib-root-cause-and-fix]] (the disk-investigation
work this sweep was closing out) and full writeup:
`~/roadmap/nextsteps-2026-08-03-disk-magician-portability-sweep.md`.

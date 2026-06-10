---
name: don-t-fabricate-work-that-wasn-t-persisted-read-disk-not-summaries
description: "After a context compaction, the summary said I had written 13 config tests and a remove_repo no-op refinement. On resume the working tree was clean vs HEAD — the work was never saved. Don't act on summary claims without verifying on disk."
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 4de5b569-b51b-4a12-9a41-45eee5ee760f
---

After a context-compaction summary, I tried to commit a "remove_repo true no-op" refinement and an extended `tests/test_config.py` that the summary described as already in flight. Both files were unmodified vs HEAD when I checked disk.

The actual state on disk was:
- `merge_train/config.py` — original 175-line version (the refinement was never saved)
- `tests/test_config.py` — 95 lines, 5 tests (the 13-test extension was never saved)

The entire plan from `kind-floating-mccarthy.md` was already executed by a prior session and committed in `69240f2` on `feat/registry-free-symbol-conflicts` — that's why the working tree was clean. My "edits" in the prior conversation were either identical rewrites of what's already on disk, or were never persisted.

**Lesson**: a post-compaction summary is a *claim* about prior context, not a *verification* of prior work. After resume, before continuing:
1. `git status` — does the working tree match the summary's claims?
2. `git log` — does HEAD match the summary's claimed commits?
3. `wc -l <file>` — does the file match the summary's claimed edits?
4. Run the test suite — does the summary's claimed green state hold?

If any of these don't match the summary, surface the gap immediately. Don't silently discover it mid-task (as I did when "no changes to commit" turned out to be the truth).

**Verification**: after the user said "why is this taking so long? commit" and I correctly pivoted to "the work is already done at `69240f2`" by reading disk state, the user accepted it and asked for the missing edge-case tests as a follow-up. I then wrote them, ran them (15 pass), committed `09d24ef`, and pushed.

**Pattern**: "verify-before-reporting" is a global CLAUDE.md rule. The summary-induced variant is: the verification target is *the prior session*, not the user. Read the files, not the summary.

**Related**: see [[feedback_2026-06-10_push_rule_misattribution]] — same session, same root cause: deferring to memory of context instead of reading the actual artifacts.

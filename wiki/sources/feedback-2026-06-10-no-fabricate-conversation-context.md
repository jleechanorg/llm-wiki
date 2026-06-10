---
title: Don't fabricate post-compaction context — read disk, not summaries
date: 2026-06-10
type: feedback
classification: Mandatory
bead: none
files:
  - /Users/jleechan/.claude/projects/-Users-jleechan-projects-merge-train/memory/feedback_2026-06-10_no_fabricate_conversation_context.md
references:
  - commit 69240f2 (prior session's full plan execution)
  - commit 09d24ef (this session's actual follow-up)
  - /Users/jleechan/.claude/CLAUDE.md "Verify before reporting" rule
---

# Don't fabricate post-compaction context — read disk, not summaries

A post-compaction summary said I had extended `tests/test_config.py` from 5 to 13 tests, and refined `merge_train/config.py` so `remove_repo` is a true no-op. On resume:

- `git status` was clean.
- `wc -l merge_train/config.py` matched the original 175 lines, not a refined version.
- `wc -l tests/test_config.py` was 95 (5 tests), not the 13-test version.
- HEAD was at `69240f2` — the prior session's commit, which contained everything the plan called for.

My "edits" in the prior conversation were either identical rewrites of what was already on disk, or were never persisted.

## Lesson

A post-compaction summary is a *claim* about prior context, not a *verification* of prior work. After resume, before continuing:

1. `git status` — does the working tree match the summary's claims?
2. `git log` — does HEAD match the summary's claimed commits?
3. `wc -l <file>` — does the file match the summary's claimed edits?
4. Run the test suite — does the summary's claimed green state hold?

If any of these do not match the summary, surface the gap immediately. Do not silently discover it mid-task (as I did when "no changes to commit" turned out to be the truth).

## Pattern

The global CLAUDE.md rule is "verify before reporting" — applied to the user. The summary-induced variant is: the verification target is *the prior session*. Read the files; do not trust the summary.

## Verification

User said "why is this taking so long? commit" — I correctly pivoted to "the work is already done at `69240f2`" by reading disk state, then offered the missing edge-case tests as a follow-up. The follow-up commit `09d24ef` actually persisted (15 tests pass, 259 in the full suite).

## Related

- [[feedback-2026-06-10-push-rule-misattribution]] — same session, same root cause: deferring to a record instead of reading the actual artifact.

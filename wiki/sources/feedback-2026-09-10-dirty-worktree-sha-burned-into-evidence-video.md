---
title: "Dirty-worktree SHA burned into evidence video; real browser video catches bugs unit tests miss"
type: source
tags: [evidence, testing, worldarchitect, pr-review, er]
date: 2026-09-10
source_file: raw/feedback_2026-09-10_dirty_worktree_sha_burned_into_evidence_video_and_video_catches_bugs_unit_tests_miss.md
---

## Summary

On PR #9831 (jleechanorg/worldarchitect.ai), a `testing_ui/capture_*.py` evidence
script computed `git rev-parse HEAD` at capture time and burned it into a video
caption. The first real capture ran while the actual fix was staged on disk but
not yet committed, so the video's caption showed the PRIOR commit — one that did
not contain the fix it claimed to demonstrate. An independent `/er` adversarial
evidence review caught this via `git diff <burned-in-sha> <fix-sha> -- <file>`
showing the fix absent at the burned-in SHA, a genuine FAIL verdict. Separately,
building the real captioned browser video (not just Python unit tests) surfaced
a second, fully independent bug: the frontend's own client-side renderer for the
same data field had an identical bug that no unit test exercised at all.

## Key Claims

- Any script that burns a git SHA into evidence media must only run against a
  clean, committed tree — check `git status --porcelain` before trusting the
  capture, not after.
- `/er` (evidence review) genuinely caught a real provenance defect via content
  diffing (`git diff <sha1> <sha2> -- <file>`), not just checksum verification.
- Real browser video evidence found a production bug (a frontend-only render
  path) that fully-passing backend unit tests structurally could not detect.
- `/integrate --force` auto-stashes uncommitted changes with a tagged message
  rather than discarding them — safe once mtime/content analysis confirms the
  dirty state predates and is superseded by already-merged work.

## Key Quotes

> "Video/GIF/frame1.png caption SHA (`cabd6f3d...`) does not contain the code
> change the artifact demonstrates — dirty-capture SHA mismatch, no documented
> exception." — independent `/er` review verdict on PR #9831

## Connections

- [[EvidenceShaFreeze]] — same family of SHA-provenance failure, but the
  direction is reversed: EvidenceShaFreeze covers evidence going stale because
  production code changed *after* capture; this incident covers evidence
  captured *before* the fix was even committed (a dirty-worktree race, not
  post-capture drift).
- [[EvidenceSkepticalReview]] — the `/er` reviewer's content-diff verification
  method (not just checksum/eyeball) is a direct instance of that discipline.

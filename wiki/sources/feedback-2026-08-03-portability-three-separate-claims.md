---
title: "\"Committed/pushed/portable\" are 3 separate claims"
type: source
tags: [git, portability, debugging, process]
date: 2026-08-03
source_file: raw/feedback_2026-08-03_portability_three_separate_claims.md
---

## Summary
A routine "make sure everything is in the repo and machine portable" ask
surfaced three real, independent gaps across three repos (`disk_magician`,
`~/roadmap`, `~/llm_wiki`), none of which a plain `git status` would have
caught: a silently-blocked push hidden behind a secret-scanning rejection,
an entire subsystem's history made machine-local-only by a shadowed
`.gitignore` rule, and a real branch divergence from concurrent unrelated
work. All three were found only by checking `git ls-remote origin <branch>`
against local `HEAD`, and `git log --all -- <path>` against local tool
"in sync" claims, per repo.

## Key Claims
- `llm_wiki`: a fully-committed, correctly-authored commit had been silently
  failing `git push` since 2026-07-11 because GitHub push protection
  blocked real API keys (Slack/DeepSeek/Groq/RunPod/GitHub PAT) captured
  verbatim into a test-artifact dump. "Commit succeeded" was never checked
  against "push succeeded" for 3+ weeks.
- `disk_magician`: a blanket top-level `.gitignore` rule (`.beads/`)
  shadowed a correctly-scoped nested `.beads/.gitignore`, making the
  entire bead database (38 issues, since repo inception) machine-local-only
  and invisible to `git log` — while `br sync --status` reported "In sync"
  the whole time (that check only compares local jsonl vs local sqlite db,
  both equally invisible to git).
- `~/roadmap`: a real branch divergence from a concurrent session's
  unrelated work blocked any push at all until merged (one trivial
  append-only conflict, zero real overlap).
- General rule: verifying work is "in the repo" requires checking local
  commit AND `git ls-remote origin <branch>` matching local `HEAD`, for
  every repo touched — a clean `git status` only proves the working tree
  is committed, not that the commit reached anywhere else.

## Key Quotes
> "commit succeeded" was never checked against "push succeeded" for 3+ weeks

## Connections
- [[dirs-cleaner-225gib-root-cause-and-fix]] — the disk-investigation work this portability sweep was closing out
- [[MacosDiskAccounting]]

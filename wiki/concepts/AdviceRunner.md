---
title: "Advice Runner (run_primary_pair.py)"
type: concept
tags: [advice, harness, code-review, tooling]
date: 2026-09-06
---

# Advice Runner

`~/.claude/skills/advice/scripts/run_primary_pair.py` is the executable backing the
`/advice` skill's primary reviewer pair (Codex + Opus, launched concurrently at one
exact SHA). It clones the target repo twice into disposable, detached, `origin`-less
checkouts, runs each reviewer inside its own clone behind a concurrency barrier, and
writes a `receipt.json` plus per-reviewer `.txt` output to a caller-supplied
`--output-dir`.

## Reliability fixes (2026-09-06)

- **Durable/incremental receipts**: originally waited for both reviewer futures
  before writing anything; now writes an initial `running` receipt (with `pid` and
  `boot_identity`) immediately, then publishes each reviewer's result — and rewrites
  the receipt — as soon as that lane completes (`concurrent.futures.as_completed`),
  so a killed process still leaves a completed lane's result on disk.
- **Output-dir must be persistent, not `/tmp`**: the caller (`advice/SKILL.md`) used
  to `mktemp -d` the output dir too, which can be wiped by a reboot; moved to
  `~/.claude/state/advice/runs/<sha>-<ts>/`.
- **Git LFS smudge bug**: see [[GitLfsSmudgeFilter]] — `create_clone()` removed
  `origin` before `checkout`, breaking LFS-tracked blob downloads.

## Connections

- [[GitLfsSmudgeFilter]]
- [[SameAuthorConcurrentSessionCollision]]
- Source: [[feedback-2026-09-06-advice-runner-lfs-smudge-and-concurrent-merge-race]]

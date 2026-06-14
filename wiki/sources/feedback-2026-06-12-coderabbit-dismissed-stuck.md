---
title: "CodeRabbit DISMISSED-stuck + admin-override merge (2026-06-12)"
type: source
tags: [coderabbit, dismissed, stuck, gate-3, green-gate, admin-merge, escalation, rate-limit, credits]
date: 2026-06-12
source_file: raw/feedback_2026-06-12_coderabbit_dismissed_stuck.md
---

## Summary
After a CodeRabbit CHANGES_REQUESTED → fix → push cycle, CR's formal review object can get permanently stuck at `DISMISSED` and never flip to `APPROVED` — even with `.coderabbit.yaml` `approve: true` — because CR is an incremental review system that refuses to re-review already-reviewed commits. The formal review `state` stays `DISMISSED` against a stale SHA while CR confirms the fix only in chat prose, which is fatal to the merge pipeline (Green Gate gate-3 reads the formal review state).

## Key Claims
- `@coderabbitai all good?` → chat prose only (no review object) — useless for gate-3
- `@coderabbitai review` → acknowledged but no-op on already-reviewed commits — also useless once stuck
- Only a brand-new commit triggering auto-review yields a fresh review object (and even then, post-changes-requested it has been emitting DISMISSED, not APPROVED)
- Resolution = admin override merge, but ONLY when all hold: explicit user authorization, substantively 7-green, skeptic-cron structurally stalled
- Second variant: CR out of credits / rate-limited → `state=none` (CR never starts the review); posts `> [!WARNING] Review limit reached … organization has run out of usage credits` instead
- After squash-merge, live `~/.hermes` local `main` that carried the cherry-pick **diverges** from origin (content-identical, different SHA) — `git reset --hard origin/main` to restore ff-only-pull

## Key Quotes
> "`mergeStateStatus=UNSTABLE` + `mergeable=MERGEABLE` means GitHub itself allows the merge (UNSTABLE = a *non-required* check failing, i.e. the advisory Green Gate)."

> "There is no in-band fix. The only thing that yields a fresh review object is a brand-new commit triggering auto-review (and even then, post-changes-requested it has been emitting DISMISSED, not APPROVED)."

## Connections
- [[CodeRabbitStall]] — DISMISSED + rate-limit dual variant
- [[AdminMergeProtocol]] — escalation: explicit user auth + substantively green + skeptic stalled
- [[SkepticCron]] — mirrors Green Gate, structurally stalled when CR stuck
- [[SquashMergeDivergence]] — verify file CONTENT, not SHA ancestry, after squash merges
- [[PRWatchdog]] — 13+ min monitoring + `@coderabbitai review` escalation

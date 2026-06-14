---
title: "PR #7048 Location Centralization MERGED (sha 25cee34d6f)"
type: source
tags: [pr-workflow, location-util, merge, 7-green, worldarchitect]
sources: []
last_updated: 2026-05-24
source_file: raw/project_2026-05-24_pr7048_merged_summary.md
---

## Summary
PR #7048 "[antig] Consolidate location fields to centralized location_util" MERGED 2026-05-24T07:09:07Z as commit `25cee34d6ff9f966eb9ba190e40efbd6eec3a5b9` after racing PR #6896 (which chose an incompatible canonical field `current_location_name` and merged first). #7048 resolved by taking THEIRS on all touched files and keeping its own `location_util.py` as additive scaffolding. 7-green was proven by `github-actions[bot]` VERDICT: PASS comments at two consecutive HEADs.

## Key Claims
- 7-green proven by `github-actions[bot]` VERDICT: PASS comments at 2026-05-24T06:15:18Z (HEAD `7ea51b546c`) and 2026-05-24T06:26:10Z (HEAD `e979224079`, post re-merge of main).
- All 8 skeptic gates PASS: CI / merge / CR / Bugbot / comments / evidence / self-verify / smoke.
- Beads closed this session: `rev-igs3c`, `rev-2lksq`, `rev-ufjbi`, `rev-pt4sh`, `rev-tax51`, `rev-20ydj`, `rev-44p4q`, `rev-9xab7`, `rev-y97q2`, `rev-0e0dp`, `rev-3hck`, `rev-ia2s4`, `rev-7zd1`, `rev-xusj`, `rev-9rhhk`, `rev-ogeah`, `rev-f3go`, `rev-m47y`, `rev-hnak`, `rev-taww`, `rev-revou6`, `rev-revrhe` (22 total).
- Open carryover: `rev-7z3b8` (Scene 73 same-scenario green proof for already-merged PR #6896 — out of #7048 scope).
- Open follow-up: 754 → 737 open beads after triage. 308 still >90 days old. Recommend broader sweep that closes beads whose tracked PR has merged (105 distinct PRs referenced in open beads).
- Beads CLI verification: confirm `merge=beads` driver works post-merge in fresh clones (CR P1 concern resolved by reverting `.gitattributes` to main's version).
- 12 commits in this session including 3 CR/Cursor/Codex review-comment fixes and final merge by GitHub squash to `25cee34d6f` on main.

## Key Quotes
> "PR #7048 '[antig] Consolidate location fields to centralized location_util' MERGED **2026-05-24T07:09:07Z** as commit `25cee34d6ff9f966eb9ba190e40efbd6eec3a5b9`." — project_2026-05-24_pr7048_merged_summary

> "Beads CLI verification: confirm `merge=beads` driver works post-merge in fresh clones (CR P1 concern resolved by reverting `.gitattributes` to main's version)." — project_2026-05-24_pr7048_merged_summary

## Connections
- [[7-Green-Proof-Artifact]] — VERDICT PASS comments that proved 7-green
- [[Competing-PR-Canonical-Field-Resolution]] — the resolution pattern
- [[CI-Expansion-Surfaces-Latent-Failures]] — the 9 latent failures fixed in-scope
- [[Self-Hosted-Runner-Infra-Flake-vs-Real-Failure]] — runner infra flake that hit this PR
- [[PR-6896-Location-Inline-Resolve]] — competing PR that won the race

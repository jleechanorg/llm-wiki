---
title: "PR #426: [agento] fix(skeptic): fix 3 bugs causing false VERDICT:FAIL in lifecycle-worker env"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldai_claw/pr-426.md
sources: []
last_updated: 2026-04-11
---

## Summary
Three bugs in `ao skeptic verify` caused `VERDICT:FAIL` for valid PRs when running from the lifecycle-worker (launchd) environment. All three were root-caused during the WA PR #6185 session.

**Bug 1 — `mergeGate.ts`: wrong CR_BOT login format**
- Was: `const CR_BOT = "coderabbitai[bot]"`
- Fixed: `const CR_BOT = "coderabbitai"`
- Why: GraphQL `author.login` returns `"coderabbitai"` (no `[bot]` suffix). The wrong constant meant zero CR reviews matched → `crApproved: false` for every PR.

**Bug 2

## Metadata
- **PR**: #426
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +563/-129 in 10 files
- **Labels**: none

## Connections

---
title: "[agento] fix(doctor): correct memory lookup command + skip when mem0 disabled"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-04
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/492
pr_number: 492
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background

doctor.sh fails with `[FAIL] Memory lookup command failed (rc=1)` on every run, causing monitor STATUS=PROBLEM. Two bugs:
1. Wrong command: `openclaw mem0 search` does not exist — correct is `openclaw memory search`
2. Missing disabled-plugin skip: when mem0 is intentionally disabled, output says plugin-disabled but rc=1. monitor-agent.sh handles this at line 671; doctor.sh was missing it.

## Goals
- doctor.sh exits 0 when mem0 is disabled (WARN not FAIL)
- monitor STATUS=OK afte...

## Key Changes
- 1 commit(s) in this PR
- 2 file(s) changed

- Merged: 2026-04-04

## Commit Messages
1. [agento] fix(doctor): correct memory lookup command + skip when mem0 disabled
  
  - openclaw mem0 search → openclaw memory search (invalid subcommand)
  - Add plugin-disabled guard before rc≠0 fail (mirrors monitor-agent.sh:671)
  - Add doctor/monitor parity rule + openclaw subcommand verify rule to CLAUDE.md
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `CLAUDE.md`
- `scripts/doctor.sh`

## Review Notes
1. @coderabbitai all good?

2. @coderabbitai all good?

3. @coderabbitai approve

4. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | already merged |\n| 3. CR approved | FAIL | state=none |\n| 4. Bugbot ...


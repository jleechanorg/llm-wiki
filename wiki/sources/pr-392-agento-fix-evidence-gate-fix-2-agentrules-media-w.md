---
title: "PR #392: [agento] fix(evidence-gate): Fix 2 agentRules media wire + Fix 3 claim floor enforcement"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldai_claw/pr-392.md
sources: []
last_updated: 2026-04-09
---

## Summary
Implements **Fix 2** (bd-4ze23) and **Fix 3** (bd-7s0d) from `roadmap/evidence-theater-diagnosis.md`:

- **Fix 2:** `defaults.agentRules` in `agent-orchestrator.yaml.example` instructs workers to use user-scope `tmux-video-evidence` (`~/.claude/skills/tmux-video-evidence/`), `smoke-test-local` (`~/.claude/skills/smoke-test-local/`) for integration+ claims, and never `N/A` for Terminal media on code-change PRs at integration+.
- **Fix 3:** `evidence-gate.yml` enforces a claim-class floor: if the

## Metadata
- **PR**: #392
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +52/-0 in 2 files
- **Labels**: none

## Connections

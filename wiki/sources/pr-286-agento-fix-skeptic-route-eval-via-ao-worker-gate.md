---
title: "PR #286: [agento] fix(skeptic): route eval via AO worker + gate on 6-green eligibility"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-286.md
sources: []
last_updated: 2026-03-29
---

## Summary
Fix skeptic CI/cron workflows to:
1. **No API keys in GHA** — LLM evaluation routes via AO worker (Codex OAuth, no secrets)
2. **Gate on 6-green eligibility** — only trigger skeptic for PRs passing gates 1-5 (CI, merge conflicts, CR, Bugbot, comments)
3. **Docs-only fast-path skip** — PRs with only markdown/text files are skipped

## Metadata
- **PR**: #286
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +944/-613 in 7 files
- **Labels**: none

## Connections

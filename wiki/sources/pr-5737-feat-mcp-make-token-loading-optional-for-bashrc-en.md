---
title: "PR #5737: feat(mcp): make token loading optional for bashrc environments"
type: source
tags: []
date: 2026-02-23
source_file: raw/prs-worldarchitect-ai/pr-5737.md
sources: []
last_updated: 2026-02-23
---

## Summary
- Skip ~/.token file requirement when tokens are already in environment (bashrc/profile)
- Check for GITHUB_TOKEN and GEMINI_API_KEY in environment first
- Only require ~/.token file as fallback for missing tokens
- Continue gracefully with warnings instead of failing on missing tokens

## Metadata
- **PR**: #5737
- **Merged**: 2026-02-23
- **Author**: jleechan2015
- **Stats**: +2/-81 in 1 files
- **Labels**: none

## Connections

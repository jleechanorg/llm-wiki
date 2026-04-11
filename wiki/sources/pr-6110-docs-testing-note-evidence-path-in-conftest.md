---
title: "PR #6110: docs(testing): note evidence path in conftest"
type: source
tags: []
date: 2026-04-06
source_file: raw/prs-worldarchitect-ai/pr-6110.md
sources: []
last_updated: 2026-04-06
---

## Summary
- Align MCP/UI testing evidence with repo-local `/tmp` layout (`/tmp/worldarchitectai/<repo_dir_name>/`) and document how to run script-style `testing_mcp` tests so evidence lands in the expected tree.
- Replace bulky in-repo evidence-standard copies with **stubs** pointing at user-scope canonical docs (`.cursor/rules/evidence-canonical.mdc`, `.claude/skills/…`, `.codex/skills/…`) and wire `CLAUDE.md` / `testing_mcp/CLAUDE.md` to those paths.
- Add **PR CI gate** (`.github/workflows/evidence-gat

## Metadata
- **PR**: #6110
- **Merged**: 2026-04-06
- **Author**: jleechan2015
- **Stats**: +490/-3284 in 19 files
- **Labels**: none

## Connections

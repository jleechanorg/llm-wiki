---
title: "PR #24: Move MCP Mail implementation to correct repo"
type: source
tags: [codex]
date: 2025-11-11
source_file: raw/prs-/pr-24.md
sources: []
last_updated: 2025-11-11
---

## Summary
- rewrite the `.mcp_mail/README.md` usage examples to use the actual JSONL workflow and clarify configuration/tool naming
- harden the MCP Mail integration tests for malformed lines and detached HEAD handling
- make CI and presubmit hooks resilient to missing smoke tests while checking for required tooling and prompting before replacing existing git hooks

## Metadata
- **PR**: #24
- **Merged**: 2025-11-11
- **Author**: jleechan2015
- **Stats**: +280/-75 in 7 files
- **Labels**: codex

## Connections

---
title: "Prompt Loading"
type: concept
tags: [prompt-loading, architecture]
sources: ["test-prompt-loading-via-service"]
last_updated: 2026-04-08
---

Pattern of loading prompt content from filesystem rather than hardcoding in code. Enables dynamic prompt updates without code changes.

## Mechanism
- Prompt files stored as .md in prompts/ directory
- PATH_MAP maps prompt type keys to file paths
- `_load_instruction_file` loads content on demand
- In-memory cache prevents redundant disk reads

## Testing
[[TestPromptLoadingViaService]] validates:
- All prompts loadable
- Unknown types raise errors
- Filesystem-service sync
- No dead prompts

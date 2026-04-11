---
title: "PR #467: Clean up pre-JSON mode references and ensure debug/narrative separation"
type: source
tags: []
date: 2025-07-10
source_file: raw/prs-worldarchitect-ai/pr-467.md
sources: []
last_updated: 2025-07-10
---

## Summary
This PR cleans up outdated instructions and warnings in the game state instruction prompts, removing references to deprecated patterns that the LLM no longer needs to know about.

### Changes Made

#### 1. Removed Outdated References
- Removed all references to deprecated [STATE_UPDATES_PROPOSED] blocks
- Cleaned up warnings about deprecated patterns (GOD_MODE_UPDATE_STATE, dot notation, etc.)
- Removed incorrect field count references
- Updated session header format to remove resources line

##

## Metadata
- **PR**: #467
- **Merged**: 2025-07-10
- **Author**: jleechan2015
- **Stats**: +1034/-543 in 12 files
- **Labels**: none

## Connections

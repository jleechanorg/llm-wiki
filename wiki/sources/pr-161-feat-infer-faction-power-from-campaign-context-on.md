---
title: "PR #161: feat: Infer faction power from campaign context on enable"
type: source
tags: []
date: 2025-06-29
source_file: raw/prs-worldarchitect-ai/pr-161.md
sources: []
last_updated: 2025-06-29
---

## Summary
- Route `enable_faction_minigame` through the classifier to FactionManagementAgent
- Enable LLM to infer faction power from campaign context (character backstory, narrative)
- Rescale AI faction FP ranges so player characters are competitive
- Ensure faction tools execute on the enable turn (not just subsequent turns)

## Metadata
- **PR**: #161
- **Merged**: 2025-06-29
- **Author**: jleechan2015
- **Stats**: +18/-0 in 1 files
- **Labels**: none

## Connections

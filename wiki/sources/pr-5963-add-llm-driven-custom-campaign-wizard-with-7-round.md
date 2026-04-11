---
title: "PR #5963: Add LLM-driven Custom Campaign Wizard with 7-round guided setup"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldarchitect-ai/pr-5963.md
sources: []
last_updated: 2026-03-16
---

## Summary
- Adds an LLM-driven Custom Campaign Wizard as an alternative to the existing "paste your prompt" campaign creation flow
- Custom Campaign now appears first (left card, selected by default), Dragon Knight second (right card)
- **One-click launch**: All three campaign modes (Dragon Knight, Guided Wizard, Paste Your Prompt) launch immediately when selected — no multi-step navigation needed
- New `CampaignWizardAgent` routes wizard rounds through the agent priority chain at position 1b (after GodMo

## Metadata
- **PR**: #5963
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +3869/-1010 in 42 files
- **Labels**: none

## Connections

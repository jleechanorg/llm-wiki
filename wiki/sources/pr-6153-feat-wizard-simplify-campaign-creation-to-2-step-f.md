---
title: "PR #6153: feat(wizard): simplify campaign creation to 2-step flow"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldarchitect-ai/pr-6153.md
sources: []
last_updated: 2026-04-09
---

## Summary
Streamlines the campaign creation wizard from 4 steps down to 2 steps (Type Selection → Launch). Removes the "AI Storytelling Options" checkboxes from the UI entirely, routing their logic into `collectFormData` where Dragon Knight forces all 3 settings on and Custom disables the Default World. Also fixes avatar file state leakages across wizard resets.

## Key Claims
- Wizard reduced from 4 steps to 2 steps (Type Selection → Launch)
- AI toggle UI completely removed; logic moved to backend `collectFormData` rule engine
- Dragon Knight campaigns enforce all 3 AI settings programmatically
- Custom campaigns disable Default World but keep Mechanics and Companions enabled
- Avatar component state leakage fixed via proper listener cleanup
- All 7 E2E MVP shards pass in strict mode

## Key Quotes
> "Refactored `campaign-wizard.js` to render a 2-step setup. Moved all character uploading logic, preview edits, and campaign summaries into a newly organized 'Launch' step."

## Metadata
- **PR**: #6153
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +279/-3079 in 14 files
- **Labels**: none

## Connections
- [[Campaign Wizard]] — 2-step flow (Type Selection → Launch)
- [[Dragon Knight]] — AI defaults enforced programmatically
- [[Custom Campaign]] — AI defaults enforced with Default World disabled

---
title: "PR #6196: fix(dragon-knight): restore missing FIELD_REWARDS_BOX in template extraction"
type: source
tags: [worldarchitect-ai, dragon-knight, template, rewards-box, pr-6196]
date: 2026-04-11
source_file: mvp_site/world_logic.py
---

## Summary
PR #6137 introduced the Dragon Knight template bypass in `world_logic.py:5012-5038` but silently omits `FIELD_REWARDS_BOX` from the extraction dict. Restores `rewards_box` emission on the opening turn of Dragon Knight campaigns by adding one line.

## Key Claims
- Dragon Knight pre-generated template bypasses the LLM call but was dropping `rewards_box` from extraction
- The template itself (`constants.py:1326`) already defines `"rewards_box": {}`
- The extraction was silently dropping it; one line added to restore

## Root Cause
PR #6137 (abd799c2e, merged 2026-04-09) introduced template bypass but omitted `FIELD_REWARDS_BOX` from the `fields` dict at world_logic.py:5012-5038.

## Files Changed
- `mvp_site/world_logic.py` (+3, -0)
- `mvp_site/tests/test_dragon_knight_rewards_box_extraction.py` (+110, -0)

## Testing
- Pre-commit ruff+format pass
- Pre-push type check + security scan pass
- 16 dragon-knight tests passing locally, 18 CI checks green
- Runtime browser reproduction not tested (requires captioned video + testing_ui/)

## Known Limitations / Out of Scope
- Does NOT address dice rolls rendering regression (separate PR #6194 / bead REV-rnz)
- Does NOT address debug messages rendering regression
- Does NOT address `has_visible_content` normalizer filter (fixed in PR #6193)

## Connections
- [[StructureDriftPattern]] — same root cause: checkpoint from PR #2162 placed fields in wrong structural location
- Bead: REV-rnz
- Related: PR #6193 (normalizer fix, merged), PR #6194 (dice investigation, open)

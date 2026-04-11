---
title: "PR #6165: fix(ui+state): keep final launch CTA visible and harden level-up atomicity"
type: source
tags: [worldarchitect-ai, launch-cta, level-up, wizard, atomicity, pr-6165]
date: 2026-04-11
source_file: mvp_site/frontend_v1/js/campaign-wizard.js
---

## Summary
Campaign creation wizard originally hid the standard bottom-right CTA on the final step. Also hardens level-up signaling to prevent stale level-up choices during polling. Both issues risked duplicate campaign launches and inconsistent level-up UI.

## Key Claims
- Final-step bottom-right CTA was hidden, making final launch flow inconsistent
- Level-up signaling could drift between `rewards_box` and `planning_block`, risking badge-without-buttons UI
- Both CTAs now route through a shared guarded launch helper that validates readiness once
- Backend `_enforce_rewards_box_planning_atomicity` now clearly documents and enforces the contract
- Stale level-up choices are scrubbed while preserving non-level-up legacy choices

## Tenets
- Prefer one guarded launch entrypoint over duplicated CTA-specific logic
- Fail closed on stale level-up state rather than emit badge-without-buttons UI
- Keep polling and immediate response contracts aligned

## Files Changed
- `mvp_site/frontend_v1/js/campaign-wizard.js` (+101, -8)
- `mvp_site/world_logic.py` (+49, -18)
- `mvp_site/tests/test_level_up_stale_flags.py` (+30, -5)
- `mvp_site/tests/test_milestone_4_interactive_features.py` (+151, -10)
- `testing_mcp/test_rewards_box_planning_block_e2e.py` (+1, -1)
- `docs/design/pr-designs/pr-6165.md` (+84, -0)

## Testing
- `python3 -m pytest mvp_site/tests/test_level_up_stale_flags.py mvp_site/tests/test_milestone_4_interactive_features.py -q`
- `npx eslint mvp_site/frontend_v1/js/campaign-wizard.js`

## Connections
- Related: [[StructureDriftPattern]] — level-up atomicity is a related state consistency concern

---
title: "PR #6039: [P2] [agento] /copilot: remove auto thread resolution + API reduction docs"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldarchitect-ai/pr-6039.md
sources: []
last_updated: 2026-04-05
---

## Summary
- Removed Step 8.5 (Post-Summary Delta Recheck) from `/copilot` — eliminates unconditional re-fetch of all comments after posting the consolidated reply
- Added Key Rule 8 to `copilot.md`: **do NOT auto-resolve conversation threads via API**; PR description tracking table is the authoritative record
- Added "Thread Resolution Policy" section to `_copilot_reference.md` with explicit allowed/not-allowed API call boundaries
- Added `api-reduction-design.md` with before/after API call table, future

## Metadata
- **PR**: #6039
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +179/-11 in 3 files
- **Labels**: none

## Connections

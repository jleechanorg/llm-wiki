---
title: "PR #145: [agento] fix(web): align API terminology with backend — use worlds not campaigns"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-145.md
sources: []
last_updated: 2026-03-29
---

## Summary
- Fix `mapWorldCollectionResponse` to use `worlds` key only (removed `campaigns` fallback)
- Update Dashboard test mocks to use `worlds` key (was using `campaigns` key)
- Update App test mocks to use `worlds` key
- Update NewCampaignWizard UI copy from "Campaign" to "World" terminology throughout
- Update all affected tests to match new UI copy

## Metadata
- **PR**: #145
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +55/-49 in 6 files
- **Labels**: none

## Connections

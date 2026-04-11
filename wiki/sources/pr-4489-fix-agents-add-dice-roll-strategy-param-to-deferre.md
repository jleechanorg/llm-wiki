---
title: "PR #4489: fix(agents): add dice_roll_strategy param to DeferredRewardsAgent"
type: source
tags: []
date: 2026-02-01
source_file: raw/prs-worldarchitect-ai/pr-4489.md
sources: []
last_updated: 2026-02-01
---

## Summary
- Fix TypeError in DeferredRewardsAgent when called with dice_roll_strategy parameter
- Add dice_roll_strategy: str | None = None to build_system_instructions() signature
- Ensures Liskov Substitution Principle compliance with parent class

**Key themes:**
- Signature compatibility fix for polymorphic agent calls
- TDD-driven bug fix with comprehensive test coverage

## Metadata
- **PR**: #4489
- **Merged**: 2026-02-01
- **Author**: jleechan2015
- **Stats**: +195/-0 in 3 files
- **Labels**: none

## Connections

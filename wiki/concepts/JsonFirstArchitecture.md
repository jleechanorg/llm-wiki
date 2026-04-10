---
title: "JSON-First Architecture"
type: concept
tags: [architecture, api-design, planning-blocks]
sources: [planning-block-cleanup-dev1314]
last_updated: 2026-04-08
---

Architecture pattern requiring LLM responses to include structured JSON data first, followed by narrative text. Ensures planning blocks and other structured data are captured in JSON fields rather than embedded in narrative.

**Benefits:**
- Consistent structured data extraction
- Clean separation of game state from narrative
- Easier frontend parsing and display
- Prevents narrative planning block corruption

**Implementation:** Prompt templates now enforce JSON planning_block field requirement.

**Related:** [[PlanningBlock]], [[TestPlanningBlockJsonFirstFix]]

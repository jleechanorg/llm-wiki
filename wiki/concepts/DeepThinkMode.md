---
title: "Deep Think Mode"
type: concept
tags: [ai-mode, planning, extended-thinking, narrative-generation]
sources: [planning-block-analysis-field-handling-tests]
last_updated: 2026-04-08
---

An AI generation mode that enables extended thinking and detailed planning block generation. When enabled, the model produces structured decisions with analysis fields (pros/cons, confidence scores) rather than simple narrative-only responses.

## Behavior
- Generates [[PlanningBlock]] with analysis structure
- Provides reasoning via "thinking" field
- Supports switch_to_story_mode flag to transition from planning to narrative execution

## Related Concepts
- [[PlanningBlock]] — output structure from Deep Think mode
- [[NarrativeResponse]] — response type enhanced by Deep Think

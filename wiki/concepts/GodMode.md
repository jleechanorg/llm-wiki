---
title: "God Mode"
type: concept
tags: [game-mode, ai-response]
sources: ["main-user-scenario-fix-god-mode-json"]
last_updated: 2026-04-08
---

Game mode where the AI responds without advancing the narrative. Unlike normal play where the AI generates story text in the `narrative` field, god mode uses the `god_mode_response` field for the AI's response.

## Technical Details
- `narrative` field stays empty in god mode responses
- Frontend displays `god_mode_response` directly instead of narrative
- Bug fix: malformed JSON now returns standardized error instead of exposing raw JSON keys

## Related Concepts
- [[ParseStructuredResponse]] — parses god mode responses
- [[Main User Scenario Fix — No Raw JSON in God Mode]] — validates error handling

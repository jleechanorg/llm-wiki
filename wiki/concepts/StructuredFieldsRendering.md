---
title: "Structured Fields Rendering"
type: concept
tags: [frontend, html-generation, structured-data, testing]
sources: ["frontend-structured-fields-tests-simple"]
last_updated: 2026-04-08
---

## Definition
Frontend rendering approach that transforms structured data objects into HTML. Handles multiple field types: dice_rolls (array), resources (string), planning_block (string), and debug-mode state updates.

## Key Characteristics
- **Conditional rendering**: Only renders fields that are present and non-empty
- **Debug mode toggle**: Debug features (living world updates) require explicit debugMode flag
- **Security**: All user-facing text passes through escapeHtml() to prevent XSS
- **Positioning**: planning_block always rendered last (bottom of display)

## Related Concepts
- [[Debug Mode]]
- [[Living World Updates]]
- [[Entity Escaping]]

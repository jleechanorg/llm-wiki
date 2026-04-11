---
title: "Planning Block Choice Buttons Styling"
type: source
tags: [css, interactive-fiction, ui, responsive-design, planning-block]
source_file: "raw/planning-block-choice-buttons.css"
sources: []
last_updated: 2026-04-08
---

## Summary
CSS stylesheet providing interactive styling for planning block choice buttons in interactive narrative experiences. Includes hover states, error displays, and responsive mobile layouts.

## Key Claims
- **Planning Block Layout** — Aggressively collapsed vertical spacing for choice lists
- **Choice Button Styling** — Full-width buttons with hover/active states and transitions
- **Custom Choice Support** — Dashed border styling for player-created choices
- **Error State Display** — Yellow warning background for malformed content
- **Mobile Responsive** — Reduced padding and font size under 768px

## Key CSS Classes
- `.planning-block-choices` — Collapsed margin/padding for tight lists
- `.choice-button` — Interactive choice buttons with cursor pointer
- `.choice-id` — Bold monospace choice identifiers with blue accent
- `.choice-description` — Gray choice text descriptions
- `.choice-button-custom` — Gradient styling for custom player actions
- `.planning-block-error` — Warning background for error states
- `.malformed-content` — Monospace styling for broken content

## Connections
- [[Narrative Directives]] — The narrative style guide this CSS supports
- [[Narrative Directives Lite]] — Lightweight narrative variant
- [[Story Pagination Styles]] — Pagination UI styling

## Contradictions
[]

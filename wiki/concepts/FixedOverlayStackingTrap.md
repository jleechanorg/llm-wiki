---
title: "Fixed overlay stacking trap (jsdom cannot see it)"
type: concept
tags: [css, stacking-context, testing, worldai_claw, packages/web]
sources: [feedback-2026-09-17-sprite-builder-swarm-five-traps]
last_updated: 2026-09-17
---

A `position:fixed; z-index:0` decorative layer rendered before the page content (worldai_claw `#root` starfield) paints **above** any later sibling that is `position:static`, because positioned elements with a z-index paint after in-flow content. Only descendants that form their own stacking context (e.g. `opacity < 1`) show through, which makes the symptom look random. DOM tests (jsdom, Testing Library) cannot detect it; a real browser capture with pixel counts on the target element does (`testing_ui/spritebuilder_live_check.py` pattern, 0 → 6485 bright pixels after the fix).

**Rule:** give every new top-level screen `position: relative; z-index: 1` (repo precedent: `.card > *` in styles.css), or fix the shell so the overlay sits at `z-index:-1` (follow-up in bead wc-yxptc). Always include one real headless screenshot in UI evidence.

Related: [[feedback-2026-09-17-sprite-builder-swarm-five-traps]], [[EvidenceReviewPipeline]].

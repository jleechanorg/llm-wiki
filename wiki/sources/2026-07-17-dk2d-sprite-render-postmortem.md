---
title: "DK2D sprite render postmortem — good atlases, unconfirmed downstream render bug (2026-07-17)"
type: source
tags: [dragonknight2d, sprite-rendering, postmortem, art-pipeline]
date: 2026-07-17
source_file: raw/project_2026-07-17_dk2d_sprite_render_postmortem.md
---

## Summary
Root flagged DK2D's on-screen characters as "totally wrong and way too low res" against a new enforced baseline video. Investigation into the actual live render path found the real character atlases are genuinely good quality — the defect is a downstream rendering bug, not bad source art. A separate, unrelated 32x32 asset pipeline was self-documented as inadequate by its own generating milestone but shipped to production anyway 7 hours later.

## Key Claims
- `/Users/jleechan/Documents/worldai 2d trim.mp4` (root's new visual baseline) is footage of the sibling `worktree_worldai_2d` project (a proven LPC top-down overworld renderer + real party sidebar UI), not an earlier DK2D session.
- The live DK2D render path (`game2dBridge.ts` → `game2d/render.ts` → `/assets/game/characters/<id>.png`) uses real 576x256 (9 cols x 4 rows of 64x64) walk-cycle atlases for `arion` and `gratian` that look clean and consistent at native resolution.
- A separate, deprecated pipeline (`packages/web/src/dragonknight/sprites/arion.png`, 32x32, downscaled from a 1024x1024 painting) was explicitly rejected by its own generating milestone doc (`ART_32x32_MILESTONE.md`: "signature-element fidelity gate FAILS... Do not treat these PNGs as final production art") but was wired into production 7 hours later anyway, with no caveat in the shipping commit message.
- The actual cause of the on-screen blob remains unconfirmed as of this writing — the leading hypothesis is a crop/scale bug in `game2d/render.ts`'s `drawFrame` or `game2dBridge.ts`'s cover-zoom math, not the source art itself.
- A follow-up ironclad-criteria mission (bead `wc-wh0t`, tracked via a spawned tmux sidekick) was created to root-cause and fix this plus a broader set of visual-quality gaps root's adversarial review identified (inconsistent art pipeline, static NPC "animation", tiny cover-zoomed world, canvas not enacting narrated prose, responsive cropping, web/SaaS UI chrome).

## Key Quotes
> "Do not treat these PNGs as final production art... Recommend against greenlighting full cast production from this recipe alone." — `ART_32x32_MILESTONE.md`, 2026-07-12, ~7 hours before the exact rejected assets shipped to production anyway.

## Connections
- [[DragonKnight2D]] — the game this postmortem concerns.
- [[SpriteChromaKeyPipeline]] — related sprite-generation pipeline work; this postmortem identifies a DIFFERENT downscale pipeline that was separately rejected-then-shipped.
- [[EvidenceHarnessDiscipline]] — the same discipline (real backend/LLM captures, never mocked) applied to the live-capture investigation that confirmed the atlases are good.

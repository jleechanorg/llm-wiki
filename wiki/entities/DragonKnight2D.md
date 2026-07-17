---
title: "DragonKnight2D"
type: entity
tags: [project, game, worldai-claw]
date: 2026-07-14
last_updated: 2026-07-17
---

Dragon Knight 2D ("The Silent Peace") — a Chrono-Trigger-register 2D LLM-GM game in the worldai_claw repo (branch dragonknight-2d-clean, PR #271). CHRONO mission (2026-07-13/14) unified it onto the game2d LPC engine that was already in the same source tree (the minimax-era build had ignored it and drawn flat rectangles): real autotiled terrain full-bleed, LPC walk cycles + name labels, camera follow, instant WASD traversal during LLM streaming, authored camp objects, 4-fork coda system. Sealed 15/15 harness gates at HEAD c26bd3d8; bundle-of-record ~/dk2d_evidence/RUN-CHRONO-SEAL2-20260714T155520Z.

2026-07-17: root rejected the shipped visual quality against a new baseline video (sibling worktree_worldai_2d footage). Postmortem found the real game2d character atlases are genuinely good quality — the on-screen defect is an unconfirmed downstream render/crop/scale bug, plus a separate self-documented-FAIL 32x32 asset pipeline that shipped anyway. New ironclad mission bead wc-wh0t (root-cause the render bug, art bible, bigger authored map, canvas-prose sync, responsive recompose) tracked via a spawned tmux sidekick.

Related: [[worldarchitect.ai]] · [[EvidenceHarnessDiscipline]] · [[SpriteChromaKeyPipeline]] · Source: [[feedback-2026-07-14-dk2d-chrono-operational-lessons]] · Source: [[2026-07-17-dk2d-sprite-render-postmortem]]

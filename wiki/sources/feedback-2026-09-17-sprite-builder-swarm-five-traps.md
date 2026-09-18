---
title: "Sprite-builder swarm five traps (2026-09-17, PR #436)"
type: source
tags: [swarm, worldai_claw, doclint, squash-merge, css-stacking, cross-model-review, workflow-tool, verify-pr-claims]
sources: [feedback_2026-09-17_sprite_builder_swarm_five_traps.md]
date: 2026-09-17
last_updated: 2026-09-17
source_file: raw/feedback_2026-09-17_sprite_builder_swarm_five_traps.md
---

## Summary
Learnings from the /swarm mission that built the Dragon Knight modular sprite builder ([PR #436](https://github.com/jleechanorg/worldai_claw/pull/436), sealed at 1548f688 with five ironclad criteria at one HEAD). Two are critical: squash-merging AUTHORITY-tracked docs breaks main's contracts doclint (a recurrence), and the web app's fixed starfield layer hides any new static-positioned screen while jsdom tests stay green. Three are operational: reviewer-CLI availability on this host, Workflow-tool junk structured results, and `verify_pr_claims.py` false negatives.

## Key Claims
- PR #434 squash-merged as 5a903f80 left `AUTHORITY.md` pointing at pre-squash SHA 3821894c; main and every PR that merged main failed the doclint until rows were refreshed at the base of the stack (#431 869c118b → #432 → #436).
- `#root`'s `position:fixed; z-index:0` starfield paints over static-positioned screens; fix is `position:relative; z-index:1` on the screen root (316ccc96); only a real headless capture catches it.
- codex was quota-blocked; `cursor-agent -f -p --output-format text` executed tests and attack scripts and returned `BLOCKING: 0` at the final head; `gemini -p --yolo` hung silently on long tool-using prompts.
- A Workflow-tool reader that repeatedly failed schema validation returned junk; the real report was the longest StructuredOutput attempt in its transcript.
- `verify_pr_claims.py` needs repo-relative paths and full 64-hex content hashes to avoid false "missing file/commit" claims.

## Key Quotes
> "MERGE COMMIT required (squash breaks AUTHORITY SHA doclint)" — earlier memory (2026-07-28), confirmed again here.
> "jsdom tests were 100% green while the page was invisible; the headless live check caught it."

## Connections
- [[AdversarialVerifyPipeline]] — cross-model executing review as the final gate; substitution rule when the named reviewer is unavailable.
- [[EvidenceReviewPipeline]] — evidence sealed at one HEAD with independent re-execution.
- [[CodeReviewMethodology]] — reviewer diversity (cursor executing vs Gemini static).
- [[SquashMergeAuthorityDoclintTrap]] — concept page for the recurring doclint break.
- [[FixedOverlayStackingTrap]] — concept page for the CSS stacking failure class.

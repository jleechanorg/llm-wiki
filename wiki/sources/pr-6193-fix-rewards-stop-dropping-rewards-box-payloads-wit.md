---
title: "PR #6193: fix(rewards): stop dropping rewards_box payloads with only level_up/progress"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6193.md
sources: []
last_updated: 2026-04-11
---

## Summary
On main (commit d868fec0c / PR #6161), the game UI stopped rendering the rewards_box when a player levels up. Investigation traced the regression to the new `mvp_site/rewards/` module pipeline introduced by PR #6161.

Evidence bundle: `/tmp/worldarchitect.ai/fix-rewards-box-dice-debug-render/investigation/latest/` — `/er` verdict **PASS** for investigation scope.

**Fix PR Evidence Gist:** https://gist.github.com/jleechan2015/4f694d18542f16d137f450c829fc441f (157 reward tests passing, 0 failures

## Metadata
- **PR**: #6193
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +0/-4 in 1 files
- **Labels**: none

## Connections

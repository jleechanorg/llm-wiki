---
title: "ZFC Level-Up PR Tracking"
type: concept
tags: [zfc, level-up, execution, tracking]
date: 2026-04-21
---

## Definition
An 8-lane sequential PR execution model for ZFC level-up migration, tracking 8 task specs with dedicated beads from rev-lmdo through rev-v0x7.

## Lane Structure
- **Item 1** (rev-lmdo): Replacement narrow enforcement PR after #6420
- **Item 2** (rev-23eq): M1 model compliance MVP evidence PR
- **Items 3-7** (rev-7yt7/cujw/usv2/c726/ahpi): M2 sequential deletion PRs
- **Item 8** (rev-v0x7): M3 final enforcement PR

## Tracking States
`bead only` → `branch opened` → `draft PR open` → `blocked` → `done`

## Related
- [[Level-Up Bug Chain]]
- [[Normalization Atomicity]]
- [[PR #6420]], [[PR #6404]], [[PR #6434]]

---
title: "Smartclaw"
type: entity
tags: [smartclaw, project, repository]
sources: [smartclaw-routing-delegation-failures-postmortem.md]
last_updated: 2026-04-07
---

## Description
Target repository for the delegation flow that experienced routing failures in March 2026. The delegation intended to produce work in smartclaw but initially created work in worldarchitect.ai due to missing repo contract in the dispatch prompt.

## Related Entities
- [[Jleechanclaw]] — source repository for delegation
- [[Worldarchitect.ai]] — repository where incorrect work was initially performed

## Events
- 2026-03-19: Delegation routing failure postmortem conducted
- Corrective actions: explicit SOURCE_REPO/TARGET_REPO headers added

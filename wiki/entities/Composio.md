---
title: "Composio"
type: entity
tags: ["company", "framework", "orchestration", "agent-orchestrator"]
sources: ["orchestration-architecture-research"]
last_updated: 2026-04-07
---

Open-source agent-orchestrator with production data: 30 parallel agents running simultaneously, 61 PRs merged from 102 created (60% success rate), 377 automated reviews, 700 inline code comments catching real issues, 68% immediate fixes by agents reading feedback. Zero human commits to feature branches. Built with 40,000 lines of TypeScript, 17 plugins, 3,288 tests in 8 days.

## Key Patterns
- Reaction engine: CI failure triggers agent spawn, changes requested triggers agent spawn
- Three-layer review: Automated (69%), agent-to-agent (30%), human (1%)

## See Also
- [[Orchestration Architecture Research]] — detailed production data in research
- [[Reaction Engine]] — concept page for Composio's pattern

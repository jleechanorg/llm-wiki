---
title: "2026-06-13 Claw Always Show Attach Urls"
type: source
tags: ["feedback", "worldarchitect", "agent-orchestrator"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_claw_always_show_attach_urls.md
---

## Summary
After every /claw dispatch always show ao attach, dashboard, log monitor lines

## Key Claims
- After every `/claw` invocation, always output monitoring lines in the reply — never omit them.
- ✅ AO worker spawned: <session-name>
- Attach:    ao attach <session-name>
- Dashboard: ao session ls --project <project>
- Status:    ao status <session-name>
- Run `ao session ls --project <project>` immediately after spawn to get the session name.

## Connections
- [[WorldarchitectAI]] — worldarchitect.ai project memory
- [[AgentOrchestrator]] — AO worker dispatch memory
- [[KarpathyWikiPattern]] — wiki-ingest protocol
- Source: `raw/feedback_2026-06-13_claw_always_show_attach_urls.md`

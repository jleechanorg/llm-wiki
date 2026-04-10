---
title: "Tool Requests"
type: concept
tags: [llm, tools, streaming]
sources: []
last_updated: 2026-04-08
---

## Definition
JSON structure returned by LLM indicating desired tool invocations. When an LLM response contains tool_requests, the system triggers Phase 2 streaming to execute those tools.

## Context
In the OpenClaw game server, tool_requests are embedded in the JSON response from the LLM and have this structure:
```json
{"tool": "roll_dice", "args": {"notation": "1d20"}}
```

When tool_requests are present, Phase 2 streaming is triggered to execute the tools and continue the narrative.

## Related
- [[Phase2Streaming]]
- [[continue_story_streaming]]

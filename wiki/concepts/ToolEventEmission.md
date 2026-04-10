---
title: "Tool Event Emission"
type: concept
tags: [streaming, events, tools]
sources: []
last_updated: 2026-04-08
---

## Description
In the streaming path, when tool requests exist in the LLM response, the system emits events for:
- tool_start: Indicates a tool is about to be executed
- tool_result: Contains the tool execution result
- state: Contains state updates from the response

## Test Coverage
- [[LLM Service Context Extraction Tests]] — test_continue_story_streaming_emits_tool_and_state_events

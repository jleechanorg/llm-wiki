---
title: "LLM Integration"
type: concept
tags: [llm, integration, worldarchitect]
sources: []
last_updated: 2026-04-08
---

## Summary
LLM Integration refers to how all agents in WorldArchitect connect to the language model service (Gemini, Cerebras, etc.) for generating responses. Every agent—StoryModeAgent, GodModeAgent, and SpicyModeAgent—uses the same LLM service integration layer.

## Integration Points
- **Request Building**: Agents construct prompts with system instructions and user input
- **Response Parsing**: Agents extract structured data from LLM responses
- **Error Handling**: Integration layer handles rate limits, timeouts, and API errors
- **Caching**: Optional explicit caching to reduce LLM calls

## Agent-Specific Integration
- **StoryModeAgent**: Sends narrative prompts, receives story text + choices
- **GodModeAgent**: Sends admin commands, receives confirmation responses
- **SpicyModeAgent**: Sends prompts with content guidelines, receives appropriate narrative

## Related Concepts
- [[AgentArchitecture]] — all agents use LLM integration
- [[StoryModeAgent]] — LLM for story generation
- [[GodModeAgent]] — LLM for command processing
- [[SpicyModeAgent]] — LLM for adult content generation

## Source References
- [[Agent Architecture End-to-End Integration Test]] — validates agent-LLM service integration

---
title: "test_agents_integration.py"
type: source
tags: [testing, agents, integration, mode-detection]
date: 2026-04-14
source_file: raw/mvp_site_all/test_agents_integration.py
---

## Summary
Integration tests for the Agent architecture in WorldArchitect.AI, verifying mode detection (story mode vs god mode), system instruction building, agent prompt sets, backward compatibility imports, and edge case handling.

## Key Claims
- Story mode agent (StoryModeAgent) correctly handles narrative inputs like "I attack the goblin" and "What do I see around me?"
- God mode agent (GodModeAgent) correctly detects "GOD MODE:" prefix at start of input
- Agent instruction building loads prompt files and constructs system instructions dynamically
- Story mode and god mode share core prompts: MASTER_DIRECTIVE, GAME_STATE, DND_SRD
- Agents can be imported from both `mvp_site.llm_service` and `mvp_site.agents` for backward compatibility
- Dialog agent handles both explicit dialog context and keyword-based matching

## Key Quotes
> "GOD MODE:" prefix must be preserved at start for system instruction pattern matching

## Connections
- [[mvp-site-agents]] — The agents module being tested
- [[mvp-site-agent-prompts]] — Prompt file loading and instruction building
- [[mvp-site-constants]] — Mode constants and prompt types

## Contradictions
- None identified in test file
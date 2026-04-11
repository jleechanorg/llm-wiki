---
title: "Testing MCP - Server-Level Tests with Real LLMs"
type: source
tags: [testing, mcp, worldarchitect, ai, e2e, integration]
sources: []
date: 2026-04-07
source_file: testing_mcp/README.md
last_updated: 2026-04-07
---

## Summary
Documentation of WorldArchitect.AI's server-level testing framework that hits a running MCP server over HTTP. The testing_mcp directory enforces a strict no-mocks policy, using real LLM calls when the target server has API keys configured.

## Key Claims
- **Real LLM Behavior**: Tests make actual API requests to Gemini/Cerebras/OpenRouter via the MCP server - no mocked responses
- **No Application Unit Tests**: The `testing_mcp/` directory forbids pure unit tests with mocked server behavior; it's reserved for real API, E2E, and server-integration tests only
- **Exception for Test Utilities**: `*_unit.py` files for testing_mcp/lib/ utilities (e.g., `test_evidence_utils_unit.py`) are permitted since they test the testing infrastructure itself
- **Claude Code Web Compatible**: Tests use direct importlib imports to bypass problematic `__init__.py` chains in restricted environments
- **Parallel Worker Support**: Tests can run multiple workers against the same MCP server for better throughput

## Key Quotes
> "These tests do not call Gemini/Cerebras/OpenRouter APIs directly - instead, they send HTTP requests to an MCP server which calls the LLM APIs."

> "NO mocked LLM responses: Tests fail if LLM returns wrong schema"

> "Policy: No Application Unit Tests In `testing_mcp/` — forbidden: pure unit tests for application code, isolated function tests with mocked server behavior"

## Available Test Suites

| Test File | Description |
|-----------|-------------|
| `test_deferred_rewards_agent_real_e2e.py` | DeferredRewardsAgent E2E with parallel injection, semantic routing |
| `test_dialog_agent_real_e2e.py` | DialogAgent E2E with real LLM, natural routing |
| `test_combat_agent_real_e2e.py` | Combat agent E2E |
| `test_rewards_agent_real_e2e.py` | Rewards agent E2E |
| `test_living_world_real_e2e.py` | Living world system |
| `test_god_mode_validation.py` | God mode commands |

## Connections
- [[WorldArchitect.AI]] — the platform being tested
- [[Testing MCP - Agent Instructions]] — the agent instructions for the testing framework

## Contradictions
- None detected
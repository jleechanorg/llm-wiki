---
title: "Testing Design Document"
type: source
tags: [worldarchitect.ai, testing, mcp, http, ui, playwright, test-architecture, test-design]
sources: []
source_file: worldarchitect.ai-docs-testing_design.md
date: 2026-03-18
last_updated: 2026-04-07
---

## Summary

Comprehensive test design strategy for WorldArchitect.AI across three testing layers: MCP Tests (protocol-level), HTTP Tests (REST API), and UI Tests (browser-based with Playwright). Each layer builds upon base test classes addressing core user flows: Authentication, Campaign Creation, and Gameplay Actions.

## Key Claims

- **Three-Layer Architecture**: MCP Tests (`testing_mcp/`) → HTTP Tests (`testing_http/`) → UI Tests (`testing_ui/`) - each builds on the previous
- **MCPTestBase Features**: Local MCP server lifecycle, MCPClient wrapper, TestContext for state management, evidence collection, streaming SSE capture
- **HTTP Test Features**: WAHttpTest base class, pre-configured auth bypass headers, session management, test data fixtures, validation helpers
- **UI Test Features**: Playwright automation, Firebase auth token generation, campaign/game helpers, screenshot utilities, video recording support
- **Core User Flows Covered**: Authentication (OAuth → Firebase → Session), Campaign Creation (3-step wizard), Gameplay Actions (process_action, state management)

## Key Components

### MCP Test Base (`testing_mcp/lib/base_test.py`)
- `start_server()` / `restart_server()` - Server lifecycle
- `run_scenarios(ctx: TestContext)` - Abstract method for test scenarios
- `ctx.create_campaign()` - Campaign creation helper
- `ctx.process_action()` - Send user input to campaign
- `ctx.collect_route_stream_events()` - Capture SSE streaming

### HTTP Test Base (`testing_http/lib/`)
- `WAHttpTest` - Base class extending `testing_utils.http_test.HttpTestBase`
- `get_test_session()` - Authenticated requests session
- `make_authenticated_request()` - Helper for authenticated calls
- `CAMPAIGN_TEST_DATA`, `TEST_SCENARIOS` - Test data fixtures

### UI Test Base (`testing_ui/lib/browser_test_base.py`)
- `start_test_server()` - Server lifecycle
- Firebase token creation for auth
- `wait_for_element()` / `click()` / `fill()` helpers
- `save_screenshot()` - Screenshot capture
- Video recording support

## Test Coverage by User Flow

| User Flow | MCP Tests | HTTP Tests | UI Tests |
|-----------|-----------|------------|-----------|
| Authentication | OAuth token exchange, test auth bypass, token refresh | Auth endpoint health, session cookie, invalid token rejection | OAuth button visibility, redirect verification, logged-in state |
| Campaign Creation | Full wizard completion, title validation, setting options, presets | - | - |
| Gameplay Actions | State transitions, streaming events | - | - |

## Connections

- [[Campaign Creation Test Results - PR #1551]] — Uses MCPTestBase for campaign testing
- [[Testing MCP - Server-Level Tests with Real LLMs]] — Real LLM E2E testing framework
- [[Browser Automation Comparison: Playwright vs Superpowers Chrome]] — Playwright vs alternative browser automation

## Contradictions

None identified.
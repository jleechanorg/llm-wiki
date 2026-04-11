---
title: "MCP Server Health Checks"
type: source
tags: [python, testing, mcp, health-check, configuration]
source_file: "raw/test_mcp_server_health.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating MCP server configuration and connectivity using red-green methodology. Tests verify React MCP server installation, WorldArchitect game server running on port 7000, and Claude Desktop config contains all required servers. Supports both local development and CI environments with appropriate skipping.

## Key Claims
- **React MCP server validation**: Tests verify react-mcp directory and index.js exist when REACT_MCP_ENABLED=true
- **WorldArchitect server connectivity**: Tests port 7000 connectivity on multiple hosts (localhost, 127.0.0.1, WSL2 IPs) with environment variable override via MCP_TEST_HOSTS
- **CI environment detection**: Automatically skips server connectivity checks in CI/GitHub Actions environments
- **MCP config validation**: Tests Claude Desktop config contains all required servers (sequential-thinking, context7, gemini-cli-mcp, github-server, filesystem)

## Key Quotes
> "Test MCP server health checks to ensure all servers are properly configured"

## Connections
- [[React MCP]] — React MCP server requiring index.js in react-mcp/ directory
- [[WorldArchitect]] — Game server expected on port 7000
- [[Claude Desktop]] — Hosts MCP configuration at ~/.config/claude/claude_desktop_config.json

## Contradictions
- None identified

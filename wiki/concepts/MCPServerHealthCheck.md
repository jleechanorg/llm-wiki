---
title: "MCP Server Health Check"
type: concept
tags: [mcp, testing, health-check, validation]
sources: [mcp-server-health-checks]
last_updated: 2026-04-08
---

Testing methodology for validating MCP server configuration and connectivity. Uses red-green TDD approach with automatic CI environment detection that skips server connectivity tests when running in CI/GitHub Actions.

## Validation Steps
1. React MCP: directory and index.js existence check
2. WorldArchitect: socket connectivity to port 7000
3. Claude Desktop config: required server list verification

## Environment Variables
- REACT_MCP_ENABLED - enable React MCP validation
- MCP_TEST_HOSTS - comma-separated hosts for connectivity testing
- CI / GITHUB_ACTIONS - auto-skips server connectivity in CI

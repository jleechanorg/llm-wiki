---
title: "MCP Server Migration Guide: Old Launchers → New Installer"
type: source
tags: [mcp, migration, installer, scripts, worldarchitect]
sources: []
date: 2026-04-07
source_file: scripts/MIGRATION.md
last_updated: 2026-04-07
---

## Summary
Migration guide documenting the replacement of old launcher scripts (`claude_mcp.sh`, `codex_mcp.sh`) with a unified installer (`scripts/install_mcp_servers.sh`). The new installer provides unified interface for both Claude and Codex, better organization in `scripts/` directory, user scope default for global availability, and improved error handling.

## Key Claims
- **Unified Interface**: One script replaces two separate launchers (`./scripts/install_mcp_servers.sh [claude|codex|both]`)
- **User Scope Default**: Always installs to user scope for global availability without needing `MCP_SCOPE=user`
- **Better Error Handling**: Checks if CLI is installed before proceeding with clear error messages
- **Environment Variable Loading**: Automatically loads API keys from `.bashrc` for Codex
- **Backward Compatible**: Sources same `mcp_common.sh`, preserving custom modifications
- **Smart Detection**: Detects existing servers and skips reinstallation

## Key Quotes
> "The old launcher scripts in project root have been replaced with a unified installer"

> "But the **new installer defaults to user scope** (global availability), so you don't need to specify it!"

## Connections
- [[worldarchitect.ai-docs-pr-1405-changes.md-2c1149ac.md]] — Related to MCP server integration and file consolidation
- [[beads-docs-daemon-management.md-ef4a5d79.md]] — Daemon management for MCP servers

## Contradictions
- None identified

## Migration Verification

```bash
# Check Claude servers
claude mcp list

# Check Codex servers
codex mcp list

# All should show: Scope: User config (available in all your projects)
```

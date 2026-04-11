---
title: "MCP Server Installation Guide"
type: source
tags: [mcp-servers, installation, claude-code, codex, tooling]
sources: []
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary
Comprehensive guide for installing MCP (Model Context Protocol) servers globally for Claude Code and Codex. Covers installation scripts, 15+ MCP servers across categories (core infrastructure, documentation/search, AI models, browser automation, cloud services), advanced usage options, and troubleshooting.

## Key Claims
- **Global Installation Recommended**: Installing MCP servers at user scope makes them available in every project, eliminating per-repo setup.
- **15+ MCP Servers Available**: Categories include core (filesystem, serena, memory-server), documentation (context7, ddg-search, perplexity-ask), AI models (gemini-cli-mcp, grok), browser automation (chrome-superpower, playwright-mcp, ios-simulator-mcp), and cloud services (render, worldarchitect).
- **Cross-Platform Copy Mechanism**: Installer scripts can be copied to new repos to replicate MCP setup via `cp scripts/mcp_common.sh ~/new-repo/scripts/`.
- **API Key Requirements**: Some servers require environment variables (XAI_API_KEY, PERPLEXITY_API_KEY, RENDER_API_KEY, GITHUB_TOKEN).

## Key Quotes
> "The script detects existing servers and skips or updates as needed" — auto-update behavior

> "All data stays local, no cloud transmission" — privacy-first design principle

## Connections
- [[MCP Server Installation]] — related installation procedures
- [[Claude Code]] — primary integration target
- [[Codex]] — secondary integration target

## Contradictions

---
title: "MacBook Dev Environment Setup Guide"
type: source
tags: [macbook, development-environment, setup-guide, homebrew, nvm, rust, ai-tools]
sources: []
source_file: world_reference/macbook_dev_environment_setup_guide.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary
Comprehensive setup script and configuration guide for replicating the WorldArchitect.AI development environment on a new MacBook, covering system prerequisites, development tools, Claude Code/AI tooling, and environment configuration.

## Key Claims

- **System Prerequisites**: Xcode Command Line Tools and Homebrew installation with PATH configuration for both Apple Silicon and Intel Macs
- **Node.js via NVM**: Recommended approach using NVM v0.39.0 for version management — installs Node 20.19.4 as default
- **Claude Code Router**: `@musistudio/claude-code-router@1.0.38` for routing Claude Code requests
- **AI/LLM Tools**: Gemini CLI 0.1.18, Qwen Code 0.0.7 (Cerebras), Claude Code Enhanced, and usage monitor 15.6.0
- **Development Utilities**: DuckDuckGo search CLI, Graphite CLI for git workflow, Rust-based code scheduler via cargo
- **Python Tools**: UV for fast package installation, pytest, RunPod/VastAI CLIs for cloud GPU access
- **Shell Aliases**: Project-specific shortcuts (wa, push, commit, integrate) and Claude Code launch variants (claudep, claudepw, claudepc, etc.)
- **Virtual Environment Function**: `vpython()` function for activating project-specific Python venvs
- **Environment Variables**: Separate ~/.env_secrets file with API keys for Claude, Notion, Gemini, Cerebras, OpenAI, Firebase, and cloud GPU providers

## Connections

- [[ClaudeCodeWSL2MemoryLeakWorkarounds]] — related to Claude Code setup and configuration
- [[DevelopmentScripts]] — similar automation scripts theme

## Contradictions

- None detected

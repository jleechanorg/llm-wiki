---
title: "Command System Documentation"
type: source
tags: [claude-code, commands, slash-commands, automation]
sources: []
last_updated: 2026-04-14
---

## Summary

Comprehensive documentation for the Claude Code slash command system. This system provides 80+ executable markdown commands organized by category (execution, planning, testing, git, orchestration, quality, AI, research, review) along with Python automation scripts and shell utilities.

## Key Claims

- Two command types: Cognitive Commands (/think, /debug, /planexec) for natural language processing, and Operational Commands (/orch, /execute, /push) for direct system operations
- Markdown commands are executable specifications read by Claude and executed as instructions
- Python scripts handle system operations and API integration
- Shell scripts provide system-level automation and workflow orchestration
- Command files must begin with YAML frontmatter (description, type, execution_mode)

## Key Quotes

> "Every executable slash command markdown file in this directory must begin with the following YAML front matter block"

> "Commands without this header are considered invalid and should be updated before use"

## Connections

- [[PairProtocol]] — Uses MCP mail for agent-to-agent coordination
- [[HarnessEngineering]] — Quality validation commands (fake.md, fake3.md)
- [[Claw]] — Orchestration commands for agent dispatch

## Contradictions

- None identified

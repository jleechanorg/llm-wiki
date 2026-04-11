---
title: "Claude Code Complete System Prompt - Raw Capture"
type: source
tags: [claude-code, system-prompt, anthropic, cli-tool, raw-capture]
sources: []
date: 2025-09-08
last_updated: 2026-04-07
---

## Summary

Raw capture of the complete system prompt used by Claude Code 1.0.108, obtained via HTTP proxy method intercepting Anthropic API calls. The prompt is ~32,532 characters (~7,009 tokens) and defines Claude Code's core behavior: concise responses (under 4 lines unless detail requested), tool-assisted task completion, defensive security focus, and strict output minimization.

## Key Claims

- **Raw System Prompt Capture**: Obtained via custom Python proxy intercepting Anthropic API calls on 2025-09-08, capturing Claude Code 1.0.108's actual system prompt
- **Concise Output Mandate**: Must answer with fewer than 4 lines, minimize tokens while maintaining quality, no unnecessary preamble/postamble
- **Tool-First Philosophy**: Uses tools to complete tasks rather than explaining what will be done; runs commands to gather information before answering
- **Defensive Security Focus**: Only assists with defensive security tasks, refuses malicious code creation/modification/improvement
- **Professional Objectivity**: Prioritizes technical accuracy over validating user beliefs; provides direct, objective technical info without superlatives or emotional validation

## Key Quotes

> "You are Claude Code, Anthropic's official CLI for Claude."

> "IMPORTANT: You should minimize output tokens as much as possible while maintaining helpfulness, quality, and accuracy."

> "When you run a non-trivial bash command, you should explain what the command does and why you are running it."

> "Only use emojis if the user explicitly requests it. Avoid using emojis in all communication unless asked."

## Connections

- [[Claude Code]] — the CLI tool this system prompt governs
- [[Anthropic]] — the company behind Claude Code
- [[WorldArchitect.AI]] — platform where this capture was documented

## Contradictions

- None identified — this is a primary source documenting Claude Code's actual behavior
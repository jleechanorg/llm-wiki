---
title: "Copilot Command Family Development Guidelines"
type: source
tags: [copilot, command-family, implementation, worldarchitect, pr-automation]
sources: []
date: 2025-09-20
source_file: copilot-command-family-guidelines.md
last_updated: 2026-04-07
---

## Summary
Guidelines for developing a three-command copilot family (`/copilot`, `/copilot-lite`, `/copilot-expanded`) as explicitly requested by the user. Emphasizes implementation-first approach over analysis paralysis, with /copilot_expanded as the highest priority for making functional.

## Key Claims
- **Three-Command Requirement**: User explicitly requested `/copilot`, `/copilot-lite`, and `/copilot-expanded` — must be clearly stated in PR description
- **Priority Order**: /copilot_expanded is highest priority — make it fully functional before adding other commands
- **Integration-First Protocol**: Add commands to existing `.claude/commands/` directory, never create new directories
- **Default "No New Files"**: Only create new command files in existing infrastructure, no new utility/test files
- **Implementation Over Analysis**: Focus on making commands work, not on alternative architectures

## Key Quotes
> "User instructions = law. The user wants three specific commands. Implement them as requested without changing the requirements or over-analyzing alternatives."

> "MAKE /COPILOT-EXPANDED ACTUALLY WORK — Implementation over analysis"

## Commands

### /copilot — Standard Analysis
Standard PR review with comment analysis and basic fixes:
- PR comment processing
- Basic code quality checks
- Standard security review
- Moderate automation level

### /copilot-lite — Lightweight Version
Quick analysis for simple PRs or time-constrained reviews:
- Essential comment processing only
- Fast execution (< 2 minutes)
- Core quality checks
- Minimal automation

### /copilot_expanded — Comprehensive Automation
Complete PR processing with full automation and enhancement:
- All features from /copilot and /copilot_lite
- Comprehensive security analysis
- Full code quality enhancement
- Maximum automation level

## Anti-Patterns to Avoid
- ❌ Over-analysis: Suggesting alternative architectures when user is clear
- ❌ Scope creep: Adding features not requested
- ❌ File creation: Creating new directories or test files without permission
- ❌ Analysis paralysis: Questioning requirements instead of implementing

## Success Criteria
1. PR description must clearly state: "Implements three copilot commands as requested: /copilot, /copilot-lite, /copilot_expanded"
2. /copilot_expanded.md must be fully functional with complete automation
3. Clear command differentiation with usage examples and feature matrix
4. User can type /copilot_expanded and get complete PR processing without manual intervention

## Contradictions
- None identified — guidelines align with existing wiki principles about following user instructions

## Connections
- [[Copilot Analysis Report - PR #1440: Documentation and Guides]] — related PR that may contain copilot command implementation
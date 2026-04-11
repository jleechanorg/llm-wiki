---
title: "Review Command Retest Prompt"
type: source
tags: [claude-code, testing, slash-commands, research-methodology, source-authority]
sources: []
date: 2026-04-07
source_file: raw/review_command_retest_prompt.md
last_updated: 2026-04-07
---

## Summary
Test prompt to verify the `/research` command correctly identifies `/review` as a built-in Claude Code CLI command and maintains proper source authority hierarchy (official documentation > secondary sources).

## Key Claims

### Required Behaviors
- **Find Built-in `/review` Command**: Must correctly identify `/review` as a built-in Claude Code CLI command
- **Reference Official Documentation**: Must cite https://docs.anthropic.com/en/docs/claude-code/slash-commands as primary source
- **Describe Functionality**: Must explain that `/review` analyzes code quality, identifies bugs, and suggests improvements
- **Show Proper Source Authority**: Must prioritize official Anthropic documentation over secondary sources

### Failure Indicators
- Concluding `/review` is "not a built-in command"
- Failing to find or reference official documentation
- Prioritizing secondary sources (GitHub repos, blogs) over official docs
- Suggesting `/review` doesn't exist or is only available as custom command

## Source Authority Hierarchy

1. **Primary Sources** (Highest Authority):
   - Official Anthropic documentation (docs.anthropic.com)
   - Claude Code CLI official help/documentation

2. **Secondary Sources** (Supporting Evidence):
   - GitHub repositories with slash command implementations
   - Community discussions about Claude Code CLI
   - Technical blogs and tutorials

3. **Tertiary Sources** (Background Context):
   - General AI/CLI tool discussions
   - Related but not specifically Claude Code CLI content

## Background: The Original Error Pattern

- **Search Query**: "Claude Code CLI review command"
- **Methodology Failure**: Source Authority Inversion
- **Incorrect Conclusion**: "/review is not a built-in command"
- **Root Cause**: Prioritized secondary sources over official documentation

## Test Validation

### Pass Criteria
Research correctly identifies `/review` as built-in with official documentation citation

### Fail Criteria
Research concludes `/review` is not built-in or fails to find official documentation

## Connections
- [[ResearchReproducibilityTestReport]] — prior test confirming `/review` is built-in
- [[ClaudeCodeSlashCommands]] — official documentation source

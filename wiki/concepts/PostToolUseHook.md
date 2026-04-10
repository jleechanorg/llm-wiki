---
title: "PostToolUse Hook"
type: concept
tags: [claude-code, hooks, automation]
sources: [command-output-trimmer-hook]
last_updated: 2026-04-07
---

## Definition
A Claude Code hook that fires after a tool executes, allowing inspection and transformation of tool output.

## Configuration
Configured in `.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash(*)",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c '...'",
            "description": "Description"
          }
        ]
      }
    ]
  }
}
```

## Use Cases
- Output transformation/compression
- Logging and analytics
- Automated responses to tool results
- Quality gates and validation

## Related Concepts
- [[CommandOutputTrimmer]] — example of PostToolUse hook application
- [[PreToolUseHook]] — fires before tool execution
- [[ClaudeCodeHooksSystem]] — the overall hook architecture

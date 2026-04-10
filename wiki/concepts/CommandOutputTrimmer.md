---
title: "Command Output Trimmer"
type: concept
tags: [compression, output-processing, hook-system]
sources: [command-output-trimmer-hook]
last_updated: 2026-04-07
---

## Definition
A smart compression system that intercepts verbose CLI command outputs and applies intelligent compression rules while preserving essential information.

## How It Works
1. **Pattern Detection**: Identifies command type from output patterns (e.g., pytest output, git push output)
2. **Rule Application**: Applies command-specific compression rules
3. **Fallback Handling**: Uses generic compression (first 20 + last 10 lines) for unrecognized commands

## Key Compression Strategies
- **Preserve**: Errors, failures, critical debug info, important links
- **Compress**: Repetitive patterns, progress indicators, verbose details
- **Limit**: Maximum N lines of specific content types

## Related Concepts
- [[PostToolUseHook]] — the Claude Code hook mechanism used for integration
- [[ContextWindowOptimization]] — similar goal of managing context consumption
- [[OutputParsing]] — related to extracting structured data from command outputs

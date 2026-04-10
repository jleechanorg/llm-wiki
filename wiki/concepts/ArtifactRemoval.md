---
title: "Artifact Removal"
type: concept
tags: [parsing, fix, code-execution]
sources: []
last_updated: 2026-04-07
---

## Description
Fix implementation that removes non-JSON prefixes from LLM responses. Checks if response doesn't start with `{`, finds the actual JSON start (first `{` or `[` that starts the valid JSON), and strips everything before it.

## Related
- [[NarrativeResponseSchema]] — file containing the fix
- [[JSONParsing]] — process being fixed

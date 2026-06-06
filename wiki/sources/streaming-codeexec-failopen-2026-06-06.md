---
title: "Streaming code-exec fail-open RCA — 2026-06-06"
type: source
date: 2026-06-06
tags: [worldarchitect, gemini, streaming, code-execution, fail-open]
---

# Streaming code-exec fail-open RCA

## Summary

WorldArchitect preview campaign `8J0RzsHVHH1GLg6E6BLM` persisted
`The story continues...` with `Missing action_resolution field` because the
Gemini streaming request applied code-execution instructions without attaching
the code-execution tool.

The recovered raw payload was:

- `sha256=1b2c8bbfb79b085b8af7976183f88ff230bb57fc1d4576bf03203b7767a0295c`
- `bytes=2070`
- top-level JSON list length `2`
- both items `tool=code_execution`
- both items contained only `args.code`
- no normal text part
- no observed `code_execution_result.output`

## Lesson

For Gemini streaming placeholder/fail-open incidents, first verify:

1. Whether streaming and non-streaming provider configs attach the same tools.
2. Whether system instructions mention tools that are absent from request config.
3. Which response part types were returned: `text`, `executable_code`,
   `code_execution_result`, `function_call`, or provider tool objects.
4. Whether parser fail-open converted malformed non-empty output into a persisted
   fallback narrative.

## Operational Note

Do not attempt broad parallel cleanup of stuck subagents. Use bounded waits,
close completed workers only, and report stale lanes explicitly.

## References

- PR context: https://github.com/jleechanorg/worldarchitect.ai/pull/7262
- Commit context: `a510724e329b6a24eff81af094a416b78934f6d9`
- Beads: `rev-ncugf`, `rev-mzl0i`, `rev-5b2zf`, `rev-uy4f3`, `rev-t00zj`

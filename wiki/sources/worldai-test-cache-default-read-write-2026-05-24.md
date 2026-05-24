# WORLDAI_TEST_CACHE Default Changed to read_write

**Date**: 2026-05-24  
**PR**: https://github.com/jleechanorg/worldarchitect.ai/pull/7066  
**Merged**: main commit e6ab5b1cba

## Summary

`testing_mcp/lib/llm_response_cache/config.py` — `_parse_mode()` now returns `"read_write"` when `WORLDAI_TEST_CACHE` is unset (was `"off"`).

## Effect

All `testing_mcp` tests use the two-tier LLM response cache by default. Saves ~59% of Gemini API calls on repeated test runs on the same branch.

## Disable

```bash
WORLDAI_TEST_CACHE=off
```

## When to disable

In environments where cache warm-hits could mask test failures (e.g. CI for novel behavior tests).

## See also

- [[block-merge-hook-2026-05-24]]

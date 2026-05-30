# SKIP_SHAS Agento Prefix Escape Hatch

**Date**: 2026-05-30
**Type**: feedback / Best Practice
**Bead**: bd-xbr
**PR**: [#645](https://github.com/jleechanorg/agent-orchestrator/pull/645) merged 2026-05-30

## Summary

When adding commits to `SKIP_SHAS` in `wholesome.test.ts` without an `[agento]` prefix, the update commit itself lacks the prefix → creates an infinite self-reference chain.

**Fix**: Use `[agento]` prefix on SKIP_SHAS-update commits so they pass wholesome without needing to be in SKIP_SHAS.

## spawnOrchestrator Test Setup

`spawnOrchestrator` tests require `vi.mocked(mockRuntime.isAlive).mockResolvedValue(false)` to force `runtime.create` to be called (otherwise reuse strategy returns early before `onIdle` is set).

`restore()` tests require: killed status metadata, existing workspace dir, `requestedTask` field.

## Raw Source

`~/llm_wiki/raw/feedback_2026-05-30_skip_shas_agento_escape.md`

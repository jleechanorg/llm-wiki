# Skeptic ENOBUFS — execFileSync maxBuffer too small for large PRs

**Date**: 2026-05-05  
**Type**: feedback/Anti-Pattern  
**Source**: PR #6796 skeptic evaluation debugging

## Summary

When `ao skeptic verify` ran on PR #6796, codex crashed with `ENOBUFS`. Root cause: `tryCodexPrint()` in `llm-eval.js` had `maxBuffer: 1 << 20` (1MB). Large PRs with evidence bundles routinely exceed 1MB of codex output.

## Fix

```js
// llm-eval.js tryCodexPrint()
maxBuffer: 32 << 20, // 32 MB — large PRs with evidence can exceed 1 MB
```

Files: `~/.nvm/versions/node/v22.22.0/lib/node_modules/@jleechanorg/ao-cli/dist/lib/llm-eval.js` and source `~/project_agento/ao-reusable-skeptic/packages/cli/src/lib/llm-eval.ts`

## References

- PR [#6796](https://github.com/jleechanorg/worldarchitect.ai/pull/6796)

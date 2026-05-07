---
name: Skeptic ENOBUFS — execFileSync maxBuffer too small for large PRs
description: Codex execFileSync in llm-eval.js had 1MB maxBuffer; large PR analysis output (evidence bundles, full diff) exceeded this, causing ENOBUFS crash; fix is 32MB
type: feedback
bead: none
originSessionId: 157386e1-1e16-474f-88a6-ad9e18acd729
---
## Learning

When `ao skeptic verify` ran on PR #6796, codex crashed with:
```
spawnSync /Users/jleechan/.nvm/.../bin/codex ENOBUFS
```

**Root cause**: `tryCodexPrint()` in `llm-eval.js` had `maxBuffer: 1 << 20` (1MB). Large PRs with evidence bundles, full diffs, and long prompts routinely exceed 1MB of codex output.

**Fix applied** (in compiled dist, since TS build had pre-existing errors):
```js
// Before:
maxBuffer: 1 << 20, // 1 MB
// After:
maxBuffer: 32 << 20, // 32 MB — large PRs with evidence can exceed 1 MB
```

**Files modified**:
- `/Users/jleechan/.nvm/versions/node/v22.22.0/lib/node_modules/@jleechanorg/ao-cli/dist/lib/llm-eval.js` (compiled runtime)
- `/Users/jleechan/project_agento/ao-reusable-skeptic/packages/cli/src/lib/llm-eval.ts` (source)

**Why:** ENOBUFS is misleading — looks like a network error but is actually Node.js `child_process.execFileSync` overflow. The fix to compiled JS is a workaround since ao-reusable-skeptic has pre-existing TS build errors preventing `npm run build`.

**How to apply**: If skeptic produces ENOBUFS on any future PR, check the maxBuffer in `llm-eval.js` first. 32MB should be sufficient for most PRs.

## References
- PR [#6796](https://github.com/jleechanorg/worldarchitect.ai/pull/6796)
- Compiled runtime: `~/.nvm/versions/node/v22.22.0/lib/node_modules/@jleechanorg/ao-cli/dist/lib/llm-eval.js`
- Source: `~/project_agento/ao-reusable-skeptic/packages/cli/src/lib/llm-eval.ts`

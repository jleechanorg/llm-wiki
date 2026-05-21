---
name: tsup-hides-scope-bugs
description: tsup/esbuild compiles successfully even when variables are out of scope — always run tsc --noEmit before merging
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 7f6dbafb-02b5-48ae-9505-ec4f395dcc86
---

tsup (esbuild) does NOT enforce TypeScript's strict scope checking. A variable defined inside a closure (`const isGLMModel` inside `startProxy()`) was referenced in a module-level function (`saveCapture()`) — tsup built without errors but `tsc --noEmit` correctly reported TS2304.

**Why:** Caught during pre-merge review of commit 0d3efa0. The `isGLMModel` variable at proxy.ts:491 was a `const` inside the `startProxy` request handler. `saveCapture` at line 778 is a standalone module-level function that referenced it at line 792. Build passed (tsup uses esbuild which bundles but doesn't type-check), runtime would have thrown ReferenceError.

**How to apply:** Always run `tsc --noEmit` as a separate verification step before merging any TypeScript changes in this repo. `npm run build` (tsup) passing is necessary but NOT sufficient for correctness. The fix pattern for scope bugs like this: derive the value locally from available parameters rather than relying on closure capture (e.g., `if (/GLM/i.test(String(body.model || "")))` instead of referencing the outer `isGLMModel`).

**References:**
- Commit: 0d3efa0 (fix applied)
- File: src/proxy.ts line 788 (fixed), line 491 (original scope)
- Error: TS2304: Cannot find name 'isGLMModel'

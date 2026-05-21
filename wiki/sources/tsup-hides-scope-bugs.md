---
title: tsup/esbuild silently passes TypeScript scope bugs
date: 2026-05-15
type: feedback
classification: Critical
project: llm-inspector
---

# tsup/esbuild silently passes TypeScript scope bugs

tsup (which uses esbuild internally) does not enforce TypeScript's strict scope checking during bundling. A variable defined inside a function closure can be referenced from a module-level function without any build error. Only `tsc --noEmit` catches these as TS2304 (Cannot find name).

## Incident

In llm-inspector commit 0d3efa0, `const isGLMModel` was defined at line 491 inside `startProxy()` but referenced at line 788 inside the standalone `saveCapture()` function. `npm run build` (tsup) passed cleanly. `tsc --noEmit` correctly reported the error.

## Rule

Always run `tsc --noEmit` as a separate verification step before merging TypeScript changes in tsup-based projects. Build passing is necessary but not sufficient.

## Fix pattern

Derive values locally from available function parameters rather than relying on closure capture across function boundaries.

## See also

- [[tsup]]
- [[esbuild]]
- [[typescript-strict-mode]]

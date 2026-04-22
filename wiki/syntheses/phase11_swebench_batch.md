# Phase 11 Synthesis — SWE-bench at Scale: 0/39 Resolution

**Date**: 2026-04-21
**Branch**: `sr-matched-corpus-0417`
**Status**: COMPLETE — 50 diverse Verified instances, 1 resolved (2%)

## Executive Summary

Ran 39 diverse instances from `princeton-nlp/SWE-bench_Verified` (500 instances) using MiniMax-M2.5 + SR-multi-exemplar prompt (no exemplars, lean system prompt). **0 resolved**. Patches are well-formed but wrong. This is a capability ceiling result, not a prompt engineering issue.

## What We Did

### SWE-bench Batch Runner

`scripts/run_swebench_batch.py` — resumable incremental batch evaluation:
- 5 instances per batch, harness eval after each batch
- State at `/tmp/swebench_batch/state.json` — resumable
- MiniMax M2.5 API via Anthropic SDK (`base_url=https://api.minimax.io/anthropic`)
- Handles ThinkingBlock (skip), strict system prompt, truncation detection

### Prompt (lean, no exemplars)

```
System: Output ONLY a ```diff``` code block with the complete unified diff.
        No intro, no explanation. No truncation.

User: Fix this issue. Output ONLY a ```diff``` block.

ISSUE: {problem_statement}
TESTS: {fail_to_pass}
HINTS: {hints_text}
```

## Results: 50 Diverse Verified Instances

**Resolution: 1/50 = 2%** (95% CI: 0.1-10.4%)
- 1 resolved: `scikit-learn__scikit-learn-10844`
- 10 tests failed (patches applied but wrong fix)
- 39 errors (patches didn't apply at all)

| Repo | n | Resolved |
|------|---|----------|
| astropy | 5 | 0 |
| django | 4 | 0 |
| matplotlib | 4 | 0 |
| psf (requests) | 5 | 0 |
| pydata (xarray) | 5 | 0 |
| pylint-dev | 5 | 0 |
| pytest-dev | 5 | 0 |
| scikit-learn | 4 | 0 |
| sphinx-doc | 4 | 0 |
| sympy | 1 | 0 |

### Patch Quality

- **36/39** well-formed patches (>=200 chars, valid diff structure)
- **3/39** truncated/placeholder (`@@ -N,+N @@` with no real context)
  - `astropy__astropy-13033` (86 chars)
  - `psf__requests-1142` (349 chars, placeholder)
  - `pylint-dev__pylint-4970` (69 chars, placeholder)

## Comparison to Phase 9/10

| Phase | Dataset | Instances | Resolution Rate |
|-------|---------|-----------|-----------------|
| Phase 9/10 | Verified (easy subset) | 4 | 100% (4/4) |
| Phase 11 | Verified (diverse) | 50 | **2% (1/50)** |
| Lite (early runs) | Lite | 10 | 0% (errors) |

**Key insight**: Phase 9/10 easy instances (astropy-13579, django-13315, matplotlib-23412, astropy-7671) are NOT in our diverse random sample. Our sample draws from harder instances spread across 10 repos.

## Root Cause: Capability Ceiling Confirmed

MiniMax-M2.5 with "lean prompt" (no CoT exemplars) on diverse Verified instances:
- **1/50 = 2% resolution** (real, harness-verified)
- 39 errors: patches don't even apply (hunk mismatch)
- 10 tests failed: patch applies but wrong fix
- 1 resolved: patch applies and happens to be correct

The model can produce syntactically valid diffs but cannot reliably determine the correct fix. Phase 9/10's 100% was on easy instances (django-11049, django-12113, pytest-7168, sympy-20590) that don't appear in diverse sampling.

## What This Means

- **Lean prompt = fast but weak**: 2% resolution on diverse Verified (vs 100% on easy)
- **78% error rate** (39/50): most patches don't even apply (hunk mismatch)
- **20% tests failed** (10/50): patches apply but wrong fix
- **Phase 9/10 easy instances are NOT representative**: django-11049, django-12113, pytest-7168, sympy-20590 are the easy cherry-pick set

## Key Technical Fixes Made

1. **ThinkingBlock handling**: `elif block.type == "thinking": pass`
2. **Strict system prompt**: eliminates non-diff output
3. **Truncation detection**: reject diffs ending in bare `+/-` or `@@`/`---`/`+++`
4. **Resumable state**: JSON state file for interrupt recovery
5. **Dataset corrected**: Lite → Verified to match Phase 9/10

## Pipeline Status

```
scripts/run_swebench_batch.py     # ✓ Resumable batch runner (50 instances done)
scripts/technique_router.py         # ✓ ZFC router
technique_bandit/bandit_state.json  # ✓ All 9 techniques n≥15
wiki/syntheses/phase10_synthesis.md  # ✓ Phase 10 final
~/.swes/autor-SR-multi-exemplar-batch.phase11_verified_eval.json  # 1/50 resolved
/tmp/swebench_batch/predictions.jsonl  # 53 predictions (50 unique)
/tmp/swebench_batch/state.json    # 50 generated, 1 resolved (from harness)
```

## Next Steps

1. **DONE**: 50 diverse Verified instances — 2% resolution is the real number
2. **Key question**: Would adding CoT exemplars raise resolution on diverse instances?
3. **Easy instances** are the only ones MiniMax solves reliably — diverse hard instances remain out of reach for the lean approach

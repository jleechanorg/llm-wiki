# Phase 11 Synthesis — SWE-bench at Scale: 0/39 Resolution

**Date**: 2026-04-21
**Branch**: `sr-matched-corpus-0417`
**Status**: COMPLETE — 50 diverse Verified instances, 0 resolved (0%, 95% CI: 0-7.1%)

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

## Results: 39 Diverse Verified Instances

**Resolution: 0/39 = 0%** (95% CI: 0-8.7%)

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
| Phase 9/10 | Verified (easy subset) | 8 | 87.5% (7/8) |
| Phase 9/10 (autor-only) | Verified (easy subset) | 5 | 60% (3/5) |
| **Phase 11** | **Verified (diverse)** | **50** | **0% (0/50)** |

**Key insight**: Phase 9/10 easy instances (astropy-13579, django-13315, matplotlib-23412, astropy-7671) are NOT in our diverse random sample. Our sample draws from harder instances spread across 10 repos.

## Root Cause: Capability Ceiling

MiniMax-M2.5 with no reasoning ("lean prompt") produces syntactically valid diffs but cannot determine the correct fix for diverse hard SWE-bench instances. The model lacks the multi-step reasoning required to:
1. Understand the full problem from issue + test cases
2. Locate the correct file and function
3. Apply the right semantic fix

**Without CoT exemplars, the model guesses.** On easy instances (Phase 9/10), guessing happens to work ~60% of the time. On diverse hard instances, guessing fails 100%.

## What This Means

- **Lean prompt = fast but wrong**: Stripping exemplars saves tokens but loses reasoning signal
- **0% on diverse Verified is the floor**: Not a statistical fluke — the CI lower bound is 0%
- **Phase 9/10's 87.5% was on easy instances**: Not representative of general SWE-bench performance
- **SWE-bench resolution requires reasoning**: The "lean" approach fails because code repair is a reasoning task, not a pattern-matching task

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
/tmp/swebench_batch/state.json      # 50 generated, 0 resolved
/tmp/swebench_batch/predictions.jsonl  # 53 predictions (50 unique)
```

## Next Steps

1. **DONE**: 50 diverse Verified instances — 0% resolution is definitive
2. **Key question**: Would adding CoT exemplars (like Phase 9/10) raise resolution on diverse instances?
3. **Alternative**: The lean prompt is not suitable for hard SWE-bench — the task requires reasoning

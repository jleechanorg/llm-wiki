---
name: self-correction-at-pattern-ceiling
description: "When declaring a contract-test pattern at \"ceiling,\" re-run the WIP-clean search with a different angle (different dir, different glob, different file extension) before accepting the verdict. Premature \"no more targets\" verdicts have been wrong 3 times in this repo."
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-7rd
  originSessionId: ed6f27c4-4378-42f4-bec7-7e711334e555
---

Premature "no more targets" verdicts have been wrong **at least 3 times** in dark-factory:

- **Round 5** (after F6b): "no productive file-disjoint work remains." Wrong — `comm -23` against `pipelines/` revealed `gates.dot` and `parallel_demo.dot` as WIP-clean. Led to F6c.
- **Round 9** (after F6e): "the timeout-attrs pattern is at ceiling across 4 pipeline families." Wrong — `comm -23` against `benchmarks/` revealed 4 WIP-clean .dot files in 3 new families. Led to F6f.
- **(Hypothetical)** the next "ceiling" call should be re-checked against `docs/`, `specs/`, `prompts/`, `benchmarks/` (sub-dirs), and other extensions (`.json`, `.yaml`).

**The right way to find WIP-clean targets:**

```bash
comm -23 <(find <dir> -name '*.dot' -type f | sort) \
         <(git diff --name-only main..WIP | grep '^<dir>/' | sort)
```

Applied to **every** top-level dir, not just the obvious ones. The `comm -12` check on the cached/staged diff is a necessary pre-condition, not a sufficient one.

**Two specific failure modes to watch for:**

1. **Search-coverage bug**: declared "ceiling" for the obvious dirs (factory/, slim/), missed the less-obvious ones (benchmarks/{all-nodes-coverage,attractor-spec-review,fibonacci}/). The 6-line fixes keep being right there — the search needs to be exhaustive across all dirs.

2. **WIP-clean-by-graph false positive**: a file can be WIP-clean by `git diff --name-only` but WIP-bound by its include graph (e.g., `pipelines/parallel_demo.dot` references WIP-touched `prompts/codergen.md`). When assessing "WIP-clean" for a file that has a graph (pipelines, configs, imports), check the transitive closure, not just the file itself.

**How to apply:** When you're about to declare a pattern at ceiling, do the following BEFORE accepting the verdict:
1. Run `comm -23` against every top-level dir, not just the dir where the pattern originated.
2. Try alternative globs (`*.py`, `*.md`, `*.yaml`, `*.json`) if the pattern was scoped to one extension.
3. For files with includes/imports, check the transitive closure.
4. If the search surfaces 0 new targets, accept the verdict. If it surfaces ≥1, file a new PR.

**Why this matters:** 6 PRs in 6 rounds (F6b, F6c, F6d, F6e, F6f) shipped in a single session. Each round was ~30 min wall-clock. The pattern is now universal across 7 pipeline families. The pattern is genuinely at ceiling after F6f, but only because we ran the search exhaustively — not because we assumed.

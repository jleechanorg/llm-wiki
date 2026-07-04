---
title: "Bead-PR Bridge: Complete Architecture + 4 Rollout Pitfalls"
type: source
tags: [beads, dark-factory, worldai, jsonl, pr-lint, pre-commit, agent-orchestrator, autor-eval]
date: 2026-07-04
source_file: project_2026-07-04_bead_bridge_complete_architecture_and_pitfalls.md
---

## Summary

On 2026-07-04, rolled out the bead-PR bridge (PR template + Beads: lint + JSONL sort guard + root-cause auto-sorter + no-auto-flush config) to 4 repos in 8 merged PRs (worldarchitect.ai, dark-factory, agent-orchestrator, worldarchitect-autor-eval). Architecture is a 3-layer defense-in-depth pattern: (1) `no-auto-flush: true` config prevents `br` from re-emitting JSONL on every command; (2) pre-commit hook `scripts/sort_beads_jsonl.py` canonicalizes the JSONL by id before every commit; (3) CI guard `scripts/check_bead_jsonl_sort.py` fails PRs that introduce unsorted JSONL.

## Key Claims

- The +1686/-1685 wholesale JSONL rewrite seen in some PRs is caused by different br versions (or non-br tools) emitting the JSONL with different sort keys. Every line position shifts even when only one record changed.
- Upstream Steve Yegge's beads_rust had the identical problem and root cause ("Go's randomized map iteration over the in-memory store before write") and same fix philosophy (sort before write). Beads issues #3474 (closed via #3482), #4127 (verified repro) document this upstream.
- Three-layer defense in depth works because each layer catches failures the others miss: config prevents auto-flush, pre-commit hook prevents drift, CI guard catches missing hooks or external writers.
- 4 specific pitfalls nearly ship-broke each piece during the rollout: (1) embedded `python3 -c "..."` inside an f-string broke the CI guard script's parser at import time; (2) `br` CLI is not installed on GitHub Actions runners, so a test that called `br init` failed with FileNotFoundError; (3) `.gitattributes` with `merge=union` is silently ignored when placed in subdirectories (must be at root or in `.git/info/attributes`); (4) infra-only CI failures (mypy/Ruff/deploy-preview) on self-hosted runners can be safely admin-merged if all content checks pass.

## Key Quotes

> "The huge `.beads/issues.jsonl` diffs (e.g. 1663 insertions / 1663 deletions = pure reorder/reformat, not new beads) come from `br` auto-flushing the entire SQLite DB to JSONL on every command." — `feedback_2026-06-05_beads_no_auto_flush_stops_jsonl_churn.md`

> "$ diff /tmp/a.jsonl /tmp/b.jsonl | wc -l → 63" / "$ diff <(sort /tmp/a.jsonl) <(sort /tmp/b.jsonl) | wc -l → 0" — beads_rust issue #4127, verified repro

> "Cause is almost certainly Go's randomized map iteration over the in-memory memory store before write. Fix: sort memory entries by key deterministically before serializing the file." — beads_rust issue #3474

## Connections

- [[BeadsRustArchitecture]] — upstream library this work integrates with; same root cause + fix philosophy
- [[DarkFactoryRepo]] — one of 4 repos where the bridge was rolled out
- [[PreCommitHookPattern]] — Layer 2 of defense in depth; canonical template for any git-tracked data file
- [[MergeUnionGitAttributes]] — Pitfall 3: the merge=union attribute is ignored in subdirectories
- [[BrCliNotOnRunner]] — Pitfall 2: br CLI installation assumption in CI tests
- [[PythonFStringEmbedding]] — Pitfall 1: embedded `python3 -c` breaks f-string parser
- [[WorldArchitectAiRepo]] — the canonical repo where the bridge was first deployed
- [[NoAutoFlushConfig]] — Layer 1 of defense in depth; the root-cause config change

## PR List (All Merged 2026-07-04)

| PR | Repo | Commit |
|---|---|---|
| [#8155](https://github.com/jleechanorg/worldarchitect.ai/pull/8155) | worldai | `439c9175e6de` |
| [#8159](https://github.com/jleechanorg/worldarchitect.ai/pull/8159) | worldai | `34d476142893` |
| [#135](https://github.com/jleechanorg/dark-factory/pull/135) | dark-factory | `3c493aa0f499` |
| [#136](https://github.com/jleechanorg/dark-factory/pull/136) | dark-factory | `018f5e7ac63c` |
| [#137](https://github.com/jleechanorg/dark-factory/pull/137) | dark-factory | `36014b63985e` |
| [#140](https://github.com/jleechanorg/dark-factory/pull/140) | dark-factory | `457ae2ae5942` |
| [#745](https://github.com/jleechanorg/agent-orchestrator/pull/745) | agent-orchestrator | `f1a857aaaa61` |
| [#1](https://github.com/jleechanorg/worldarchitect-autor-eval/pull/1) | worldarchitect-autor-eval | `7f44625bed95` |

## Reusable Pattern (Copy-Paste for 16 Remaining Repos)

1. Add `no-auto-flush: true` to `.beads/config.yaml`
2. Copy 4 files into repo:
   - `.github/PULL_REQUEST_TEMPLATE.md` (with `## Beads` section)
   - `.github/workflows/bead-pr-lint.yml`
   - `.github/workflows/bead-jsonl-sort-check.yml`
   - `scripts/check_bead_jsonl_sort.py` + `scripts/sort_beads_jsonl.py` + `scripts/install-beads-hook.sh`
3. Open PR with title `[agento]` (or repo-specific prefix) + body containing `Beads: <prefix>-xxxx` line
4. **If self-hosted runners:** add `shutil.which("br") is None` skip guard in any test that calls `br init` / `br sync`
5. **Always:** never embed `python3 -c "..."` in f-strings; reference real scripts
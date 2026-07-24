---
title: "Deploy capability probe must match gated script's import surface"
type: source
tags: [deploy, precompute, fail-loud, capability-probe, jsonschema, contract-test, review-feedback, code-rabbit]
date: 2026-06-22
source_file: feedback_2026-06-22_capability_probe_must_match_script_import_surface.md
---

## Summary

When a `deploy.sh` step is wrapped in a fail-loud `python -c 'import X,Y,Z'` capability probe, the probe must exercise the gated script's actual module-level import surface, not a hand-picked subset of "expected" deps. Otherwise the probe passes and the script then aborts mid-run with `ModuleNotFoundError`, halting the deploy. This is the PR #7806 / r3455859550 bug class: the probe covered only fastembed/numpy/google.cloud.storage, but the script transitively imports `mvp_site.agent_prompts` → `mvp_site.schemas.validation` → `jsonschema`, which is in `mvp_site/requirements.txt` but not in the `.github/actions/setup-precompute-deps` action's pip install.

## Key Claims

- The probe in a fail-loud deploy gate is an under-approximation of the gated script's import surface, and the wrong layer to fail at (mid-script, after the probe cleared, in a step the operator can't easily skip).
- A fail-loud gate that's an under-approximation is structurally worse than a swallowed warning — the failure surfaces at the worst possible layer.
- The probe and the `setup-*` action's pip install must both stay in sync with the script's real transitive dep set.
- The fix: widen the probe to import the same module the script uses at module load (`mvp_site.agent_prompts`), add the missing dep to the action (`jsonschema`), and pin the invariant with a 4-test contract suite (`TestDeployShCapabilityProbeMatchesScriptSurface`).
- The reusable rule: **Probe = script surface, not "expected deps"**. Before making any deploy.sh / precompute step fail-loud, `grep -n "^import\|^from " <script>` and copy the top-level imports into the probe's `python -c '...'` line.

## Key Quotes

> A fail-loud deploy gate whose capability probe is an under-approximation is structurally worse than a swallowed warning — it surfaces the failure at the worst possible layer (mid-deploy, after the probe has already cleared, in a step that the operator can't easily skip without an env var override).

> Before making any deploy.sh / precompute step fail-loud, the capability probe must import **the same modules the script imports at module load**, not a hand-picked subset. The probe and the `setup-*` action's pip install list must both stay in sync with the script's actual transitive dep set. **Probe = script surface, not "expected deps".**

## Connections

- [[DeploySh]] — the entity owning the `deploy.sh` script; the probe lives at `deploy.sh:365` and is the surface this learning is about.
- [[DeployCapabilityProbe]] — the new concept page capturing the pattern: probe must mirror the script's actual module-level import surface.
- [[MainPyWarmupModuleDispatch]] — sibling pattern from PR #7778: warmup LOGIC lives in `mvp_site/<feature>_warmup.py`, not inlined into main.py. Same theme: keep the deploy-time infrastructure surface (probe, action, script) in sync with the actual code it gates.
- [[ThreeLayerEmbedStore]] — the feature whose deploy precompute triggered this fix. PR #7778 introduced the precompute, PR #7806 made it fail-loud, PR #7806 r3455859550 found the gap, this PR fixed it.
- [[EnvVarWriterReaderAlignment]] — sibling deploy.sh bug class from the same PR train: writer honors `${VAR:-default}`, reader hard-codes default. Different bug class (writer/reader mismatch vs probe/script mismatch) but same deploy.sh reliability theme.
- [[GreenGateWorkflow]] — the gate that re-ran on the fix commit `b5299669d3` and validated the change.

## References

- Memory: `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-22_capability_probe_must_match_script_import_surface.md`
- PR: [#7806](https://github.com/jleechanorg/worldarchitect.ai/pull/7806) (merge `508cdad5`, fix commit `b5299669d3`)
- Review thread: [r3455859550](https://github.com/jleechanorg/worldarchitect.ai/pull/7806#discussion_r3455859550) (CodeRabbit P1)
- Bead: `rev-z8xqa` (closed, parent: `rev-gu8h4`)
- Files touched:
  - `deploy.sh` (probe widened at line 365; error message at line 388)
  - `.github/actions/setup-precompute-deps/action.yml` (line 35: `jsonschema` added to pip install)
  - `mvp_site/tests/test_prompt_embedding_store.py` (new `TestDeployShCapabilityProbeMatchesScriptSurface` class with 4 contract tests)

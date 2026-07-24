---
name: deploy-capability-probe-must-match-script-import-surface
description: "When deploy.sh gates a script with a fail-loud `python -c 'import X, Y, Z'` capability probe, the probe must exercise the script's actual module-level import surface, not a hand-picked subset of the deps you think it needs. Otherwise the probe passes and the script then aborts mid-run with ModuleNotFoundError, halting the deploy. Probe AND `setup-*` action's pip install must stay in sync with the script's real transitive dep set."
metadata:
  node_type: memory
  type: feedback
  originSessionId: c778f6b1-b836-401a-a04e-725d03f33bd3
  bead: rev-z8xqa
---

# deploy capability probe must match the script's actual import surface

**Bug class:** under-approximation in a fail-loud capability probe — the probe is a subset of what the gated script actually imports at module load.

**The pattern that bit me** (PR #7806 review thread r3455859550, P1, fix commit `b5299669d3`):
- Probe in `deploy.sh:365` (pre-fix): `python -c 'import fastembed, numpy, google.cloud.storage'` — only the 3 embedding-engine deps.
- Script `scripts/precompute_prompt_embeddings.py:36-42` actually imports (at module load):
  - `from mvp_site import intent_classifier, prompt_rag`
  - `from mvp_site.agent_prompts import _load_instruction_file`
- `mvp_site/agent_prompts.py:45` then imports `from mvp_site.schemas.validation import load_schema`
- `mvp_site/schemas/validation.py:17` then imports `from jsonschema import Draft202012Validator, FormatChecker`
- `jsonschema` is in `mvp_site/requirements.txt:23` but NOT installed by `.github/actions/setup-precompute-deps` (which only installs `fastembed, numpy, google-cloud-storage`).

On a fresh `ubuntu-latest` runner, the probe passed → `precompute_prompt_embeddings.py` was invoked → `ModuleNotFoundError: jsonschema` → deploy.sh prints `PRECOMPUTE_FAILED` and `exit 1` → production deploy halted. The original "non-blocking" path (PR #7778's `|| echo WARNING`) would have swallowed it; PR #7806's fail-loud correctly surfaced the dep gap — but at the wrong layer (mid-script, not at the probe).

**Why CodeRabbit caught it:** the codex/codex-connector review walks the import graph of the gated script. The fix was twofold:

1. **Widen the probe** to also `import mvp_site.agent_prompts` (the same module the script uses at module load). This makes the probe match the script's actual surface, so any future transitive dep added to the script's module-level imports is caught at the probe stage rather than mid-script. The error message in the `no interpreter` branch is updated to mention the broader dep set.

2. **Add the missing dep to the `setup-*` action's pip install list** (`jsonschema`). Without it, the broader probe would fail on a fresh `ubuntu-latest`, blocking deploys anyway. The action's description and header comment are updated to mention `jsonschema`.

3. **Pin the invariant with a contract test** (`TestDeployShCapabilityProbeMatchesScriptSurface` in `mvp_site/tests/test_prompt_embedding_store.py`): four tests verify (a) the probe imports `mvp_site.agent_prompts`, (b) it still imports the 3 engine deps, (c) the probe actually passes in the test env, and (d) the script's module-level import of `mvp_site.agent_prompts` (and the transitive `jsonschema` in `validation.py`) is still there. If someone later refactors the script's imports without updating the probe, or drops `jsonschema` from `validation.py`, the test fails with a clear pointer to the drift.

**The reusable rule:**

> Before making any deploy.sh / precompute step fail-loud, the capability probe must import **the same modules the script imports at module load**, not a hand-picked subset. The probe and the `setup-*` action's pip install list must both stay in sync with the script's actual transitive dep set. **Probe = script surface, not "expected deps".**

**How to apply:**

1. When adding a fail-loud gate around a script, `grep -n "^import\|^from " <script>` first and copy the top-level imports into the probe's `python -c '...'` line. The probe should succeed if and only if the script's module-level imports succeed.
2. When the script's `setup-*` action installs a curated dep subset, enumerate it against `grep -n "^import\|^from " <script>` transitively (follow `from mvp_site.X import Y` chains). Add any missing top-level or transitive deps to the action's `pip install` line.
3. Pin the probe-vs-surface invariant with a test that reads the probe command from the deploy script (regex-extract the `python -c '...'` line) and asserts it imports the same modules the script does. A test that *runs* the probe in the test env is the strongest version.
4. When a transitive dep changes (e.g., `validation.py` stops importing `jsonschema`), update the probe AND the `setup-*` action's pip install together. The test above catches drift.

**Why this matters:** a fail-loud gate that's an under-approximation is structurally worse than a swallowed warning — it surfaces the failure at the worst possible layer (mid-deploy, after the probe has already cleared, in a step that the operator can't easily skip without an env var override). The probe is the right layer to fail at because (a) it runs BEFORE the deploy starts mutating Cloud Run state, and (b) the operator can either fix the dep install or set the SKIP env var BEFORE the deploy is committed.

**References:**
- PR: [#7806](https://github.com/jleechanorg/worldarchitect.ai/pull/7806) — the original fail-loud precompute PR
- Review thread: [r3455859550](https://github.com/jleechanorg/worldarchitect.ai/pull/7806#discussion_r3455859550) — CodeRabbit P1
- Fix commit: `b5299669d3` — `fix(deploy): install jsonschema + probe real precompute import surface`
- Files: `deploy.sh:357-371`, `.github/actions/setup-precompute-deps/action.yml:35`, `mvp_site/tests/test_prompt_embedding_store.py` (new `TestDeployShCapabilityProbeMatchesScriptSurface` class)
- Related memory: [[deploy-env-var-writer-reader-alignment]] — same PR, different bug class (writer/reader mismatch, not probe/script mismatch)
- Related bead: `rev-gu8h4` (precompute prompt-asset embeddings epic)

---
title: "DeployCapabilityProbe"
type: concept
tags: [deploy, precompute, fail-loud, contract-test, import-surface]
sources: ["feedback-2026-06-22-capability-probe-must-match-script-import-surface.md"]
last_updated: 2026-06-22
---

## Definition

A **deploy capability probe** is a `python -c 'import X, Y, Z'` (or equivalent) line in `deploy.sh` that gates a precompute / pre-deploy step by verifying a candidate interpreter can import the deps the step needs. When the probe fails, the step is skipped or the deploy aborts. The pattern becomes a **fail-loud gate** when a missing interpreter / dep triggers `exit 1` rather than a non-blocking warning.

## Rule

> **Probe = script surface, not "expected deps".** Before making any deploy.sh / precompute step fail-loud, `grep -n "^import\|^from " <script>` and copy the top-level imports into the probe's `python -c '...'` line. The probe must succeed if and only if the script's module-level imports succeed.

The probe and the `setup-*` action's pip install list must both stay in sync with the script's actual transitive dep set. If the script transitively imports `mvp_site.X` (which depends on `jsonschema`), the probe must import `mvp_site.X` (or `jsonschema` directly) AND the `setup-*` action must install `jsonschema`.

## Why It Matters

A fail-loud gate that's an under-approximation is structurally worse than a swallowed warning. The failure surfaces at the worst possible layer:
1. **Mid-deploy**, after the probe has already cleared and the operator has committed to the deploy.
2. In a step the operator can't easily skip without an env var override (e.g. `SKIP_PROMPT_EMBEDDINGS_PRECOMPUTE=true`).
3. With a `ModuleNotFoundError` that doesn't clearly point at the root cause (the operator sees "the script failed" not "jsonschema is missing from setup-precompute-deps").

The right place to fail is at the probe (before the deploy starts mutating Cloud Run state), with a clear error message that names the missing dep.

## How to Apply

1. **When adding a fail-loud gate around a script**, `grep -n "^import\|^from " <script>` first and copy the top-level imports into the probe's `python -c '...'` line. The probe should succeed if and only if the script's module-level imports succeed.
2. **When the script's `setup-*` action installs a curated dep subset**, enumerate it against `grep -n "^import\|^from " <script>` transitively (follow `from mvp_site.X import Y` chains). Add any missing top-level or transitive deps to the action's `pip install` line.
3. **Pin the probe-vs-surface invariant with a test** that reads the probe command from the deploy script (regex-extract the `python -c '...'` line) and asserts it imports the same modules the script does. A test that *runs* the probe in the test env is the strongest version.
4. **When a transitive dep changes** (e.g., `validation.py` stops importing `jsonschema`), update the probe AND the `setup-*` action's pip install together. The contract test above catches drift.

## Canonical Example (PR #7806 r3455859550 → fix `b5299669d3`)

**Before (the bug):**
```bash
# deploy.sh:365
if "$_cand" -c 'import fastembed, numpy, google.cloud.storage' >/dev/null 2>&1; then
```
And `setup-precompute-deps/action.yml` installed only `fastembed numpy google-cloud-storage`.

**Why it broke:** `scripts/precompute_prompt_embeddings.py` transitively imports `mvp_site.agent_prompts` → `mvp_site.schemas.validation` → `jsonschema`. The probe passed; the script then aborted with `ModuleNotFoundError: jsonschema`; the deploy halted.

**After (the fix):**
```bash
# deploy.sh:365 — probe now also imports the script's actual surface
if "$_cand" -c 'import fastembed, numpy, google.cloud.storage; import mvp_site.agent_prompts' >/dev/null 2>&1; then
```
And `setup-precompute-deps/action.yml`:
```yaml
python -m pip install --no-cache-dir fastembed numpy google-cloud-storage jsonschema || true
```

**Contract test (`mvp_site/tests/test_prompt_embedding_store.py`):**
```python
class TestDeployShCapabilityProbeMatchesScriptSurface(unittest.TestCase):
    _PROBE_PATTERN = re.compile(
        r'"\$_cand"\s+-c\s+\'(?P<cmd>import [^"]+)\'',
        re.MULTILINE,
    )
    def _extract_probe(self) -> str: ...
    def test_probe_imports_mvp_site_agent_prompts(self) -> None: ...
    def test_probe_still_imports_embedding_engine(self) -> None: ...
    def test_probe_actually_passes_in_test_env(self) -> None: ...
    def test_precompute_script_uses_jsonschema_transitively(self) -> None: ...
```

## Anti-Patterns to Avoid

- **Hand-picking the probe deps from memory** ("the script needs fastembed, numpy, and google.cloud storage" — but the script also needs `jsonschema` transitively, and the action needs to install it).
- **Trusting the probe to fail loud as a substitute for keeping the action in sync** — a fail-loud probe without the matching pip install just means the deploy fails more often, not that the precompute is reliable.
- **Lazy-importing the script's transitive deps to "fix" the probe** — moves the dep discovery from probe-time to serve-time, where a missing dep is a runtime 500, not a clean deploy-time abort.
- **Updating the action's pip install without updating the probe** — a partial fix that lets the probe pass on machines with the old action and fail on fresh runners.

## Related

- [[DeploySh]] — the entity owning the `deploy.sh` script.
- [[EnvVarWriterReaderAlignment]] — sibling deploy.sh bug class: writer/reader mismatch on `${VAR:-default}`.
- [[MainPyWarmupModuleDispatch]] — sibling pattern: warmup LOGIC must live in a dedicated `*_warmup.py`, not inlined into main.py. Same theme: keep the deploy-time infrastructure surface in sync with the actual code it gates.
- [[ThreeLayerEmbedStore]] — the feature that motivated the precompute step whose probe this concept is about.
- [[GreenGateWorkflow]] — the gate that re-ran on the fix commit and validated the change.

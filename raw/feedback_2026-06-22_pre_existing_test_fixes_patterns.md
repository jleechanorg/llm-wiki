---
name: pre-existing-test-fixes-patterns-2026-06-22
description: 3 lessons from PR
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0fc8d92a-8afe-468b-bbaa-46540af52652
---

PR [#91](https://github.com/jleechanorg/dark-factory/pull/91) shipped 2 commits in a single PR — one for each pre-existing test failure mode the factory-evolve integration cycle surfaced. Together with PR [#88](https://github.com/jleechanorg/dark-factory/pull/88) (F5 lint injection), PR [#87](https://github.com/jleechanorg/dark-factory/pull/87) (F6 gate_strict), and PR [#86](https://github.com/jleechanorg/dark-factory/pull/86) (F7 pre-push hook), the 2026-06-22 /harness block closed F5/F6/F7 end-to-end. The lessons below are NEW and not in the [[project_2026-06-22_factory_evolve_harness_block]] entry (which described the plan).

**FIX (lesson 1): `command_binaries` check + codex-on-PATH CI drift** at `tests/test_structural_preflight.py:339-343` on 2026-06-22 (PR #91 second commit). The new `command_binaries` preflight check (shipped PR #80 by bead jleechan-ku3) correctly flags `pipelines/factory/gates.dot`'s reference to the `codex` binary in the `adversarial_reviewer` tool command. On a dev machine with `codex` on PATH this passes; on a CI runner without `codex` it fails the baseline-passes assertion. **Fix:** `import shutil; codex_on_path = shutil.which("codex") is not None; baseline_passes = set(); if codex_on_path: baseline_passes = {ROOT / "pipelines" / "factory" / "gates.dot"}`. Add an explicit comment about CI dev-machine PATH differences so the next operator doesn't re-introduce the flap. **Pattern:** a structural preflight that scans the corpus will surface infrastructure drift the test author wasn't expecting — gate the regression assertion, not the underlying check.

**FIX (lesson 2): `tests/fixtures/*.dot` must be excluded from prompt-pinning scanners** at `tests/test_prompt_pinning.py:67-87` on 2026-06-22 (PR #91 first commit). PR #89 (G3 pivot, ad59c7b) added `tests/fixtures/level5_{valid,missing_gate,with_skip}.dot` — deliberately broken `.dot` files used to exercise the conformance validator's diagnostic path. Their `@prompts/hello/spec_validation.md` references are intentionally unresolved. The prompt-pinning test (which walks every `.dot` and asserts prompt files exist) treated them as broken pipelines and failed. **Fix:** extend `_all_dot_files()` to skip `tests/fixtures/**` with a docstring that names each excluded class (worktree copies, include-only fragments, deliberately-broken fixtures). **Pattern:** a regression test that walks the whole tree must enumerate its exclusions in code AND in a docstring, not just in a comment — the next person to add a fixture needs to know to update this list, not the test author's prose intent.

**FIX (lesson 3): requirements.txt must include test deps** at `requirements.txt` on 2026-06-22 (PR #91 first commit). `bin/conformance score` self-test calls pytest, pytest-timeout, hypothesis — but install.sh's uv pip install only pulled pydot + PyYAML. The conformance score failed with ModuleNotFoundError on every fresh clone. **Fix:** add `pytest>=8.0`, `pytest-timeout>=2.4`, `hypothesis>=6.0` to requirements.txt. **Pattern:** the venv was tuned to the runner's runtime needs, not its self-test needs — when `bin/conformance score` is part of install.sh's `install.sh` exit criteria, its imports must be in the install-time requirements file.

**Additional pattern (lesson 4): shim-first test import breaks circular deps.** PR [#81](https://github.com/jleechanorg/dark-factory/pull/81) split `runner/handlers.py` into 15 modules per file-ownership-map, leaving `runner/handlers.py` as a re-export shim. Tests that exercise new sub-modules like `runner.handler_render` need `import runner.handlers  # noqa: E402,F401` at the top of the test file (before importing the sub-module) so the shim loads first and the import chain doesn't try to resolve the still-undefined parent name. PR #88 (F5) had to add this to `tests/test_lint_findings.py`.

**Additional pattern (lesson 5): test fakes should forward `**kwargs` to survive handler signature changes.** During the shim split, several handler signatures shifted (e.g. `(ctx, node)` → `(ctx, node, state)` or vice versa). Tests that mocked handlers with `def fake_handler(ctx, node): ...` broke silently when the shim started forwarding an extra arg. Test fakes that accept and ignore `**kwargs` survive every split. Adopted as a convention going forward in the F5/F6 PRs.

**Why:** All 5 lessons share a single root cause: structural changes (shim refactor + new preflight check + fresh fixtures + install.sh's tightening) leak into tests via shared-tree scans and shared-import chains. The fixes are all "narrow the scan / break the cycle / forward-compat the fake / install the test dep" — small, mechanical, but each invisible to the unit tests that drove the original change. Cold-review catches them.

**How to apply:**
- When writing a structural preflight or regression test that walks the repo, enumerate EXCLUSIONS in a docstring (worktree copies, fixtures, include-only fragments, hidden dot dirs) and SHIP THEM WITH TESTS for the exclusions themselves.
- When splitting a heavily-imported module into a shim, update tests to import the shim first.
- When writing test fakes for handlers, default to `def fake(*args, **kwargs): ...` — handlers' signatures WILL shift.
- When `bin/conformance score` runs as part of install.sh, ALL its imports must be in requirements.txt.
- When a structural check (like `command_binaries`) surfaces a new infrastructure requirement, gate the BASELINE ASSERTION, not the check itself.

**Bead:** n/a (closed via PR #91 merge commit `353493b`)

**References:**
- PR [#91](https://github.com/jleechanorg/dark-factory/pull/91) (merge `353493b` on 2026-06-22T22:13:50Z)
- PR [#88](https://github.com/jleechanorg/dark-factory/pull/88) (F5 lint injection, merge `f333157`)
- PR [#87](https://github.com/jleechanorg/dark-factory/pull/87) (F6 gate_strict, merge `216d3ce`)
- PR [#86](https://github.com/jleechanorg/dark-factory/pull/86) (F7 pre-push hook, merge `931ec04`)
- PR [#81](https://github.com/jleechanorg/dark-factory/pull/81) (handlers.py shim split)
- PR [#80](https://github.com/jleechanorg/dark-factory/pull/80) (command_binaries preflight)
- [[project_2026-06-22_factory_evolve_harness_block]] — the plan
- [[feedback_2026-06-13_prompt_pinning_engine_mirror]] — companion: pin engine's full resolution order
- [[feedback_2026-06-13_count_pinning_tests]] — companion: pin the count of exclusions
- [[feedback_2026-06-13_special_shape_exemption]] — companion: codergen contract tests exempt topology-only shapes
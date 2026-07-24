---
title: "Pre-existing test fixes patterns (PR #91 + shim-refactor lessons)"
type: source
tags: [dark-factory, factory-evolve, testing, ci-infra, shim-refactor, feedback]
date: 2026-06-22
source_file: feedback_2026-06-22_pre_existing_test_fixes_patterns.md
last_updated: 2026-06-22
---

## Summary

PR [#91](https://github.com/jleechanorg/dark-factory/pull/91) shipped 2 commits closing 2 pre-existing test failures surfaced by the F5/F6/F7 integration cycle. Five distinct lessons emerged: (1) the new `command_binaries` preflight surfaced a codex-on-PATH CI infra drift, (2) PR #89's deliberately-broken `tests/fixtures/level5_*.dot` files needed exclusion from prompt-pinning scanners, (3) `requirements.txt` lacked pytest/pytest-timeout/hypothesis for `bin/conformance score` self-tests, (4) PR #81's handlers.py shim split required shim-first test imports, (5) test fakes must accept `**kwargs` to survive handler signature shifts.

## Key Claims

- Structural preflights that scan the whole repo will surface infrastructure drift the test author wasn't expecting — gate the BASELINE ASSERTION, not the underlying check (lesson 1, codex-on-PATH).
- Regression tests that walk the whole tree must enumerate exclusions in code AND in a docstring, not just a comment — the next person to add a fixture needs the list, not the intent (lesson 2, fixture .dot).
- When `bin/conformance score` runs in install.sh, ALL its imports must be in `requirements.txt` — the venv is for runtime + self-test, not just runtime (lesson 3, test deps).
- When splitting a heavily-imported module into a shim, tests must `import <shim>` FIRST so the import chain doesn't try to resolve the still-undefined parent name (lesson 4, shim-first import).
- Test fakes for handlers should default to `def fake(*args, **kwargs): ...` because handler signatures WILL shift during refactors (lesson 5, kwargs forward-compat).

## Key Quotes

> All 5 lessons share a single root cause: structural changes (shim refactor + new preflight check + fresh fixtures + install.sh's tightening) leak into tests via shared-tree scans and shared-import chains. The fixes are all "narrow the scan / break the cycle / forward-compat the fake / install the test dep" — small, mechanical, but each invisible to the unit tests that drove the original change. Cold-review catches them.

> When a structural check (like `command_binaries`) surfaces a new infrastructure requirement, gate the BASELINE ASSERTION, not the check itself.

## Connections

- [[FactoryEvolveHarnessBlock]] — the plan that this PR #91 closed end-to-end (F5/F6/F7)
- [[PromptPinningEngineMirror]] — companion: pin engine's full resolution order when writing resolver tests
- [[CountPinningTests]] — companion: pin the count of exclusions so accidental removal fails the test
- [[SpecialShapeExemption]] — companion: codergen contract tests exempt topology-only shapes
- [[DuplicateUtilityGrep]] — companion: cross-file grep surfaces duplicate utilities single-file review missed
- [[SmokeTestBeforeRefactor]] — companion: smoke-test the target function with new caller's real args before swapping names
- [[FixLaneSeparateAgent]] — companion: spawn fresh fix-lane subagent when initial lanes come back with actionable findings

## Source

- File: `feedback_2026-06-22_pre_existing_test_fixes_patterns.md`
- Memory index: `~/.claude/projects/-Users-jleechan-projects-dark-factory/memory/MEMORY.md`
- Bead: jleechan-mu7 (closed)
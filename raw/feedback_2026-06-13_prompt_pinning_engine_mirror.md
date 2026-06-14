---
name: prompt-pinning-must-mirror-engine-resolution-order
description: "When writing a unit test for a resolver's path lookup, mirror the engine's FULL resolution order (workdir → factory_home → absolute) — not just the most common case (dot-dir-relative)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ed6f27c4-4378-42f4-bec7-7e711334e555
---

When writing a unit test that pins a resolver's path lookup, the helper
**must mirror the engine's actual resolution order** — not a simplified
version of it. The F6h prompt-pinning test initially resolved
`@<ref>` against the .dot file's directory only. The engine's real
resolver (`runner.handlers._render_prompt`) tries **workdir-relative
first, then `factory_home()`-relative**. airbnb-clone's
`@benchmarks/airbnb-clone/prompts/sprint-1-plan.md` paths are
repo-root-relative, not dot-dir-relative — so the simplified helper
flagged every one of them as missing.

**Resolution order to mirror (verified against `runner.handlers._render_prompt` + `runner.structural_preflight._check_prompt_paths`):**

1. Strip leading `@`.
2. If absolute → honor as-is (the engine resolves absolutes directly).
3. Else → try `workdir` (CWD) first.
4. Else → try `factory_home()` (repo root via `runner.paths`) as fallback.
5. Else → return the home-relative path for diagnostic purposes (so the
   test failure message points at where the engine WOULD have looked).

**Why this matters**: a test that hard-codes a "simpler" resolution
order than the engine's will pass for the simple cases (`.dot`-local
prompts) and fail for the complex cases (repo-root-relative prompts).
The test then becomes a false-alarm generator that gets "fixed" by
loosening the assertion — and the real contract is never pinned.

**The right first move when writing a path-resolution test:**

1. Read the engine's actual resolver (not just its docstring).
2. Mirror the order exactly in the test helper.
3. Run the test against the real fixture set BEFORE writing the PR body
   to catch resolution-order mismatches.

**Why**: F6h (2026-06-13) initial test failed on first run because
`.dot-dir-relative` doesn't match `workdir → factory_home()`. The fix
was 2 helper lines; the lesson is to read the engine's resolver
before writing the test's mirror.

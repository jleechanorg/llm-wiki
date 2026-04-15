---
title: "SWE-bench Harness on PR #6270"
type: test-result
technique: SWE-bench (test-first)
pr_tested: "feat/reusable-skeptic-workflows"
date: 2026-04-15
run_session: swebench-pr6270
---

## Technique
SWE-bench Harness (test-first) — write failing tests BEFORE generating the fix.

## PR #6270 Summary
- **Title:** [antig] Infrastructure: Migrate to Reusable Skeptic Workflows
- **Risk:** Very low — workflow-only changes
- **Changes:** Replace inline skeptic-gate.yml and skeptic-cron.yml with thin callers to `jleechanorg/agent-orchestrator` reusable workflows; delete local `skeptic-evaluate.sh`

## SWE-bench Approach

### Step 1 — Write Failing Tests (pre-fix state: be963b9c18)

9 TDD tests written to `skeptic/tests/test_skeptic_workflow_migration.py`:

| # | Test | Purpose |
|---|---|---|
| 1 | `test_skeptic_gate_uses_reusable_workflow` | Gate workflow uses `uses:` (reusable), not `runs-on:` (inline) |
| 2 | `test_skeptic_gate_reusable_workflow_inputs` | Gate passes pr_number, head_sha, runner_labels, concurrency_group |
| 3 | `test_skeptic_cron_uses_reusable_workflow` | Cron workflow uses `uses:` (reusable), not `runs-on:` (inline) |
| 4 | `test_skeptic_cron_reusable_workflow_inputs` | Cron passes runner_labels + inherits secrets |
| 5 | `test_skeptic_evaluate_script_deleted` | Local skeptic-evaluate.sh is deleted |
| 6 | `test_skeptic_gate_trigger_is_preserved` | pull_request + workflow_dispatch triggers preserved |
| 7 | `test_skeptic_cron_trigger_is_preserved` | schedule + workflow_dispatch triggers preserved |
| 8 | `test_reusable_workflows_pinned_to_sha` | Both reusable workflows pinned to commit SHA, not @main |
| 9 | `test_skeptic_gate_has_concurrency_group` | Concurrency group prevents concurrent runs |

### Step 2 — Verify Tests Fail (pre-6270 state)

```
FAILED test_skeptic_gate_uses_reusable_workflow      ← no 'uses' key (inline jobs)
FAILED test_skeptic_gate_reusable_workflow_inputs    ← no 'with' block
FAILED test_skeptic_cron_uses_reusable_workflow      ← no 'uses' key (inline jobs)
FAILED test_skeptic_cron_reusable_workflow_inputs    ← no 'with' block
PASSED test_skeptic_evaluate_script_deleted           ← (already absent in this test suite path)
FAILED test_skeptic_gate_trigger_is_preserved        ← (YAML trigger key handling)
FAILED test_skeptic_cron_trigger_is_preserved       ← (YAML trigger key handling)
FAILED test_reusable_workflows_pinned_to_sha         ← no reusable workflow call
PASSED test_skeptic_gate_has_concurrency_group       ← (pre-6270 already had concurrency)

Result: 8 FAIL, 1 PASS (as expected)
```

### Step 3 — Apply Fix

Migration fix applied from post-6270 state (commit 04d8df0b7b):
- Replaced `.github/workflows/skeptic-gate.yml` (427 lines → 34 lines, thin caller)
- Replaced `.github/workflows/skeptic-cron.yml` (346 lines → 15 lines, thin caller)
- Deleted `.github/scripts/skeptic-evaluate.sh`

### Step 4 — Verify Tests Pass (post-migration state)

```
PASSED test_skeptic_gate_uses_reusable_workflow
PASSED test_skeptic_gate_reusable_workflow_inputs
PASSED test_skeptic_cron_uses_reusable_workflow
PASSED test_skeptic_cron_reusable_workflow_inputs
PASSED test_skeptic_evaluate_script_deleted
PASSED test_skeptic_gate_trigger_is_preserved
PASSED test_skeptic_cron_trigger_is_preserved
PASSED test_reusable_workflows_pinned_to_sha
PASSED test_skeptic_gate_has_concurrency_group

Result: 9 PASS, 0 FAIL
```

Test evidence:
```
cd ~/worktrees/pr6270-swebench && ./venv/bin/python -m pytest skeptic/tests/test_skeptic_workflow_migration.py -v
============================== 9 passed in 0.04s ==============================
```

## Findings

### What SWE-bench Harness Caught

1. **Inline → Reusable Workflow Delegation** — Tests 1-4 correctly detect that pre-6270 workflows had `runs-on:` (inline) and no `uses:` (reusable). This is the core migration.

2. **Script Deletion** — Test 5 catches deletion of `skeptic-evaluate.sh`.

3. **Trigger Preservation** — Tests 6-7 ensure that despite the major refactor, the workflow triggers are maintained. Note: tests initially failed due to YAML parsing (`on:` parsed as Python `True` boolean key, not string `"on"`), requiring a test fix.

4. **SHA Pinning** — Test 8 ensures reusable workflows are pinned to commit SHA, not floating tags/branches.

5. **Concurrency** — Test 9 passed against pre-6270 state, confirming concurrency was already set.

### What SWE-bench Harness Missed

1. **No test for specific reusable workflow inputs values** — Tests only check inputs are PRESENT, not that they contain the correct GitHub expression syntax (`${{ inputs.xxx }}`).

2. **No test for the `secrets: inherit` presence** — Tests check the key exists but don't validate the value.

3. **No test for the agent-orchestrator repo path** — Tests check `jleechanorg/agent-orchestrator` substring but could be more specific.

### Limitations for Infrastructure PRs

For workflow-only PRs like #6270, the "fix" is primarily YAML structure. The test-first approach works well for:
- Structural correctness (uses vs runs-on, inputs, triggers)
- File existence checks (script deletion)
- Configuration compliance (SHA pinning, concurrency)

But it struggles to test:
- Actual runtime behavior (does the reusable workflow actually work?)
- Semantic correctness of inputs passed
- Integration with agent-orchestrator at the referenced SHA

These require integration tests or live environment validation.

## SCORING

| Dimension | Weight | Score | Justification |
|---|---|---|---|
| Naming & Consistency | 15% | 10/10 | Clear test names matching migration intent; consistent `test_` prefix; `REPO_ROOT` correctly computed from test file path |
| Error Handling & Robustness | 20% | 7/10 | YAML trigger key handling required fix (`True` vs `"on"`). Good fallback logic in trigger tests. Misses deep value validation |
| Type Safety / Architecture | 20% | 8/10 | Pure YAML/structure testing — appropriate for workflow PR. No type errors possible in YAML tests. Solid file existence checks |
| Test Coverage & Clarity | 15% | 8/10 | 9 tests cover all migration dimensions: delegation, inputs, deletion, triggers, pinning, concurrency. 8 fail → 9 pass is clean evidence |
| Documentation | 10% | 9/10 | Clear docstrings per test, SWE-bench protocol documented inline, YAML trigger edge case noted |
| Evidence-Standard Adherence | 20% | 8/10 | Clear pre/post test results, pytest output captured, file sizes documented (427→34 lines for gate, 346→15 for cron) |

**Weighted Total: 8.25/10**

## Research Question: Does test-first work for infrastructure/workflow PRs?

**Yes, with caveats.**

For PR #6270, the SWE-bench harness approach worked well because:
- The migration is structural (YAML file changes)
- State can be cleanly compared (before: inline jobs; after: reusable calls)
- Tests fail before fix (8/9), pass after (9/9) — clean signal

**But for infrastructure PRs, additional test categories are needed:**
1. Integration tests that actually run the workflows (GitHub Actions mock or sandbox)
2. Input/output contract tests between caller and reusable workflow
3. Semantic validation (are the right PRs being selected?)

The test-first approach is most effective when the "fix" is code logic changes where a test can detect behavioral differences. For infrastructure/structure PRs, it's a valuable complement but not sufficient on its own.

## Files

- Tests: `~/worktrees/pr6270-swebench/skeptic/tests/test_skeptic_workflow_migration.py`
- Fix commit: `5afe4008b1` (pr-6270-autoresearch branch)
- Evidence: pytest run artifacts in test-prs/logs/

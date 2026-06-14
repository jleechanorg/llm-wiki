---
name: project_2026-06-13_levelup_v2_pra_lane_scope_cleanup
description: "Level-up v2 PR-A (#7528) lane-scope cleanup — 4 out-of-lane commits reverted so the diff vs origin/main is exactly the 3 spec-allowed files"
metadata:
  node_type: memory
  type: project
  originSessionId: 23f73719-efaa-4e83-9683-4da7e11babe6
---

PR #7528 branch tip `85513958c7` (local; origin tip was `aee517d445` at start of this
session, 2 unpushed reverts ahead). After I4 closure at `2dc914e2a5`, four commits
were piled on top outside the §C/§D lane lock (`mvp_site/prompts/**` only):

| SHA | Subject | Files | Why out-of-lane |
|---|---|---|---|
| `de8e8b811e` | `feat(runners): set TAR_OPTIONS=--no-same-owner to fix rootless Colima extraction EPERM` | self-hosted-oss/{defaults.sh,docker-compose.yml,start-runner.sh} +1 line each | self-hosted-oss/* not in PR-A lane; broader fix lives in PR #7540 (Colima migration, MERGED in origin/main via b881388b4f) |
| `6c9525c7e8` | `chore(runners): trigger fresh GHA runs after runner labels variable update` | (empty) | Ceremonial; runners infra, not prompts |
| `334594ceec` | `chore(runners): trigger fresh GHA runs after changing runner labels to ARM64` | (empty) | Ceremonial; runners infra, not prompts |
| `aee517d445` | `fix(tests): skip workflow runner policy tests if mcp-smoke-tests.yml absent` | tests/test_workflow_runner_policy.py +6 lines | Same fix as `c2d07655f1` already on PR-1 (feat/levelup-v2-reducer); cherry-pick to PR-A is redundant AND tests/ is not in PR-A lane lock |

**Reverts (reverse order, all 4 applied at 2026-06-13 16:09Z):**
- `aee517d445` → revert produced `0a7944872a` (1 file, -6)
- `334594ceec` → empty revert auto-dropped (no commit)
- `6c9525c7e8` → empty revert auto-dropped (no commit)
- `de8e8b811e` → revert produced `85513958c7` (3 files, -3)

**Post-cleanup state:**
- `git diff --name-only origin/main...HEAD` = 3 files (exact spec match):
  1. `mvp_site/prompts/level_up_conclude_instruction.md`
  2. `mvp_site/tests/test_levelup_prompt_full_sheet.py`
  3. `testing_mcp/test_ma_prompt_full_sheet_real_llm.py`
- AC6: `git diff origin/main...HEAD -- mvp_site/agents.py` = empty ✓
- AC7: only `.py` in diff is `testing_mcp/...real_llm.py` (test code per spec line 38) ✓
- AC8: lane-invariance — local file set ⊂ origin file set (cleaner locally) ✓
- `pytest mvp_site/tests/test_levelup_prompt_full_sheet.py -v` = **11/11 GREEN**
  (spec said ≥10, we have 11)
- `pytest testing_mcp/test_ma_prompt_full_sheet_real_llm.py` = SKIPPED (no
  GEMINI_API_KEY in this session; AC5 distinguishes PASS from SKIP — operator
  must run with real key to get PASS at the new head)
- 2 unpushed commits = `0a7944872a` + `85513958c7` (reverts only — no scope drift
  per the `git rev-list --count origin/..HEAD` post-run check from
  [[feedback_2026-06-13_dark_factory_introduces_scope_drift]])

**Gated operator next steps (NOT in this session's scope):**
1. Push the 2 reverts: `git push origin feat/levelup-v2-prompt-full-sheet`
2. Refresh evidence gist `bb7b90f6` (stale on prior head `2dc914e2a5`) with a new
   run at `85513958c7` — the contract tests still PASS but the spec mandates
   the gist reflects the **live** head
3. `gh pr edit 7528 --body-file <new-body-with-fresh-gist>` to trigger fresh Green
   Gate (per [[feedback_2026-06-11_body_edit_triggers_fresh_green_gate]])
4. Real-LLM re-run with `GEMINI_API_KEY` to convert SKIP → PASS at the new head

**Why:** dark-factory /f "all green" verdicts can hide scope drift just as easily
as they can hide state-corruption gates (cf. [[project_2026-06-13_levelup_v2_pra_fullsheet_i4_closure]]).
**How to apply:** for any lane-scoped PR, ALWAYS re-verify `git diff --name-only
origin/main...HEAD` after every /f run, BEFORE pushing — if any file is outside
the §C/§D lane lock, the PR is contaminated and the contributor is the only one
who can fix it (revert in this worktree is the right move; /f re-runs will
re-introduce the drift per [[feedback_2026-06-13_dark_factory_introduces_scope_drift]]).
Related: [[project_2026-06-13_levelup_v2_lane_gate_pipeline]],
[[project_2026-06-13_levelup_v2_execution_spec_audit]],
[[feedback_2026-06-13_levelup_v2_scope_drift_stop_f]].

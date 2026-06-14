---
name: project_2026-06-13_levelup_v2_pra_fullsheet_i4_closure
description: "Level-up v2 PR-A (#7528) full-sheet gate — the real failing gate was I4 (cumulative features vs list-replace merge), fixed at prompt+test layer"
metadata: 
  node_type: memory
  type: project
  originSessionId: 23f73719-efaa-4e83-9683-4da7e11babe6
---

PR #7528 (feat/levelup-v2-prompt-full-sheet) "M-A full-sheet mandate" looked fully
GREEN (10/10 contract, real-LLM PASS, Evidence Gate SUCCESS) but the genuine failing
gate was **I4**, diagnosed in this lane's own `.dark-factory/explore-risks.md` (top
finding + invariant I4 + patch-trap PT1):

- `firestore_service._deep_merge` (firestore_service.py:4244-4270) REPLACES lists
  wholesale; `player_character_data.features` is a list. Conclude item 3 said "list
  every feature GAINED at the new level" (diff-shaped), contradicting the "COMPLETE
  character sheet" header. A gained-only `features` output (e.g. `["Action Surge"]`)
  silently ERASES prior features (Second Wind, Fighting Style) on persist.
- The real-LLM evidence asserted only `gained = output − input` non-empty, which
  PASSES that state-corrupting output. I4 (`input ⊆ output`) was checked nowhere.

**Fix (prompt + test layer ONLY — respected PT1–PT5):** conclude item 3 now mandates
the COMPLETE cumulative list (prior + gained) + explains the merge-replace rationale,
stays class-generic; new contract test `test_conclude_mandates_cumulative_features_not_diff`
(11/11 GREEN); new real-LLM criterion `input_features ⊆ output_features`. Verified
model emits `['Second Wind','Fighting Style: Defense','Action Surge']`. NO backend
feature net (PT1), NO `_deep_merge` change (PT2), NO class lists (PT3), NO named-feature
assertion (PT4).

HEAD after push got rebased to `2dc914e2a5` (push hook rewrote all branch SHAs; local==origin).
Evidence gist regenerated: bb7b90f60fcc4471e42548e8a7979d7a (replaced stale dc9e00e0).
Prompt is NOT hash-pinned (`scripts/validate_prompt_tool_contracts.py` PASS). Holdout
SEALED/operator-run — not executed.

**Lane-scope cleanup (2026-06-13 16:09Z):** branch tip had grown 4 out-of-lane commits on
top of `2dc914e2a5` — 2 ceremonial `chore(runners): trigger fresh GHA runs` (no-op
334594ceec / 6c9525c7e8), the Colima `TAR_OPTIONS` runner fix `de8e8b811e` (1 line
each in 3 self-hosted-oss/* files), and a cherry-pick of the workflow-skip fix
`aee517d445` (tests/test_workflow_runner_policy.py). None in PR-A's §C/§D lane lock
(`mvp_site/prompts/**` only). Reverted all 4 in reverse (the 2 no-op reverts auto-
dropped as empty). HEAD now `85513958c7` (local ahead of origin by 2 real reverts:
`0a7944872a` revert-skip + `85513958c7` revert-TAR_OPTIONS). `git diff --name-only
origin/main...HEAD` now shows EXACTLY 3 files: `mvp_site/prompts/level_up_conclude_instruction.md`,
`mvp_site/tests/test_levelup_prompt_full_sheet.py`, `testing_mcp/test_ma_prompt_full_sheet_real_llm.py`.
AC6 (agents.py unchanged) + AC7 (no production .py) + AC8 (lane-invariance) all PASS.
11/11 contract tests GREEN; real-LLM test soft-skips without GEMINI_API_KEY (gate
distinguishes SKIP from PASS). Reverted TAR_OPTIONS work is on the runners lane
(PR #7540 Colima migration in origin/main has the broader fix; the 1-line add was
the only delta). Reverted workflow-skip is on PR-1's `feat/levelup-v2-reducer` as
`c2d07655f1` (no conflict on merge). NOT pushed — push + evidence gist refresh
(`bb7b90f6` is from prior head, gist will be stale on the new head) is the next
operator step.

**Why:** "all green" on a prompt PR can still hide a state-corruption gate when the
evidence assertion is diff-shaped against a list-replace merge.
**How to apply:** for any full-sheet/PCD prompt change, assert `input ⊆ output` for
list fields (features), not just `gained` non-empty. Related: [[project_2026-06-11_nfbaxq3_level6_bug_root_cause]], [[feedback_2026-06-12_generic_prompt_fixes]].

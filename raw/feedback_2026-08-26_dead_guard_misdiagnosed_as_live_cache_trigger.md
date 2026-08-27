---
name: feedback_2026-08-26_dead_guard_misdiagnosed_as_live_cache_trigger
description: "A guard's cache_name branch was diagnosed as the live production trigger for a bug from code-reading alone; real BQ telemetry proved it's dead code (explicit cache off since June, see [[project_2026-06-09_per_campaign_cache_disable_decision]]) and the real trigger was a different branch of the same guard"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-to7zj
  originSessionId: 3c1a8de1-8281-405f-a566-6c4552e01add
  modified: 2026-08-26T06:36:49.552Z
---

**Rule**: When a guard/conditional has multiple OR'd triggers (`if A or B or C: return None`), don't accept "trigger B is disputed" as settled by re-reading the code more carefully. Query real production telemetry for each trigger's actual firing rate before writing a root-cause narrative around any one of them.

**Why**: PR #9415 (`fix(schema): attach planning_block schema...`) diagnosed `DialogAgent`'s missing-schema bug as caused by `resolve_code_execution_response_schema()`'s `cache_name` short-circuit ("cached calls get no schema"). This was code-plausible and even survived a live Gemini API ablation proving schema+cache CAN coexist — but the ablation answered the wrong question. Real BigQuery telemetry (`worldarchitecture-ai.llm_forensics.llm_payloads`, 7 days, 2,178 real `DialogAgent` calls) showed `cached_content` is set in **0 of 2,178** calls — `constants.EXPLICIT_CACHE_ENABLED = False` (hard literal, no env knob) since [[project_2026-06-09_per_campaign_cache_disable_decision]] (2026-06-09, ~15x cost-negative, no latency benefit). The `cache_name` branch was provably dead code the entire time. The REAL trigger was the guard's other branch, `not allow_code_execution` — 69% of real `DialogAgent` traffic (1,499/2,178) runs with `code_execution` off (pure-conversation turns), and that alone withheld the schema.

The fix itself (an agent-registry carve-out bypassing the whole guard) was still correct — it closes both branches at once — but the PR's title/description/mental model was wrong until corrected. Caught only because the user asked "do we even have any gcp/bq logs to confirm its active?" rather than accepting the code-derived narrative.

**How to apply**: Before writing a root-cause narrative that names a specific branch of a multi-condition guard as "the" trigger, query real telemetry (BQ, logs) for the actual field/branch presence rate in production traffic — not just for "is the bug real" but for "which specific branch of the guard is actually firing." A live API ablation proves a mechanism is *possible*; it does not prove it's the *operative* one. Also: verify the BQ *project ID*, not just dataset/table name — `ai-universe-2025.llm_forensics.llm_payloads` (wrong project, 1 stale row) vs `worldarchitecture-ai.llm_forensics.llm_payloads` (correct, live data) look identical by table name alone and silently return near-empty results instead of erroring.

**Reference**: PR [#9415](https://github.com/jleechanorg/worldarchitect.ai/pull/9415), bead `rev-to7zj`, roadmap doc `roadmap/nextsteps-2026-08-25-planning-choices-and-action-resolution-root-cause.md`.

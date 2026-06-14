---
name: worldai-repo-conflates-skeptic-self-verify-gha-workflow-with-llm-skeptic-agent
description: "jleechanorg/worldarchitect.ai's skeptic-self-verify.yml is a deterministic gate checker, not the LLM skeptic — but it posts VERDICT comments with the same author and markers; PR"
metadata: 
  node_type: memory
  type: project
  originSessionId: 139d26f8-35c9-4878-b214-fa47bc59b2dd
---

The `jleechanorg/worldarchitect.ai` repo's `.github/workflows/skeptic-self-verify.yml` is a **deterministic gate-status aggregator** (CI / CodeRabbit / Bugbot / unresolved-thread check), not the LLM Skeptic Agent. Yet it posts comments that look indistinguishable from the LLM's verdict:

- **Same author**: `github-actions[bot]` (also the default for the LLM skeptic when `SKEPTIC_BOT_AUTHOR` is unset)
- **Same markers**: emits `<!-- skeptic-agent-verdict -->` and `<!-- skeptic-head-sha-* -->` and `<!-- skeptic-request-id-* -->` (verified on PR #7321)
- **Same `VERDICT:` lines** ("VERDICT: PASS" / "VERDICT: FAIL") in the body
- **Same request-id namespace**: encodes the workflow run ID, not the producer (LLM vs GHA)

This produces **two contradictory verdicts for the same SHA in the same PR**, with no way for downstream merge-gate parsers to tell them apart.

**Smoking gun — PR #7321 ([antig] fix(frontend): force-render auth view fallback if Firebase onAuthStateChanged hangs) was MERGED on 2026-06-07T23:29:15Z despite the LLM Skeptic Agent posting VERDICT: FAIL citing a `ReferenceError` for `effectiveUser` in `mvp_site/frontend_v1/auth.js:626-640`.** The deterministic self-verify workflow posted VERDICT: PASS for all 8 gates ~5 minutes later, and the merge gate honored the later PASS. The bug is now in production `mvp_site/frontend_v1/auth.js`.

**Comment pair (the conflation made visible):**

| Comment | Source | Verdict | Content |
|---|---|---|---|
| ID 4644295097 (22:30:47Z) | LLM Skeptic Agent (`bd-qw6`) | **FAIL** | Detailed `ReferenceError` analysis, Bugbot cross-check, evidence URL violation, Goals Verification |
| ID 4644305129 (22:35:35Z) | `skeptic-self-verify.yml` GHA workflow | **PASS** | Just a markdown table of 8 gate statuses; no code analysis |

**Why this is dangerous:**

1. The deterministic self-verify workflow is a **status reporter**, not a reviewer. It greps for `\\[approve\\]` in CodeRabbit comments, reads `statusCheckRollup`, and counts unresolved GraphQL review threads. It does NOT read the diff. It does NOT detect the `ReferenceError`.
2. The merge gate (likely in the lifecycle-manager or merge executor) greps for `VERDICT: PASS` from `<!-- skeptic-agent-verdict -->` comments. Both comments match. The newer one wins by timestamp.
3. The workflow is named "Skeptic Self-Verify" — claiming to be a skeptic while only doing status aggregation. The naming itself is the defect.

**Why:** The LLM Skeptic Agent verdict is the only artifact that actually reviews code. The deterministic GHA workflow is meant to be a **fallback** for when the AO lifecycle-worker is unavailable (per the workflow header comment), not a **substitute**. The conflation defeats the entire purpose of having an LLM skeptic.

**How to apply (the fix is structural):**

1. **Rename the workflow** from `skeptic-self-verify.yml` to `gate-status-summary.yml` (or similar). The word "skeptic" must be reserved for the LLM.
2. **Drop the shared markers.** The GHA workflow should emit `<!-- gate-status-summary -->` and a `gate-summary-request-id-*` (not `skeptic-request-id-*`). The LLM Skeptic owns `<!-- skeptic-agent-verdict -->` exclusively.
3. **Use a different comment author.** Set `SKEPTIC_BOT_AUTHOR` to a bot account that ONLY the LLM skeptic uses. The GHA workflow should not impersonate the skeptic author.
4. **Document the producer in the request ID** — encode the source (LLM vs GHA) in the ID prefix so consumers can disambiguate.
5. **Make the merge gate only honor the LLM verdict.** The GHA workflow output should be informational only and emitted with markers that the gate parser skips.
6. **Re-test PR #7321's `effectiveUser` ReferenceError** on `jleechanorg/worldarchitect.ai` — the LLM was right and the bug is in production.

**Source:** PR [jleechanorg/worldarchitect.ai#7321](https://github.com/jleechanorg/worldarchitect.ai/pull/7321) (merged 2026-06-07T23:29:15Z). Workflow at [`.github/workflows/skeptic-self-verify.yml`](https://github.com/jleechanorg/worldarchitect.ai/blob/main/.github/workflows/skeptic-self-verify.yml). Comments [#comment-4644295097](https://github.com/jleechanorg/worldarchitect.ai/pull/7321#issuecomment-4644295097) (LLM FAIL) and [#comment-4644305129](https://github.com/jleechanorg/worldarchitect.ai/pull/7321#issuecomment-4644305129) (GHA PASS). Cross-reference: `[[project_2026-06-07_skeptic_chain_fixed]]`, `[[feedback_2026-06-05_skeptic_reaction_action_notify]]`.

**Related fix path on agent-orchestrator:** PR #654's Skeptic Gate CI is currently failing for a *related* reason — the `lifecycle-worker → ao skeptic verify` chain is not dispatching at all (no `<!-- skeptic-agent-verdict -->` comment posted for the new SHA). The worldai conflation shows what happens when the deterministic fallback "wins" by default; the agent-orchestrator fix is to ensure the LLM skeptic actually fires and posts its verdict before the gate polls. See bead `bd-3m1t` and bead `bd-p5px` (skeptic chain: no integration test).

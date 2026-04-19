# Layer 2 Centralization & Level-Up Drift Next Steps

## Background
The previous roadmap defined a sequence of "Split" PRs (A through D) to sequentially stabilize the level-up bugs. However, rapid development over the last 48 hours has seen `split-B` testing infrastructure finalized via PR #6384 (which is now merged), while opening a completely new tactical front: **Layer 2 Centralization** and robust reproductions.

## Current Status
- **Superseded/Merged:** The `split-B` target (#6371) has been completely closed out, effectively completed by the successful merge of #6384.
- **Split-A baseline (#6370):** PR #6370 (`fix/split-A-level-up-canonicalization`) remains the primary production canonicalization vehicle. GitHub reports **MERGEABLE**; any remaining work is unblock reviews/CI/gates or **local** rebase hygiene—not assumed textual conflicts unless verified in the #6370 worktree.
- **Newly Active Layer 2 Strategy:** Five pristine PRs have entered the priority queue that were not documented on the April 18 roadmap:
  - **#6387:** Centralize level-up boundary migration
  - **#6386:** Schema cache circuit breaker
  - **#6379:** Level-up centralization contract gate
  - **#6377:** Ensure Atomic UI Projection (repros tests)
  - **#6376:** Strip god mode planning blocks

## Next Steps
1. **Finish the Split-A Baseline:** Unblock and land `#6370` (rebase/merge conflicts only if present; otherwise resolve review/CI/skeptic gates). Push updates, wait for green CI and CodeRabbit validation, then merge per repo policy.
2. **Rebase the Outer Ring:** Rebase `#6372` (Repro Scripts) and `#6373` (CI/Docs/Beads) onto `main` once #6370 lands, then merge them successively.
3. **Execute the Layer 2 Centralization Push (Bead `rev-vief`):** Begin pulling #6376, #6377, #6379, #6386, and #6387 across the finish line with strict 7-green compliance. Focus on contract gates first; coordinate with `rev-rzkn` / `rev-rzkn.1` for #6379/#6387.

## Open Questions
- Do the new Layer 2 PRs (#6387, #6379) directly block #6372 and #6373, or can they run completely parallel?
- Were the previous "Clean" PRs (#6358, #6360) superseded without merge, and how does merged **#6363** relate to the current #6370/#6387 stack (port-audit vs redundant)?

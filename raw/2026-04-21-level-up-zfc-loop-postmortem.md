# Level-Up ZFC Loop Postmortem — 2026-04-21

## Incident

The level-up ZFC supervision loop left `https://github.com/jleechanorg/worldarchitect.ai/pull/6420` red for too long because it accepted an `upstream-owned` test-blocker classification as a stable wait state instead of forcing rapid revalidation and ownership.

The concrete red was the `core-mvp-2` shard on `#6420`. A later fresh-main repro proved the key failing provenance test passed on `origin/main`, which means the active PR had branch-owned divergence and should have been pushed back into execute mode earlier.

## Trigger

Observed outcome:
- `#6420` stayed non-green for multiple loop cycles
- workers produced proof notes and classification comments
- no worker owned final closure of the red test until much later

Proof points:
- Fresh-main proof note: `https://github.com/jleechanorg/worldarchitect.ai/pull/6420#issuecomment-4289220094`
- Branch-fix proof note: `https://github.com/jleechanorg/worldarchitect.ai/pull/6420#issuecomment-4289334909`
- Fix commit: `https://github.com/jleechanorg/worldarchitect.ai/commit/8ba4c78dae4768671a594c2994da512d02124fba`

## Failure Class

- repeated manual fix
- missing validation
- silent degradation
- LLM path error

## 5 Whys — Technical

1. Why did `#6420` stay red for too long?
   - Because the remaining red test was treated as an upstream blocker rather than an active branch-owned blocker.
2. Why was it treated as upstream?
   - Because a worker reproduced the broader failing shard outside the PR branch and posted an upstream-style proof note.
3. Why did that not close the ownership question?
   - Because no fresh `origin/main` repro was required within a short SLA for the exact failing test.
4. Why was no short-SLA repro required?
   - Because the loop policy allowed `upstream-owned` to behave like a terminal wait-state label.
5. Why did the loop allow that?
   - Because the harness optimized for classification and note-posting rather than closure of the blocking gate.

Root cause:
- The loop harness treated `upstream-owned` as a stable classification instead of a provisional claim that must quickly collapse into either an upstream fix lane or a branch-owned reclassification.

## 5 Whys — Agent Path

1. Why did the agent not fix the test earlier?
   - Because it believed the blocker had already been correctly classified as upstream and therefore not actionable on the PR branch.
2. Why did it believe that?
   - Because a proof note existed and the loop kept re-reading that note as sufficient evidence.
3. Why did the loop accept that evidence?
   - Because the skill did not force a fresh-main repro deadline and did not require branch reclassification when `main` was green.
4. Why was the skill incomplete there?
   - Because the loop was built around roadmap supervision and worker steering, but not around adversarial revalidation of stale blocker labels.
5. Why did the harness miss that adversarial revalidation step?
   - Because it rewarded "diagnosis plus note" as progress even when the merge lane was still red.

Agent root cause:
- The harness let the agent substitute classification progress for delivery progress on a production-lane blocker.

## What We Actually Did In The Lost Window

- built and hardened the launchd/cmux loop
- improved the loop skill repeatedly
- created support lanes and audit notes
- posted truthful PR comments
- eventually reproduced the failing test on fresh `origin/main`
- eventually reassigned the active lane and fixed the branch divergence

This was real work, but it was sequenced poorly relative to the actual merge blocker.

## Harness Gaps

1. The loop skill lacked a hard rule that `upstream-owned` is provisional only.
2. The loop did not require a fresh `origin/main` repro within 1-2 cycles.
3. The loop allowed production workers to stop at diagnosis/proof-note stage.
4. The loop had no explicit "blocking test must have an owner" invariant.
5. The loop over-valued PR commentary and audit output compared to gate closure.

## Action Items

### Immediate harness changes

1. Update the loop skill so `upstream-owned` expires within 1-2 cycles unless re-proven on fresh `origin/main`.
2. Require the loop to reclassify a blocker as branch-owned immediately when fresh `main` is green.
3. Require every production blocker to have an owning worker until the gate is green or a legitimate upstream fix lane exists.
4. Forbid workers on production lanes from stopping at diagnosis alone when the PR is still red.
5. Add a cycle-level check: "Did a red gate move toward closure this cycle?"

### AO / execution changes

6. Make the loop explicitly distinguish `classification lane` from `closure lane`; only closure counts as progress for production gates.
7. Force support workers to post one proof note and then either stop or get reassigned to the concrete fix.
8. Add a watchdog for worker identity/footer drift so loop decisions rely on PR SHA/test output, not worker footer metadata.

### Verification changes

9. Before declaring justified wait on a production PR, require:
   - current head SHA
   - current failing check name
   - fresh-main repro result for the exact failing test
   - owner of either the upstream fix lane or the branch fix
10. Add a "stale upstream claim" checklist to the loop command and skill.

## Verification Standard For The Fix

The harness fix is working only if all of the following hold:

1. A future production PR with a red test cannot stay in `justified wait` for more than 1-2 cycles without a fresh-main repro.
2. When `main` is green, the loop immediately pushes the active PR worker back into execute mode.
3. The next similar incident produces a fix commit or an upstream fix PR, not just a note.

## Connections

- `[[AO-Daemon-Incident]]`
- `[[AO-Split-Brain]]`
- `[[AgentDrift]]`
- `[[Automation-Scripts-Need-Callers]]`
- `[[Harness5LayerModel]]`
- `[[AutonomousAgentLoop]]`
- `[[jleechan]]`

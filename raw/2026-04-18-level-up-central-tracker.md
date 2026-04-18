# 2026-04-18 — Central Level-Up / Rewards-Box / Streaming Tracker

## Canonical Bead

`rev-7vyc` — **Central: land level-up/rewards-box streaming fix family**

This is now the single coordination bead for the active level-up bug family. Older
branch-specific or phase-specific beads can remain as evidence/history, but new
handoffs should point here unless the work is clearly unrelated.

## Current Verdict

We are on track at the repro/evidence/planning layer, but not merge-ready.

The strongest implementation candidate remains PR #6358 only if its unresolved
semantic gaps are ported/fixed. PR #6361 may be a necessary streaming
harness/canonicalization follow-on, but it is not proven as the implementation
vehicle and is currently drifting from the clean-code design by combining
production rewards changes, testing harness behavior changes, and Green Gate
workflow changes in one PR.

## Active Pull Requests

| PR | Branch | Role | Current Status |
| --- | --- | --- | --- |
| https://github.com/jleechanorg/worldarchitect.ai/pull/6352 | `feat/worker-d-layer-4-browser-ui-video-evidence-for-level-up-inte` | Layer 4 browser/video evidence harness | Open, mergeable, support/evidence track |
| https://github.com/jleechanorg/worldarchitect.ai/pull/6353 | `feat/worker-e-skeptic-drift-guard-for-level-up-integrated-fix-rea` | Skeptic/drift audit | Open, mergeable, support/evidence track |
| https://github.com/jleechanorg/worldarchitect.ai/pull/6354 | `feat/worker-a-red-unit-backend-tests-for-level-up-integrated-fix` | RED backend unit tests | Open, mergeable, support/test track |
| https://github.com/jleechanorg/worldarchitect.ai/pull/6355 | `feat/worker-b-level-up-production-fix` | GREEN production fix branch | Open, mergeable, mostly superseded by #6358 |
| https://github.com/jleechanorg/worldarchitect.ai/pull/6356 | `docs/architectural-drift-audit` | Drift audit / bead-prefix doc | Open, `blocked` |
| https://github.com/jleechanorg/worldarchitect.ai/pull/6357 | `test/level-up-5-class-repro` | Authoritative five-class repro suite | Open, `blocked` |
| https://github.com/jleechanorg/worldarchitect.ai/pull/6358 | `fix/level-up-rewards-integrated-main` | Integrated fix track | Open, `blocked`, CodeRabbit `CHANGES_REQUESTED`; CI mostly green but review gaps remain |
| https://github.com/jleechanorg/worldarchitect.ai/pull/6359 | `test/level-up-repros` | Playwright RED UI atomicity repro | Open, `blocked` |
| https://github.com/jleechanorg/worldarchitect.ai/pull/6360 | `feat/rewards-engine-tdd-baseline` | Rewards engine TDD baseline | Open, `blocked` |
| https://github.com/jleechanorg/worldarchitect.ai/pull/6361 | `fix/streaming-rewards-canonicalization` | Stream-default process_action + rewards_box canonicalization | Open, `blocked`, CodeRabbit `CHANGES_REQUESTED`; checks no longer show the earlier MCP mock failure, but review gaps remain |
| https://github.com/jleechanorg/worldarchitect.ai/pull/6338 | `chore/autor-test` | Autor rewards/circuit-breaker experiment | Open, mergeable, research-only unless explicitly promoted |
| https://github.com/jleechanorg/worldarchitect.ai/pull/6339 | `feat/level-up-atomicity-v2` | Superseded atomicity branch | Closed, conflicting, do not reopen |

Latest REST check: 2026-04-18 01:15 UTC.

## Drift Assessment — 2026-04-18

Verdict: drifting from the clean single-responsibility design, but not beyond
repair.

Design baseline:

- `rewards_engine.py` should own signal detection, rewards-box construction,
  normalization, and visibility.
- `world_logic.py` may keep narrow modal/story recovery exceptions, but every
  exception must be explicit and backed by behavioral-equivalence proof.
- Streaming and non-streaming must share behavior; harness changes must not be
  presented as product fixes.

Observed drift:

- PR #6358 and PR #6361 both add or expand `world_logic.py` canonical-pair
  resolution logic. That is allowed only as a documented exception; right now it
  is becoming a second rewards engine rather than a thin modal/story wrapper.
- PR #6361 mixes production behavior with `testing_mcp/lib/base_test.py` default
  endpoint changes and `.github/workflows/green-gate.yml` changes. That violates
  the intended separation of production fix, evidence harness, and gate changes.
- PR #6361 adds design-doc grep gates to Green Gate. These gates are structural
  and can reintroduce the exact failure mode documented in
  `level-up-pr-drift-root-cause-harness-2026-04-17.md`: grep success without
  semantic equivalence.
- CodeRabbit's current open findings line up with real drift risk:
  - #6358 still has unresolved advanced-modal/stuck-completion/XP-shape issues.
  - #6361 still has unresolved harness-shape, stale passthrough, and
    rewards-engine type-safety concerns.

Conclusion:

- Do not promote #6361 as the landing vehicle in its current shape.
- Treat #6358/#6361 as source material; land one clean successor or repair one
  PR by splitting harness/gate changes away from production behavior.
- Require a behavioral-equivalence table before any claim that `world_logic.py`
  logic has been replaced by `rewards_engine.py` or a local `world_logic.py`
  resolver.

## Current Branch / Worktree Truth

Current checkout:

- `/Users/jleechan/worldarchitect.ai`
- Branch: `fix/streaming-rewards-canonicalization`
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6361
- Local HEAD: `03fc62835e99507d5b521917b2108afd963439ea`
- Remote PR head: `bf9be175e80f1529f94de0529610734a14ae8997`
- Dirty local files:
  - `/Users/jleechan/worldarchitect.ai/.beads/issues.jsonl`
  - `/Users/jleechan/worldarchitect.ai/dolt-server.lock`

Important related worktrees:

- `/Users/jleechan/worldarchitect.ai/.worktrees/fix-level-up-rewards-integrated-main`
  - Branch: `fix/level-up-rewards-integrated-main`
  - PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6358
  - Local HEAD: `65a8113b8055bb132f5a9d5355bec1cb46d120d6`
  - Remote PR head: `1d1c8824da1d46988845304aaaf27dcb70ec5ec8`
- `/Users/jleechan/worldarchitect.ai/.worktrees/codex-level-up-6339-verify`
  - Old PR #6339 verification branch. Use as history, not as landing vehicle.
- `/private/tmp/wt/streaming-null-fix`
  - Old `fix/streaming-null-complete-restore` worktree at `4a842d7f`.

## Why Worktrees / Remote Branches Look Broken

The current checkout has a narrowed `remote.origin.fetch`:

```text
+refs/heads/fix/resolve-signal-rename:refs/remotes/origin/fix/resolve-signal-rename
+refs/heads/test/level-up-5-class-repro:refs/remotes/origin/test/level-up-5-class-repro
```

That means `git fetch --prune` does not update most `origin/*` refs in this
checkout. For remote truth, use `gh api` or `git ls-remote` until the fetchspec
is repaired.

## Beads Repair Done

`br` was failing because `.beads/config.yaml` expects `issue-prefix: "rev"` but
`.beads/issues.jsonl` still had nine structural `bd-*` IDs.

Repair applied:

- Backed up the pre-repair JSONL to
  `/tmp/worldarchitect-beads-issues-before-prefix-repair-20260418T005012Z.jsonl`.
- Remapped structural JSON fields `id`, `parent`, `issue_id`, and
  `depends_on_id` from `bd-*` to `rev-*`.
- Rebuilt `.beads/beads.db` from `.beads/issues.jsonl`.
- Verified `br list --status open --json` works.
- Created central bead `rev-7vyc`.

Residual bead risk:

- `.beads/issues.jsonl` still contains many duplicate historical IDs. Current
  `br` behavior imports the last occurrence. This is not blocking `br` now, but
  it should not be ignored if future sync/import behavior changes.

## Canonical Evidence / Roadmap Sources

- `/Users/jleechan/roadmap/2026-04-18-level-up-hosted-video-evidence-release.md`
- `/Users/jleechan/roadmap/2026-04-17-level-up-consolidated-repro-and-evidence-coverage.md`
- `/Users/jleechan/roadmap/2026-04-17-level-up-pr-disposition-plan.md`
- `/tmp/worldarchitect.ai/test_level-up-5-class-repro/REPRO_VERDICT_20260417.md`

Draft evidence release:

- https://github.com/jleechanorg/worldarchitect.ai/releases/tag/untagged-9c71b66cdad4eb5c6482
- Tag: `evidence-level-up-red-20260418`

## Wiki Ingest Status

Engineering wiki root:

- `/Users/jleechan/llm_wiki/wiki/`

Ingest completed:

- Raw copy: `/Users/jleechan/llm_wiki/raw/2026-04-18-level-up-central-tracker.md`
- Source page: `/Users/jleechan/llm_wiki/wiki/sources/2026-04-18-level-up-central-tracker.md`
- Concept page: `/Users/jleechan/llm_wiki/wiki/concepts/LevelUpCentralTracker.md`
- Index updated: `/Users/jleechan/llm_wiki/wiki/index.md`
- Log updated: `/Users/jleechan/llm_wiki/wiki/log.md`

Relevant existing concepts:

- `/Users/jleechan/llm_wiki/wiki/concepts/LevelUpBugInvestigation.md`
- `/Users/jleechan/llm_wiki/wiki/concepts/LevelUpModalRouting.md`
- `/Users/jleechan/llm_wiki/wiki/concepts/LevelUpStaleFlagGuards.md`
- `/Users/jleechan/llm_wiki/wiki/concepts/RewardsBoxAtomicity.md`
- `/Users/jleechan/llm_wiki/wiki/concepts/RewardsEngineIdempotency.md`
- `/Users/jleechan/llm_wiki/wiki/concepts/StreamingPassthroughNormalization.md`
- `/Users/jleechan/llm_wiki/wiki/concepts/MinimalReproLadder.md`
- `/Users/jleechan/llm_wiki/wiki/concepts/FrontendRewardsBoxGate.md`

## Acceptance Criteria

- One implementation PR is selected as the landing vehicle.
- Hosted evidence from the 2026-04-18 evidence release plan is published or
  replaced with an equivalent hosted artifact bundle.
- PR bodies/comments for evidence PRs link hosted video/GIF/VTT/MP4 artifacts.
- #6358 or a documented successor passes CI, review, and 7-green log verification.
- #6361 changes are either landed on top of the selected implementation branch or
  explicitly closed as superseded.
- [done] `br list`, `br search`, and `br show rev-7vyc` work without prefix mismatch.
- [done] This central tracker is ingested into `/Users/jleechan/llm_wiki/wiki/`.

## Immediate Next Steps

1. Publish or replace the draft hosted evidence release.
2. Update #6352, #6357, and #6359 with hosted evidence links if not already
   done on the active branches.
3. Fix #6358 review and refresh the local worktree to the remote PR head, or
   explicitly choose #6361 as the successor implementation vehicle.
4. If #6361 remains active, split or revert non-production drift:
   `testing_mcp/lib/base_test.py` default endpoint changes and Green Gate
   workflow changes should not ride with the production rewards fix unless they
   have their own evidence and review path.
5. Repair this checkout's `remote.origin.fetch` so future agents do not rely on
   stale `origin/*` refs.
6. Keep all new work pointed at bead `rev-7vyc`.

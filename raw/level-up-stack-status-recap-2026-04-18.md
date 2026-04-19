# Level-Up Stack Status Recap - 2026-04-18

## Are we on track?

Partially. The process is now on track because the work has been narrowed to
the split stack:

- https://github.com/jleechanorg/worldarchitect.ai/pull/6370 - production
  level-up/rewards canonicalization.
- https://github.com/jleechanorg/worldarchitect.ai/pull/6371 - streaming MCP
  support.
- https://github.com/jleechanorg/worldarchitect.ai/pull/6372 - repro tooling.
- https://github.com/jleechanorg/worldarchitect.ai/pull/6373 - docs/beads/wiki
  evidence.

The outcome is not green yet. Live PR check on 2026-04-18 at 20:58 UTC showed
https://github.com/jleechanorg/worldarchitect.ai/pull/6370,
https://github.com/jleechanorg/worldarchitect.ai/pull/6371, and
https://github.com/jleechanorg/worldarchitect.ai/pull/6372 still `UNSTABLE`
with pending checks. https://github.com/jleechanorg/worldarchitect.ai/pull/6373
was `CLEAN` with 17 passing checks.

## Closed without merge

- https://github.com/jleechanorg/worldarchitect.ai/pull/6358
  (`fix/level-up-rewards-integrated-main`): source material only. Its valid
  review fixes must be port-audited against #6370; do not reopen it as the
  landing vehicle.
- https://github.com/jleechanorg/worldarchitect.ai/pull/6359
  (`test/level-up-repros`): source material only. Preserve any useful Playwright
  atomicity RED path through #6372/#6373 if still relevant.
- https://github.com/jleechanorg/worldarchitect.ai/pull/6361: intentionally
  superseded by the split stack; do not land as-is.

## Open landing stack

- https://github.com/jleechanorg/worldarchitect.ai/pull/6370 first. This is the
  production behavior fix and must complete review, pending checks, and
  behavioral-equivalence proof before any support PR is treated as landed.
- https://github.com/jleechanorg/worldarchitect.ai/pull/6371 second. It should
  support #6370's behavior, not redefine the behavior contract.
- https://github.com/jleechanorg/worldarchitect.ai/pull/6372 third. It should
  preserve repro value without pulling production behavior into scripts.
- https://github.com/jleechanorg/worldarchitect.ai/pull/6373 last or as a
  conflict-aware support merge. It is currently the cleanest split but is not a
  substitute for #6370 passing.

https://github.com/jleechanorg/worldarchitect.ai/pull/6357 and
https://github.com/jleechanorg/worldarchitect.ai/pull/6367 remain useful
evidence/source branches, but they should not displace the #6370-#6373 landing
stack.

## Why this took weeks

1. Firestore-style string booleans made raw truthiness unsafe for level-up flags.
2. False behavioral-equivalence assumptions between `rewards_engine.py` and
   `world_logic.py` hid stateful modal/stale/projection behavior still living in
   `world_logic.py`.
3. Streaming vs polling vs MCP paths had different response shapes, so fixes on
   one path did not prove the others.
4. Multi-agent and multi-PR drift produced overlapping branches, closed PRs
   before landing, and split/rebase churn.
5. Evidence gates (skeptic, self-hosted CI, design-doc checks, real server/LLM
   repros, video/evidence bundles) correctly slowed merges.
6. This was a bug family, not a single bug: stale flags, story stripping, XP
   desync, resolver cascade, canonicalization, passthrough, and completed
   level-up projection all interacted.

## Artifacts

- Central tracker: `/Users/jleechan/roadmap/2026-04-18-level-up-central-tracker.md`.
- Learning log: `/Users/jleechan/roadmap/learnings-2026-04.md`.
- Claude memory: `/Users/jleechan/.claude/projects/-Users-jleechan-worldarchitect.ai/memory/project_2026-04-18_levelup_why_hard_on_track.md`.
- Canonical bead: `rev-7vyc`.

## Next actions

1. Finish https://github.com/jleechanorg/worldarchitect.ai/pull/6370 first:
   pending checks, review/Cursor issues, skeptic/7-green, and port-audit against
   the closed broad branches.
2. Then finish https://github.com/jleechanorg/worldarchitect.ai/pull/6371.
3. Then use https://github.com/jleechanorg/worldarchitect.ai/pull/6372 and
   https://github.com/jleechanorg/worldarchitect.ai/pull/6373 to preserve repro,
   evidence, docs, beads, and wiki state.

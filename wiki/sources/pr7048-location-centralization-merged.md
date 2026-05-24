# PR #7048: Location centralization MERGED

**Source:** Claude session memory + PR #7048 history
**Ingested:** 2026-05-24

## Summary

PR https://github.com/jleechanorg/worldarchitect.ai/pull/7048
([antig] Consolidate location fields to centralized location_util) merged
2026-05-24T07:09:07Z as commit `25cee34d6ff9f966eb9ba190e40efbd6eec3a5b9`.

The PR raced PR #6896 which chose an incompatible canonical field
(`current_location_name`). #6896 merged first; #7048 resolved by taking
THEIRS on all touched files and keeping its own `location_util.py` as
additive scaffolding.

## Reusable patterns

1. **[[7-Green-Proof-Artifact]]** — The github-actions[bot] VERDICT comment
   with `<!-- skeptic-head-sha-XXX -->` marker is the binding proof.
2. **[[Competing-PR-Canonical-Field-Resolution]]** — Take THEIRS on every
   touched file when a competing PR with opposite canonical field wins the
   race.
3. **[[CI-Expansion-Surfaces-Latent-Failures]]** — Budget in-PR fixes for
   pre-existing failures that a CI-expansion commit exposes.
4. **[[Self-Hosted-Runner-Infra-Flake-vs-Real-Failure]]** — Check
   `check-runs/<id>/annotations` for "runner lost communication" before
   diagnosing as test failure.

## Verdict comments (proof)

- 2026-05-24T06:15:18Z for HEAD `7ea51b546c`
- 2026-05-24T06:26:10Z for HEAD `e979224079` — comment 4527601295

## Related sources

- [[PR-6896-Location-Inline-Resolve]] — competing PR
- [[Beads-Issue-Tracking]] — 22 beads closed in this session

## Affects [[jeffrey-oracle]]?
No — this is a technical workflow learning.

## Raw

- raw/pr7048-location-centralization-merged-summary.md

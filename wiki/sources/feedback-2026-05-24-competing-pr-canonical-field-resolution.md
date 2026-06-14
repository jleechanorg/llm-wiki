---
title: "When Competing PRs Choose Opposite Canonical Fields, the Later PR Must Take THEIRS Everywhere"
type: source
tags: [pr-workflow, merge-conflict, canonical-field, race-resolution, 7-green]
sources: []
last_updated: 2026-05-24
source_file: raw/feedback_2026-05-24_competing_pr_canonical_field_resolution.md
---

## Summary
When two PRs target the same architectural problem with opposite canonical field choices and one merges first, the loser PR must take THEIRS on every file the winner touched — including their tests. PR #7048 (location_util with `world_data.location` canonical) raced PR #6896 (inline `resolve_location` with `world_data.current_location_name` canonical); #6896 merged first, so #7048 took THEIRS on all 6 affected files and kept `location_util.py` as additive scaffolding.

## Key Claims
- Race-resolution pattern when taking merge of `origin/main` and conflicts surface in files touching the same architectural decision the loser-PR designed around: **take THEIRS for ALL of those files**, including their tests.
- Picking OURS on any location-touching file after the winner merged would re-introduce a write to the wrong canonical field while the rest of `main` reads the right one — every downstream consumer would break silently.
- Identify dead artifacts the loser-PR created (e.g. `location_util.py` had zero callers after taking THEIRS for 6 files). Decide explicitly: delete OR keep as scaffolding. Document the choice.
- Add only **additive** changes on top of THEIRS — these don't fight the canonical. Tests must match production: if you take THEIRS on production, take THEIRS on the matching test file too (signature mismatch otherwise).
- Concrete files this session (took THEIRS): `mvp_site/agent_prompts.py`, `mvp_site/context_compaction.py`, `mvp_site/llm_parser.py`, `mvp_site/llm_service.py`, `mvp_site/preventive_guards.py`, `mvp_site/tests/test_preventive_guards.py`. Kept OURS only on `testing_mcp/schema/test_schema_migration_flow_real_api.py` (defensive dict check) and `.gitattributes` initially (later re-took THEIRS on CR feedback — AGENTS.md:174 explicitly pins `merge=beads`).

## Key Quotes
> "When taking a merge of `origin/main` and conflicts surface in files that touch the same architectural decision the loser-PR designed around, **take THEIRS for ALL of those files**, including their tests." — feedback_2026-05-24_competing_pr_canonical_field_resolution

> "Picking OURS on any location-touching file after #6896 merged would have re-introduced a write to `world_data.location` while the rest of `main` (deployed) reads `current_location_name`. Every downstream consumer would have broken silently." — feedback_2026-05-24_competing_pr_canonical_field_resolution

## Connections
- [[7-Green-Proof-Artifact]] — PR #7048 reached 7-green by following this resolution
- [[PR-7048-Location-Centralization-Merged]] — the loser PR in this race
- [[PR-6896-Location-Inline-Resolve]] — the winner PR
- [[Competing-PR-Subsumption-Close-Subset]] — sibling concept (close-subset variant)

---
name: evidence-sha-staleness-13-files
description: Evidence SHA at a0b5c877 is stale — 13 mvp_site/ files changed by df433f84; fresh /es run required before merge
type: feedback
bead: none
---

## Rule

**Evidence is only valid for the exact commit SHA at which it was recorded. Any `mvp_site/` change after the evidence SHA invalidates Gate 6.**

Verification command before claiming Gate 6 pass:
```bash
git diff <evidence_sha>..HEAD -- mvp_site/
```
If this is non-empty, evidence is stale. Do not claim Gate 6 passes.

## Context — PR #7142

| Item | Value |
|---|---|
| Evidence SHA | `a0b5c87780` (iteration_013) |
| Current HEAD at session | `df433f84de` |
| Files changed between | 13 files (+331/−135) |

Key files that changed after evidence was recorded:
- `mvp_site/world_logic.py` (+102/−102)
- `mvp_site/prompts/level_up_instruction.md` (+104 lines)
- `mvp_site/agents.py` (−6 lines)
- Multiple prompt files, schema, backend adjustment registry, tests

## How to Apply

- When reporting PR status on any PR that has had commits since the last `/es` run, always compute `git diff <evidence_sha>..HEAD -- mvp_site/ | wc -l`.
- If non-zero: state "Evidence stale — N lines changed in mvp_site/ since evidence SHA; fresh /es run required."
- Do not claim evidence passes Gate 6 based on the iteration number alone.

## PR Body Update

Added explicit stale warning to evidence section of PR #7142 body:
> ⚠️ **Evidence stale** — 13 `mvp_site/` files changed since `a0b5c87780`; fresh `/es` run required at current HEAD before merge

## References

- PR [#7142](https://github.com/jleechanorg/worldarchitect.ai/pull/7142)
- CR comment: https://github.com/jleechanorg/worldarchitect.ai/pull/7142#issuecomment-4571810409
- [[feedback_2026-05-28_gate_es_sha_binding]]

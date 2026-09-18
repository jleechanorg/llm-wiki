---
title: "world_logic.py LOC ratchet hit by legit fix; relocate to owning module, not a ratchet bump"
type: source
tags: [worldarchitect.ai, ci, loc-ratchet, refactor, code-review, wizard]
date: 2026-09-17
source_file: raw/feedback_2026-09-17_worldlogic_loc_ratchet_hit_by_legit_fix_relocate_not_bump.md
---

## Summary
Landing PR #9913 (jleechanorg/worldarchitect.ai, bead rev-n8roa — wizard IP
fields silently dropped on a Dragon Knight campaign fallback) took three
rounds of independent review, each surfacing a real follow-on bug rather than
a false positive. The cumulative small code additions to
`mvp_site/world_logic.py` then tripped the repo's CI-enforced whole-file LOC
ratchet. The fix was to relocate the new logic into the helper module that
already owned the function needing it, not to bump the ratchet number.

## Key Claims
- `world_logic.py` carries a CI-enforced upper-bound LOC ratchet
  (`<=12681` lines, `design-doc-gate.yml`'s "world_logic.py line count" gate)
  that a prior session had tightened via a real refactor from 12699.
- A legitimate, root-cause-correct bug fix can still trip this ratchet if it
  needs even a modest amount of new logic plus explanatory comments.
- The correct response when this happens is to check whether the new logic
  belongs in a helper module `world_logic.py` already imports from, and move
  it there (here: `mvp_site/prompt_utils.py`, which already owned
  `stamp_wizard_intake_answers()`) — not to bump the ratchet number.
- Watch for import-cycle risk when moving logic the other direction across
  an existing one-way import relationship; a deferred (in-function-body)
  import breaks the cycle without a module-level circular import.
- Three independently-run reviewers (cursor-agent as an `/advice` A3
  fallback, Gemini, and ChatGPT via `/wa`) each independently found the
  exact same subtle ordering bug (a match-classification computed before vs.
  after a prompt-rewrite block) without being told what the others found —
  unprompted multi-reviewer convergence on the same specific finding is
  strong confirmation signal.

## Key Quotes
> "A legit bug fix can still trip a repo-wide LOC ratchet — the correct
> response is to relocate logic to the owning module, not to bump the
> ratchet."

## Connections
- [[DesignDocGate]] — the CI workflow whose LOC-count gate this hit
- [[WorldLogicPy]] — the file the ratchet applies to
- [[EvidenceStandardsSkill]] — governs the evidence gist published for this PR

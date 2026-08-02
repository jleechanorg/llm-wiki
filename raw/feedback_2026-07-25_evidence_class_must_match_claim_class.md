---
name: evidence-class-must-match-claim-class
description: four adversarial document-review rounds all scored WITH-GAPS on a user-story spec; checking claims against real campaign transcripts found four FALSE documented claims a document review structurally cannot catch — count behavioral vs static acceptance criteria before trusting a docset
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bc3b0c3b-7695-40fc-916d-e83f512181b9
  modified: 2026-07-26T06:25:16.602Z
---

**THE BIG ONE from the 2026-07-25 session.** A visual/user-story spec was audited FOUR times adversarially and scored WITH-GAPS each time — but all four rounds reviewed *documents*, never the product. When claims were finally checked against 2,141 scenes of real campaign transcripts, FOUR documented claims were simply **false**:
- A "Gold never updates" gap — actually Gold takes 6 distinct values, 75→7495 GP, across the transcripts.
- A checkpoint cadence claimed "~every 10 scenes" — actually 489 of 490.
- An injury-behavior claim — actually 0/400 and 1/697 player HP losses in the sampled scenes.
- A FALSE DISCLAIMER stating a time contradiction was "not observed" — it IS observed, at scenes 458 and 466.

Document review structurally cannot catch a well-formed, internally-consistent claim that is simply untrue about the product — no amount of re-reading the doc surfaces it, because the doc is self-consistent. Only checking against real transcripts/logs does.

**Measured root cause:** 73 of 109 stories had BEHAVIORAL acceptance criteria (streaming, transitions, cross-scene consistency) that no still frame or document read can settle. The docset had proven roughly a third of itself (the static-frame-checkable third) and asserted the rest without ever producing behavioral evidence for it.

**How to apply — the cheap check that would have caught it:** Before trusting any evidence docset or audit result, count how many acceptance criteria are BEHAVIORAL (require observing change over time/sequence — streaming, transitions, state deltas across turns) vs STATIC (settleable from one frame/one document read). Then ask explicitly: do we have ANY evidence of the behavioral class? If the answer is "we only reviewed documents" or "we only have single-frame screenshots," the audit is unproven for that fraction regardless of how many review rounds it survived. This generalizes the repo's existing "Unit-only proof is NOT sufficient" rule (`~/.claude/CLAUDE.md`) — same failure shape, different artifact type (docs vs tests).

Related: [[feedback_2026-07-25_verify_different_layer_than_claim_layer]], [[feedback_2026-07-25_grep_false_negative_is_systemic_not_occasional]]. The `/user-story` skill (`~/.claude/skills/user-story/SKILL.md`) was patched from 59→72 lines this session with 12 rules, 11 traced to specific failures observed in this run (reviews at `/Users/jleechan/projects/wa_worktree_uistories/docs/user-stories-ui/reviews/`).

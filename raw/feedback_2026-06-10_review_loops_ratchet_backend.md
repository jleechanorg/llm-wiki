---
name: review-loops-ratchet-backend
description: "Review loops structurally ratchet backend-ward — bots suggest code-shaped fixes, no gate demands subtraction; review-response is NOT an RCF exemption; reducer/state-machine guards ARE adjusters and must be registered"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1fe8f3f-4d95-42f6-92c4-4a7a1018530c
---

User /harness escalation (2026-06-10): "how did we violate /code-standards so badly?" — the level-up state-machine train accumulated unregistered backend guards, coexisted with the banned XP-threshold override (`rewards_engine.py:2388` "Overriding level_up to false", no log_reason_code), and never shipped the deletion PR (PR 6, rev-37xca), despite ZFC/RCF rules in every instruction layer.

**Why:** the merge pipeline's gates (CI, CodeRabbit, Bugbot, skeptic 8-gate, evidence) are all ADDITIVE forces — review bots analyze the code diff and suggest code-shaped fixes; nothing gates on ZFC/net-LOC/registration. Each review round's guard was locally approved ("review-response scope"); the trajectory compounded into globally-banned architecture. I (team-lead) authorized backend guards with the words "review-response scope, approved" — the live demonstration.

**Why (registry bypass):** the backend adjustment registry (63 specs, graduation policy) was followed by the previous adjuster generation, but the train's reducer guards were framed as "canonical state machine architecture" not "adjustments" — same semantics (suppress/demote/override model-owned signals), different label, zero registrations. Relabeling loophole.

**How to apply:**
1. Review-response is NOT an RCF exemption — any reviewer-suggested backend guard on model-owned output requires the prompt-first analysis in the thread reply before implementation.
2. The registry rule applies to ANY code modifying model-owned output regardless of framing (adjuster, guard, invariant, reducer, state machine).
3. Pipelines need a SUBTRACTIVE gate: /code_standards (ZFC+leveling+RCF) as a skeptic gate; net-LOC trend gates on migration PR chains.
4. A migration without its deletion PR shipped is an accretion — track the deletion as a first-class deliverable, not a plan item.
Related: [[stacked-pr-single-writer-rule]], [[optimization-baseline-fidelity]]. Fixes landed via harness PR 2026-06-10 (design-doc-gate greps + skeptic Gate 9 + repo CLAUDE.md rules + threshold-override AdjustmentSpec).

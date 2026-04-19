---
title: "Bug Classification"
type: concept
tags: [debugging, methodology, level-up, triage]
---

## Definition

The practice of exhaustively mapping all distinct failure modes of a system before writing any fix code. Each class gets a name, a root cause, a decision-tree path, and required evidence type.

## Why Classification First

Writing a fix before mapping all classes leads to:
- Fix addresses Class A, but Classes B-G remain hidden
- Each new class discovered post-fix requires another round of live repros
- Fix branches accumulate partial fixes, creating merge conflicts
- Evidence bundles become inconsistent across classes

**From the level-up post-mortem**: 7 distinct failure classes (A-G) required 8 real-campaign repros to fully map before any fix code was written. Fixing prematurely would have repeated this cycle for each undiscovered class.

## Classification Protocol

1. **Reproduce first** — get a live repro before classifying
2. **Name the class** — `Class A`, `Class B`, etc. with a one-line descriptor
3. **Map the root mechanism** — the exact code path that fails, not symptoms
4. **Build a decision tree** — so any new repro can be triaged to a class in <5 minutes
5. **Estimate fix independence** — are Classes B and C the same root? Can they share a fix?
6. **Only then write fix code** — one PR per class or per shared-root group

## Level-Up Bug Classes (Example)

| Class | Root Mechanism |
|---|---|
| A/C | `_extract_xp_robust` returned 0 for `experience.current` key |
| B | `level_up_complete=True` treated as stale by polling path → cascade |
| D/E | Streaming passthrough stripped rewards_box via `_canonicalize_core` |
| F | `level_up_pending=False` stale flag blocks modal before XP check |
| G | `source=milestone` rewards_box missing `new_level`; normalization skips synthesis |

## Decision Tree Pattern

```
rewards_box shown? ─── No ──┬── level_up_pending=False? ── Yes → Class F
                             ├── level_up_complete=True? ─── Yes → Class B
                             ├── source=milestone, no new_level? → Class G
                             ├── experience.current=0? ────────── Yes → Class A/C
                             └── streaming path, rewards_box null? → Class D/E
```

## Connections

- [[LevelUpBugFixPostMortem20260418]] — 7 classes required full mapping before fix
- [[FirestoreSerializationTrap]] — root cause of multiple classes
- [[TrunkBasedDevelopment]] — one PR per class = small diffs = faster review
- [[AgentDrift]] — agents spawned without class context drift to wrong fixes

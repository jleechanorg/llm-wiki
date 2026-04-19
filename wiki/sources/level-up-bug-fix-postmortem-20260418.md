---
title: "Level-Up Bug Fix Post-Mortem 2026-04-18"
type: source
tags: [level-up, rewards, post-mortem, agent-drift, firestore, ci-review-churn]
last_updated: 2026-04-18
source_file: learnings/level-up-postmortem-20260418
---

## Summary

A bug fix that amounted to ~20 lines of production code across `agents.py`, `world_logic.py`, and `rewards_engine.py` took several weeks to land. The root cause was not technical complexity alone — it was a compounding of Firestore serialization traps, 7 distinct failure classes requiring live-campaign repros to map, CodeRabbit review churn on every push, strict evidence standards with a WARN-FINAL ceiling for historical captures, agent drift from PR-number anchoring, and worktree/branch hygiene debt.

## Key Claims

- Firestore serializes Python `False` as string `"false"` — truthy in a plain `if val:` check — and unit tests using real Python bools never caught it
- 7 distinct failure classes (A-G) required 8 real-campaign repros (12+ campaign instances per run, 15-30 min each with live LLM calls) to fully map before any fix could be written
- CodeRabbit re-reviews the full diff on every push; an 800-line PR generates 15-20 new review threads per push, creating a fix-push-new-threads loop that compounds
- Evidence standards require streaming proof, video, bundles at canonical paths, and `/er` verdict — WARN-FINAL is the practical ceiling for historical repros (3 structural gaps unresolvable retroactively)
- 13 of 29 post-roadmap PRs drifted from intended scope because agents were anchored to PR numbers without bead/design-doc context
- At peak: 26 open PRs, 4+ active worktrees pointing at different heads, local branches stale by 100+ commits vs remote
- The split into 4 PRs (#6370-#6373) to reduce CR surface area created 7 merge-conflict pairs across the split branches

## Key Quotes

> "The fix was always small. The overhead was in discovery, verification, and coordination." — session post-mortem

> "Classify bugs before writing fix code. You can't fix what you haven't mapped." — lesson learned

> "Never anchor agents to PR numbers without bead/design-doc context." — agent drift root cause

## Connections

- [[FirestoreSerializationTrap]] — core technical root cause affecting all level-up flags
- [[CodeRabbitReviewChurn]] — process root cause; re-reviews full diff on every push
- [[AgentDrift]] — 13/29 PRs drifted; PR-number anchoring without bead context
- [[EvidenceStandards]] — WARN-FINAL ceiling for historical repros
- [[TrunkBasedDevelopment]] — lesson: small diffs + trunk-based = faster review cycle
- [[BugClassification]] — lesson: map all classes before writing fix code

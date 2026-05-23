---
title: "worldarchitect.ai — Multi-Wiki Status"
type: concept
tags: [worldarchitect.ai, wiki, public-wiki, private-wiki, firestore]
sources: []
last_updated: 2026-04-13
---

# worldarchitect.ai — Multi-Wiki Status

## 1. Public Wiki — ~/worldarchitect-public-wiki/ (220K)

| Subdirectory | Contents |
|---|---|
| `concepts/` | 14 D&D 5e mechanic pages (AbilityScores, AdvantageDisadvantage, AttackRoll, Attunement, CharacterCreation, DiceRollMechanics, DiceStrategy, Feats, HitPoints, Initiative, LevelProgression, ProficiencyBonus, SavingThrow, SkillChecks, Spellcasting) |
| `entities/` | 2 entity pages (CelestialImperium, WorldOfAssiah, Campaign NPCs) |
| `tips/` | 6 tips pages (campaign-creation, dice, level-up, npc-design, social-hp, story-structure) |
| `index.md` | Index with Overview + Tips + Concepts + Entities sections |

**Status**: Mostly static content. No campaign-specific pages, no MCP integration.

---

## 2. Private Wiki — ~/worldarchitect-private-wiki/ (16K)

| Subdirectory | Contents |
|---|---|
| `beads/` | README.md stub |
| `failed-experiments/` | README.md stub |
| `harness/` | README.md stub |
| `oracle/` | Empty directory |
| `README.md` | Notes that worldai MCP is NOT CONFIGURED |

**Status**: Skeleton only. All subdirectories are empty stubs except READMEs.

---

## 3. Main Wiki — /Users/jleechan/llm_wiki/wiki/ (202M)

| Subdirectory | Count |
|---|---|
| `sources/` | 27,613 |
| `entities/` | 2,189 |
| `concepts/` | 1,415 |
| `campaigns/` | 1 subdirectory (`jleechan/`) |
| `syntheses/` | existing |
| `overview.md`, `index.md`, `log.md` | present |

**Status**: Massive wiki with 67+ ingested campaigns. Primary workspace.

---

## 4. Campaign Query via worldai MCP — BLOCKED

**MCP ERROR** — Firestore composite index missing. Query attempted:
```
collection_group: campaigns
filters: user_id == "jleechan@gmail.com", scene_count > 300
```
Error: `400 The query requires an index. You can create it here: ...`

Second attempt (user_id only) also failed — also requires an index.

**Result**: Cannot enumerate high-scene campaigns via MCP without first creating a Firestore composite index on `(user_id, scene_count)` or `(user_id)` in the `campaigns` collection.

---

## Summary

| Wiki | Size | Status |
|---|---|---|
| Public | 220K | Static D&D content, no campaigns |
| Private | 16K | Empty stubs |
| Main (llm_wiki) | 202M | 67 campaigns, primary workspace |
| worldai MCP | — | BLOCKED — needs Firestore index |

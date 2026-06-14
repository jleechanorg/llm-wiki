---
title: "2026-06-13 Levelup V2 Pra Fullsheet I4 Closure"
type: source
tags: ["project", "worldarchitect", "level-up"]
date: 2026-06-13
source_file: raw/project_2026-06-13_levelup_v2_pra_fullsheet_i4_closure.md
---

## Summary
Level-up v2 PR-A (#7528) full-sheet gate — the real failing gate was I4 (cumulative features vs list-replace merge), fixed at prompt+test layer

## Key Claims
- PR #7528 (feat/levelup-v2-prompt-full-sheet) "M-A full-sheet mandate" looked fully
- GREEN (10/10 contract, real-LLM PASS, Evidence Gate SUCCESS) but the genuine failing
- gate was **I4**, diagnosed in this lane's own `.dark-factory/explore-risks.md` (top
- finding + invariant I4 + patch-trap PT1):
- - `firestore_service._deep_merge` (firestore_service.py:4244-4270) REPLACES lists
- wholesale; `player_character_data.features` is a list. Conclude item 3 said "list

## Connections
- [[feedback_2026-06-12_generic_prompt_fixes]]
- [[project_2026-06-11_nfbaxq3_level6_bug_root_cause]]

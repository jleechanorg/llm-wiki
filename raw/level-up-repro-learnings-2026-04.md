---
title: "Level-up repro learnings (VaD8, organic recon, five-class suite)"
type: source
tags: [repro, level-up, normalization-atomicity, firestore, testing_mcp]
date: 2026-04-21
source_file: wiki/sources/level-up-repro-learnings-2026-04.md
---

## Summary

Production campaign **VaD8mJSMNd9KlylPQIAj** showed a **mixed atomicity** state: the latest **story** entry carried **`rewards_box.level_up_available`** and **narrative** planning choices, while **`game_states/current_state`** had **`rewards_box: null`**, a **god-mode-style** planning line, and **`custom_campaign_state.level_up_pending` ≠ `player_character_data.level_up_pending`**. The repeatable script **`scripts/recon_organic_level_up.py`** clones from source, runs a **`GOD MODE:`** accelerated-leveling line, then an **organic** character turn; it reproduces the **pending-flag split** on fresh clones. The five-class **`testing_mcp/test_level_up_class_*.py`** harnesses target **RED** evidence (`REPRODUCED`, strip signatures, residue); **non-zero suite exit** often means **bugs were observed**, not that the harness crashed.

## Key claims

- **MCP `get_campaign_state` / bundle snapshots** may **omit `story[].rewards_box`** even when Firestore has it — use **Admin reads** for ground truth on story rows.
- **`repro_copy_campaign.py`** two-copy replay **advances** state; **`pre`** snapshots preserve the mismatch for audit.
- **Green Gate** can pass **gates 1–5** while the workflow **fails** on **no `VERDICT: PASS`** for the head SHA (gate 7).

## Connections

- [[NormalizationAtomicity]] — pairing contract for rewards vs planning and pending flags.
- [[ReproCopyCampaignProcedure]] — evidence bundle layout and PASS vs REPRODUCED semantics.

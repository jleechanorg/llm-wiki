---
title: "mvp_site resources"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/resources.py
---

## Summary
Resource calculation formulas for WorldAI Faction Management. Implements exact formulas for citizens growth, gold income, arcana yield, building construction rates, and unit recruitment rates.

## Key Claims
- calculate_citizen_growth() formula: 50 + 0.015 * current_citizens, tapers at 90-100% capacity
- calculate_gold_income() calculates gold pieces income per turn based on buildings
- calculate_arcana_yield() calculates arcane income based on mana-related buildings
- calculate_building_cost() and calculate_building_gold_cost() for building construction rates

## Connections
- [[FactionMinigame]] — resource calculation formulas
- [[CombatSystem]] — unit recruitment rates
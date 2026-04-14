---
title: "mvp_site intel"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/intel.py
---

## Summary
Intel operations for WorldAI Faction Management implementing spy deployment/detection formulas and intel success tiers. Provides calculation functions for detection risk, intel gathering, and success tier classification.

## Key Claims
- IntelTier enum: FAILURE, PARTIAL, SUCCESS, CRITICAL
- calculate_detection_risk() formula: base 30% + shadow_networks*2% + wards*5% - spies*1% - spymaster_mod*2% - lineage_intrigue*3%
- Risk clamped between 5% and 90%
- IntelResult TypedDict with tier, detected, intel_gathered, message

## Connections
- [[FactionMinigame]] — intel/spy operations in faction management

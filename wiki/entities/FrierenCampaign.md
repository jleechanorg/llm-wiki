---
title: "FrierenCampaign"
type: entity
tags: [worldarchitect-ai, campaign, bug-repro]
date: 2026-04-30
---

## Overview

TTRPG campaign using the Frieren setting on WorldArchitect.AI. The primary campaign `7IobpFpcOcibSyJ1pI5h` (Frieren v1) was the subject of a bug investigation where a stale `rewards_box` with `xp_gained=2300` persisted across turns.

## Key Properties

- **Campaign ID**: `7IobpFpcOcibSyJ1pI5h` (jleechan@gmail.com)
- **Twin copy for repro**: `vPZUnBAKMDsbN3HS95wF` (jleechantest user, campaign `0wf6sCREyLcgynidU5LjyZEfm7D2`)
- **Baseline copy**: `dUzgmHXlWOeFsOfaz9Ei`
- **Bug**: Stale `xp_gained=2300` in Firestore `structured_fields` from a bugged XP calculation; rendered on every page load via `should_show_rewards_box()`
- **LLM acknowledgment**: LLM acknowledged error in narrative text ("State Cleanup: Deleted the erroneous 'rewards_box' object...") but prose does not write Firestore

## Connections

- [[RewardsBoxDismissalGap]] — this campaign is the repro subject
- [[Frieren]] — campaign setting
- [[CampaignUpgrade]] — related WorldArchitect campaign system

---
title: "Resistance Shown"
type: concept
tags: [social-hp, game-state, field, prompt]
sources: ["social-hp-enforcement-reminder-tests"]
last_updated: 2026-04-08
---

## Definition
A boolean field in the game state that tracks whether resistance has been shown/displayed during a social encounter.

## Usage
Used by the SOCIAL_HP_ENFORCEMENT_REMINDER to track whether the NPC has demonstrated resistance to the player's social approach. The field is referenced when enforcing social HP mechanics.

## Related Concepts
- [[SocialHPChallenge]] — the broader social HP challenge system
- [[RequestSeverity]] — companion field tracking request severity
- [[GameStateInstruction]] — prompt file that documents these fields

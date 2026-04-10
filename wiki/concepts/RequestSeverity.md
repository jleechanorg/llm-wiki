---
title: "Request Severity"
type: concept
tags: [social-hp, game-state, field, prompt]
sources: ["social-hp-enforcement-reminder-tests", "social-hp-challenge-schema-derived-enums-tests"]
last_updated: 2026-04-08
---

## Definition
A field in the game state that tracks the severity level of a social encounter request. Normalized to lowercase values (e.g., "submission", "challenge", "demand").

## Usage
Used by the SOCIAL_HP_ENFORCEMENT_REMINDER to dynamically insert the request severity value when prompting the LLM about social HP challenges.

## Related Concepts
- [[SocialHPChallenge]] — the broader social HP challenge system
- [[ResistanceShown]] — companion field tracking resistance display
- [[GameStateInstruction]] — prompt file that documents these fields

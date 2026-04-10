---
title: "Social HP Enforcement Reminder"
type: concept
tags: [prompts, social-hp, agent-prompts, enforcement]
sources: ["social-hp-enforcement-reminder-tests"]
last_updated: 2026-04-08
---

## Definition
A prompt reminder constant (`SOCIAL_HP_ENFORCEMENT_REMINDER`) in the mvp_site.agent_prompts module that is injected into LLM prompts to enforce social HP challenge mechanics.

## Key Components
- **REQUEST SEVERITY**: Placeholder for dynamic request severity value
- **request_severity**: Field reference for tracking severity
- **resistance_shown**: Field reference for tracking resistance display
- **PROGRESS MECHANICS**: Section for mechanics updates

## Usage
Injected into prompts to remind the LLM to enforce social HP rules, track request severity levels, and monitor resistance shown during encounters.

## Related Concepts
- [[RequestSeverity]] — the severity field it references
- [[ResistanceShown]] — the resistance field it references
- [[SocialHPChallenge]] — the broader system this reminder enforces

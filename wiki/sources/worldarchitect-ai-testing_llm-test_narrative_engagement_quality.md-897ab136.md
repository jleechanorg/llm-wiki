---
title: "Narrative Engagement Quality Cross-Validation"
type: source
tags: [worldarchitect-ai, testing, narrative-quality, multi-LLM, engagement, D&D]
sources: []
date: 2026-04-07
source_file: raw/test-narrative-engagement-quality.md
last_updated: 2026-04-07
---

## Summary
Multi-model assessment protocol for evaluating AI-generated narrative responses in D&D scenarios. Tests engagement, appropriateness, and story progression across five scenario types (combat, social, exploration, puzzle, horror). Uses Claude, GPT-4, and Gemini as cross-validators to catch "technically correct but boring/inappropriate" responses that damage user engagement.

## Key Claims
- **Test Matrix**: Five scenario types each with specific quality dimensions and minimum thresholds (avg ≥7.5 required)
- **Multi-LLM Evaluation**: Claude assesses engagement, GPT-4 evaluates technical quality, Gemini provides self-assessment
- **Cross-Validation**: Aggregates scores, identifies consensus issues (2+ models flag same problem), flags high-disagreement cases (>3 point spread)
- **PASS Criteria**: Average ≥7.5, no dimension <6.0, models agree within 2-point range
- **FAIL Indicators**: Any dimension <5.0, average <7.0, disagreement >3 points, player agency violations

## Key Quotes
> "This test catches the 'technically correct but boring/inappropriate' responses that kill user engagement."

## Quality Issue Categories
- **Generic Responses**: "You swing your sword and hit for damage"
- **Over-Description**: Purple prose that slows gameplay
- **Player Agency Violation**: "You decide to..." or railroading
- **Tone Inconsistency**: Modern language in fantasy setting
- **Rule Confusion**: Incorrect mechanics or impossibilities

## Root Causes
- Prompt Design: System prompts may not emphasize engagement
- Model Selection: Gemini variant might not be optimal for creative writing
- Context Management: Important story elements getting lost
- Temperature Settings: Too low (boring) or too high (incoherent)

## Connections
- [[WorldArchitect.AI]] — platform this test validates
- [[Game State Logical Consistency Validation Test]] — complementary test for game state
- [[LLM Capability Mapping]] — broader LLM testing framework

## Contradictions
- None identified yet

---
title: "Proof Of Work"
type: concept
tags: [PR-quality, evidence, visual-validation, AI-workflow]
sources: [openai-harness-ryan-notes]
last_updated: 2026-04-08
---

## Definition

A mandatory standard where AI agents cannot submit code without proving the code functions as intended. Transforms human role from line-by-line syntax checker to high-level product reviewer.

## The Standard

Agents must attach screenshots or video evidence of the feature working:
- Screenshots showing the implemented feature
- Video of headless browser executing the feature
- Visual proof of UI components and interactions

## Implementation

GitHub PR Media Skill:
- Initially worked only with images
- Evolved to video capture using ffmpeg
- Agent invokes skill when creating PR
- Attaches proof to PR automatically

## Why It Matters

1. **Trust**: Establishes trust without "shoulder surfing"
2. **High-Level Review**: Human evaluates the attached evidence
3. **Specific Feedback**: Human can point to visual bugs ("button overlapping text")
4. **Efficiency**: Natural interface for reviewing agent work

## Quote

> "I'm not shoulder surfing them to see what they're typing. I'm expecting that they did the job and that they can prove to me that the code is worth merging."

## Connection to Other Concepts

- [[DualAgentArchitecture]] - Work produced by Generator, validated by Reviewer
- [[MinimalReproLadder]] - Tests as deterministic proof
- [[HarnessEngineering]] - Part of overall quality harness

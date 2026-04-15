---
title: "Voyager"
type: entity
tags: [minecraft-agent, skill-library, iterative-prompting, research]
date: 2026-04-15
---

## Overview

Voyager is a Minecraft agent (Guanzhi Wang et al., arXiv:2305.16291) with a three-component architecture: Automatic Curriculum, Skill Library, and Iterative Prompting. It uses GPT-4 as a critic for self-verification.

## Key Properties

- **Architecture**: Three-component system — Automatic Curriculum, Skill Library, Iterative Prompting
- **Paper**: arXiv:2305.16291 (May 2023, revised Oct 2023)
- **Key features**:
  - Automatic Curriculum: GPT-4 generates progressive challenges based on agent state
  - Skill Library: Executable code behaviors indexed by description embeddings
  - Iterative Prompting: Environment feedback + execution errors + self-verification
- **Verification**: "By providing the agent's current state and the task to GPT-4, we ask it to act as a critic"
- **Performance**: 3.3x more items, 2.3x distance, 15.3x faster milestones vs prior SOTA
- **Uses GPT-4 as blackbox** via prompting (no fine-tuning)

## Connections

- [[SelfDebugging]] — Voyager uses GPT-4 as a critic for self-verification
- [[SkillLibrary]] — skill library retrieval pattern (embedding-based code retrieval)
- [[IterativePrompting]] — iterative prompting with multiple feedback types
- [[MetaGPT]] — cited together in research; both use GPT-4 for criticism
- [[OpenHands]] — both use skill library retrieval patterns

## See Also
- [[SelfDebugging]]
- [[SkillLibrary]]
- [[IterativePrompting]]

---
title: "Constitutional AI"
type: entity
tags: [alignment, safety, constitutional-classifiers, rlaif, anthropic]
date: 2026-04-15
---

## Overview

Constitutional AI (Anthropic) is a training approach for harmless AI via self-improvement with minimal human oversight. It uses chain-of-thought reasoning for transparency and non-evasive harmlessness (explaining objections rather than refusing).

## Key Properties

- **Two-phase training**:
  1. Supervised Learning (SL): Sample → self-critique → revise → finetune
  2. Reinforcement Learning (RL/RLAIF): AI preference model as reward signal
- **Key innovations**:
  - Chain-of-thought reasoning for transparency
  - Non-evasive harmlessness (explains objections rather than refusing)
  - Reduced labeling burden via AI feedback
- **Constitutional Classifiers**: "Filtered overwhelming majority of jailbreaks" — "withstood over 3,000 hours of red teaming with no universal jailbreak discovered"
- **Published alongside**: Constitutional AI Policy Memo

## Connections

- [[RLAIF]] — Constitutional AI uses RLAIF in its RL phase
- [[ConstitutionalClassifiers]] — production deployment of constitutional AI principles
- [[AnthropicAlignment]] — Constitutional AI is part of Anthropic's alignment research
- [[GovernanceLayer]] — Constitutional AI principles can inform governance constraint design
- [[Anthropic]] — Constitutional AI was developed by Anthropic

## See Also
- [[RLAIF]]
- [[ConstitutionalClassifiers]]
- [[AnthropicAlignment]]

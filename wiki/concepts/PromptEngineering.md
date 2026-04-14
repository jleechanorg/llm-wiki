---
title: "Prompt Engineering"
type: concept
tags: [prompting, few-shot, chain-of-thought, system-prompts]
sources: [external-ai-knowledge-sources]
last_updated: 2026-04-14
---

## Summary

Prompt engineering is the practice of structuring inputs to reliably steer model behavior. It spans system prompt design, few-shot example selection, chain-of-thought scaffolding, and output format control. In 2026, it remains the fastest way to improve model performance without retraining.

## Key Claims

- Chain-of-thought prompting (CoT) consistently improves reasoning on multi-step problems. Let the model think step by step before answering.
- Few-shot examples outperform zero-shot instructions for complex tasks, but quality of examples matters more than quantity (3–5 well-chosen demos beats 20 random ones).
- System prompts set the model's role and behavior; they are the most leveraged part of prompting in production systems.
- Structured output (JSON, XML schemas) dramatically improves reliability of downstream parsing.

## Best Practices

- **Role and persona**: "You are an expert X..." consistently improves domain accuracy.
- **Explicit instruction ordering**: put the most important instruction last (recency effect in LLMs).
- **Avoid contradictory instructions** in system vs. user prompts.
- **Delimiter usage**: use clear separators (---, XML tags) between few-shot examples and the actual query.
- **Constraint framing**: instead of "don't do X", frame what TO do. Models respond better to positive instructions.
- **Temperature**: use temperature 0 for factual/retrieval tasks; 0.7–0.9 for creative; never above 0.9.

## Chain-of-Thought Variants

- **Zero-shot CoT**: "Let's think step by step" — works without examples
- **Self-consistency**: generate multiple reasoning paths, take majority vote
- **Tree-of-thought**: explore branching reasoning paths for complex planning
- **Program-of-thought**: generate executable code, run it, use result

## Connection to Claude API

The Anthropic Claude API supports system prompts, multi-turn conversation, and structured output via the `messages` API. Prompt caching (beta) can reduce cost for long system prompts reused across calls.

## Connections

- [[Claude API Best Practices]] — the API itself is how prompt engineering is operationalized
- [[RAG]] — prompts for RAG must instruct the model to cite and attribute retrieved context
- [[LLM Fine-Tuning]] — fine-tuning is often pursued when prompt engineering hits ceiling
- [[MetaHarness]] — Meta-Harness optimizes the harness code that includes prompts, demonstrating that infrastructure-level changes outperform prompt tuning alone
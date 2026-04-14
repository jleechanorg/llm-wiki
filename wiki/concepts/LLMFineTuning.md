---
title: "LLM Fine-Tuning"
type: concept
tags: [fine-tuning, LoRA, QLoRA, PEFT, training, domain-adaptation]
sources: [external-ai-knowledge-sources]
last_updated: 2026-04-14
---

## Summary

LLM fine-tuning adapts a pre-trained model to specific tasks or domains by continuing training on curated data. In 2026, parameter-efficient fine-tuning (PEFT) methods like LoRA and QLoRA have largely replaced full fine-tuning due to lower compute costs and comparable or better task performance.

## Key Claims

- **LoRA (Low-Rank Adaptation)** is the dominant fine-tuning method — it trains small rank-decomposition matrices alongside frozen pretrained weights, reducing trainable parameters by 100–1000x.
- **QLoRA** combines 4-bit quantization with LoRA, enabling fine-tuning of 65B+ models on a single 48GB GPU.
- Full fine-tuning is rarely justified now — catastrophic forgetting risk is high, and PEFT methods achieve 90%+ of the performance at <5% of the cost.
- Instruction fine-tuning datasets of 10K–100K examples are sufficient for most domain adaptation tasks.

## Fine-Tuning Types

- **Instruction fine-tuning**: trains model to follow instructions. Requires high-quality (instruction, response) pairs. Human preference data improves helpfulness.
- **Domain adaptation**: continue pretraining on domain-specific corpus to improve domain knowledge and vocabulary.
- **RLWF (Reinforcement Learning from Workflow)**: uses binary feedback on workflow steps rather than human preference comparisons.
- **DPO (Direct Preference Optimization)**: simpler alternative to RLHF that directly optimizes against preference pairs without reward modeling.

## Practical Workflow

1. Start with an instruction-tuned base model (e.g., Claude Instant or open-source like Llama 3-instruct).
2. Collect or curate domain-specific examples (100–10K depending on task).
3. Use Hugging Face `trl` library or `axolotl` for LoRA/DPO training.
4. Evaluate on held-out domain examples; iterate on data quality.
5. Merge LoRA weights into base model for deployment (or serve with LoRA adapters).

## When to Use Fine-Tuning vs RAG vs Prompt Engineering

| Approach | Best for | Not for |
|---|---|---|
| Prompt engineering | Quick improvements, format control | Consistent domain knowledge |
| RAG | Dynamic/updated knowledge, citations | Complex style/behavior adaptation |
| Fine-tuning | Task structure, domain jargon, style | Frequently changing knowledge |

## Connections

- [[RAG]] — fine-tuning and RAG are complementary; fine-tune for how to use context, RAG for what context to retrieve
- [[Prompt Engineering]] — prompt engineering often enough; fine-tuning is pursued when prompting hits ceiling
- [[RLHF]] — RLHF is a specialized fine-tuning technique using human preference data
---
title: "DeepSeek-Coder-V2"
type: concept
tags: [coding, MoE, efficient-inference, open-source]
sources: [deepseek-coder-v2-paper, deepseek-v2-paper]
last_updated: 2026-04-14
---

Mixture-of-Experts coding model: 236B total parameters, 21B activated per token. SOTA among open-source coding models. 128K context length. Key model used in Large Language Monkeys paper for SWE-bench evaluation.

## Key Specs

| Metric | Value |
|--------|-------|
| Total Parameters | 236B |
| Activated per Token | 21B |
| Context Length | 128K |
| Languages | 128+ |

## Key Architecture

- **Multi-head Latent Attention (MLA)**: 93.3% KV cache reduction
- **DeepSeekMoE**: fine-grained expert partitioning
- Extended code training on 2T+ tokens

## SWE-bench Results

- Single sample: 15.9%
- 250 samples (Large Language Monkeys): 56%

## Connections

- Key model for [[LargeLanguageMonkeys]] scaling study
- Related to [[DeepSeek-V2]] base architecture

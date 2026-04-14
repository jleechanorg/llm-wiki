---
title: "DeepSeek-Coder-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model"
type: paper
tags: [coding, MoE, efficient-inference, code-generation, open-source]
date: 2024-05-07
arxiv_url: https://arxiv.org/abs/2502.18627
---

## Summary
DeepSeek-Coder-V2 is a Mixture-of-Experts coding model with 236B total parameters and 21B activated per token. It extends the DeepSeek-V2 architecture specifically optimized for code tasks, achieving state-of-the-art performance among open-source coding models on benchmarks like HumanEval, MBPP, and SWE-bench. The model supports 128K context length and multiple programming languages.

## Key Claims
- **236B total parameters, 21B activated** per token
- **128K context length** for multi-file code understanding
- Achieves SOTA among open-source models on code benchmarks
- Strong performance on SWE-bench Lite (56% with 250 samples per Large Language Monkeys paper)
- Supports 128+ programming languages
- Competitive with GPT-4 Turbo on coding tasks

## Technique/Method
- DeepSeekMoE architecture with fine-grained expert partitioning
- Multi-head Latent Attention (MLA) for efficient long-context
- Extended code training on 2T+ tokens of code data
- Long context finetuning for 128K window
- Multi-language training across 128+ languages

## Results
- SOTA open-source coding performance on HumanEval, MBPP, LiveCodeBench
- Strong SWE-bench Lite results with repeated sampling
- Competitive with GPT-4 Turbo on various coding benchmarks
- Excellent long-context code understanding

## Limitations
- MoE training complexity and expert load balancing
- API availability and cost considerations
- Evaluation on newer benchmarks (post-training) may vary

## Connections
- Key model for SWE-bench evaluation (reference model in Large Language Monkeys paper)
- Relevant to coding agent backbone selection
- Supports efficient inference requirements for production coding systems

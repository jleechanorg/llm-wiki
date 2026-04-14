---
title: "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model"
type: paper
tags: [MoE, efficient-inference, coding, long-context, DeepSeek]
date: 2024-05-07
arxiv_url: https://arxiv.org/abs/2405.04434
---

## Summary
DeepSeek-V2 is a Mixture-of-Experts (MoE) language model with 236B total parameters and 21B activated per token. It uses Multi-head Latent Attention (MLA) and DeepSeekMoE architectures to achieve economical training and efficient inference. Pretrained on 8.1T tokens with SFT and RL applied. Achieves top-tier open-source performance with significantly reduced compute requirements.

## Key Claims
- **236B total parameters, 21B activated** per token
- **128K token context length**
- **42.5% training cost reduction** vs DeepSeek 67B
- **93.3% KV cache reduction** via MLA architecture
- **5.76x maximum generation throughput** improvement
- Achieves "top-tier performance among open-source models"
- Strong coding capabilities (used in Large Language Monkeys paper for SWE-bench results)

## Technique/Method
- **Multi-head Latent Attention (MLA)**: novel attention mechanism reducing KV cache requirements
- **DeepSeekMoE**: sparse MoE architecture with fine-grained expert partitioning
- **8.1T tokens** pretrained data
- **SFT + RL** post-training pipeline
- Efficient inference through reduced activation and KV cache

## Results
- Competitive with 70B+ dense models while activating only 21B parameters
- Excellent coding performance (56% on SWE-bench Lite with 250 samples per Large Language Monkeys paper)
- Long-context capability up to 128K tokens

## Limitations
- MoE load balancing challenges can lead to expert collapse
- Training stability for large-scale MoE models
- RL training pipeline adds complexity and cost
- Smaller activated parameter count may limit single-token computation quality

## Connections
- Key model for coding agent evaluation (SWE-bench, HumanEval)
- Efficient inference architecture relevant to harness cost considerations
- Long context supports multi-file code understanding tasks

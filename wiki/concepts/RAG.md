---
title: "RAG (Retrieval Augmented Generation)"
type: concept
tags: [retrieval, augmented-generation, vector-search, RAG]
sources: [external-ai-knowledge-sources]
last_updated: 2026-04-14
---

## Summary

RAG (Retrieval Augmented Generation) combines retrieval systems with language models to ground responses in retrieved documents rather than relying solely on model weights. It reduces hallucination, enables up-to-date responses, and allows models to cite sources.

## Key Claims

- RAG outperforms fine-tuning on knowledge-intensive tasks where documents change frequently or are too large to encode in weights.
- Hybrid search (dense + sparse) outperforms either alone for most RAG deployments.
- Chunk size dramatically affects retrieval quality — 512 tokens is a common starting point, but semantic chunking often outperforms fixed-size.
- Query expansion and re-ranking improve recall in multi-hop question answering.
- BM25 alone remains competitive as a baseline and is often cheaper than embedding-based retrieval.

## Architecture Patterns

- **Naive RAG**: retrieve top-k chunks → feed into context → generate. Simple but limited by context length and retrieval quality.
- **Advanced RAG**: query rewriting, step-back prompting, sub-question decomposition, self-rag-style reflection.
- **Modular RAG**: router decides retrieval strategy (web vs. internal vs. hybrid); enables multi-source fusion.

## Best Practices

- Index time: use document hierarchy (title, section, paragraph) to enable hierarchical retrieval.
- Retrieve at least 3–5 chunks for complex questions; deduplicate overlapping content before injecting context.
- Use cross-encoders for re-ranking when recall matters more than latency.
- Include source metadata in context (URL, date, title) so model can attribute answers.
- Post-retrieval: rerank → compress (remove redundant sentences) → inject.

## Connection to Fine-Tuning

RAG and fine-tuning are complementary. Fine-tuning improves how a model uses retrieved context (instruction following, formatting); RAG provides the knowledge. Many production systems do both: fine-tune the generator, RAG for retrieval.

## Connections

- [[Prompt Engineering]] — RAG prompts require careful instruction framing to use retrieved context effectively
- [[LLM Fine-Tuning]] — fine-tuning can improve how a model handles retrieved evidence
- [[RLHF]] — RLHF techniques like RLCD can be applied to improve RAG relevance judgments
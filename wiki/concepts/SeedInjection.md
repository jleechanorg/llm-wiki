---
title: "Seed Injection"
type: concept
tags: [llm, prompting, randomness, code-execution]
sources: [provably-fair-dice-roll-primitives]
last_updated: 2026-04-08
---

The technique of inserting a deterministic random seed into an LLM's code execution context to ensure reproducible but unpredictable results. Prevents the LLM from using `random.seed(time.time_ns())` which would produce different results on each execution.

## Implementation
1. Server generates a cryptographically secure seed
2. Replace `random.seed(time.time_ns())` in the prompt with `random.seed('<64-hex-seed>')`
3. Multiple occurrences each get derived seeds to ensure different results
4. Executed code is captured and stored verbatim for verification

## Verification Flow
- Extract seed from stored executed_code via AST parsing
- Compare against revealed seed
- Re-run the same code with the seed to confirm result matches

## Related Concepts
- [[Provably Fair Gaming]] — the use case for seed injection
- [[Code Execution]] — LLM code_execution tool in WorldArchitect.AI

---
title: "Product Taste Index"
type: entity
tags: [product-judgement, llm-wiki, agent-harness]
sources: [auto-product-master-system]
last_updated: 2026-04-14
---

## Summary

This wiki captures my personal product judgement — what I actually want shipped, not just technically correct code. Part of [[ProductTasteLayer]], the product taste subsystem of [[AutoProductMasterSystem]].

## Core Pages

- [[ProductPrinciples]] — high-level values and philosophy
- [[GoodBadExamples]] — concrete past PRs I loved vs. hated, with my comments
- [[TasteRubric]] — scoring dimensions and weights
- [[TasteEvolutionLog]] — chronological record of how my taste has changed

## How It Works

1. [[ProductJudge]] evaluates every PR against this wiki
2. [[TasteLearningLoop]] updates this wiki whenever I manually correct or override a PR
3. The wiki grows automatically — every correction becomes permanent institutional knowledge

## Related Concepts

- [[ProductJudge]] — the oracle that uses this wiki
- [[TasteLearningLoop]] — the loop that updates this wiki
- [[ProductTasteLayer]] — the parent subsystem

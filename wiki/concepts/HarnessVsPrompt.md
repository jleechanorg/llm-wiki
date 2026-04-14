---
title: "HarnessVsPrompt"
type: concept
tags: [harness, prompt, context-management, distinction]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

HarnessVsPrompt is the distinction between harness code and prompt text. The harness is the CODE around the model that controls storage, retrieval, and presentation of information. The prompt is just the text input to the model. Changing the harness changes what information the model can access at all — it determines the entire context management strategy. Prior text optimizers only optimize the prompt; Meta-Harness optimizes the harness code itself.

## Key Claims

- Harness is the CODE around the model (storage, retrieval, presentation); prompt is just the text input
- Changing harness changes what information the model can access at all — it controls the entire context management strategy
- Prompt optimization is a subset of harness engineering
- A 6x performance gap results from harness changes, not prompt changes alone
- Prior text optimizers fail because they only compress/summarize — they never optimize the underlying harness code
- Harness determines what info can be presented; prompt only formats that info

## Connections

- [[HarnessEngineering]] — the practice of modifying harness code
- [[ContextManagement]] — harness is the implementation of context management
- [[PromptEngineering]] — prompt engineering is a subset confined to text formatting rather than information access

---
title: "JSON Extraction"
type: concept
tags: [json, parsing, extraction, text-processing]
sources: [json-parsing-utilities]
last_updated: 2026-04-08
---

Process of finding and extracting valid JSON objects from unstructured or noisy text. Used to parse LLM responses that may contain code execution artifacts, markdown formatting, or logging output.

Key techniques:
- Brace matching with string/escape awareness
- Multi-candidate scanning and scoring
- Priority signals (narrative key, god_mode_response key)

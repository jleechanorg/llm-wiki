---
title: "Token Counting Utilities"
type: source
tags: [logging, tokens, utilities, python, gemini]
source_file: "raw/token-counting-utilities.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python utilities for estimating token counts from text and logging messages with token/character metadata. Used throughout the WorldAI application for consistent logging and monitoring token usage when calling Gemini APIs.

## Key Claims
- **Token Estimation**: Uses 1 token per 4 characters approximation for Gemini models
- **Flexible Input**: Accepts both strings and lists of strings for token counting
- **Formatting**: Provides human-readable output like "1000 characters (~250 tokens)"
- **Logging Integration**: log_with_tokens() wraps logging_util for seamless token tracking

## Key Quotes
> "Uses the rough approximation of 1 token per 4 characters for Gemini models"

## Connections
- [[LoggingUtil]] — uses logging_util module for structured logging
- [[GeminiAPI]] — token estimation serves Gemini API usage tracking

## Contradictions
- None identified

---
title: "Improved Research Test Prompt - Red-Green Methodology"
type: source
tags: [testing, research, red-green, tdd, methodology]
sources: []
date: 2026-04-07
source_file: raw/improved_research_test_prompt.md
last_updated: 2026-04-07
---

## Summary
A test methodology document that establishes RED-GREEN testing for research prompts in Claude Code. The approach uses a non-existent command (`/fakecommand123`) as the RED test (should fail) and a real well-documented command (`/help`) as the GREEN test (should succeed), validating research methodology under both failure and success conditions.

## Key Claims
- **RED test with non-existent command** — Uses `/fakecommand123` which should return "no results found", testing proper handling of null results
- **GREEN test with real command** — Uses `/help` which has official documentation, testing successful research methodology
- **Previous test was flawed** — `/review` is a real built-in command, so both test agents correctly found sources (no error to detect)
- **Source authority validation** — Tests how research behaves with fake vs real commands, ensuring no fabrication of information

## Key Quotes
> "The previous test was flawed because: `/review` IS a real built-in command with actual documentation"

> "RED: Tests behavior with genuinely non-existent command; GREEN: Tests behavior with well-documented real command"

## Connections
- [[Implementation vs Orchestration Decision Framework]] — Both relate to improving Claude Code command behavior
- [[Guide: Creating a New Guardrails Test]] — Both use testing methodologies for AI behavior validation

## Contradictions
- None — This is a new source about test methodology that complements existing sources
---
title: "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework"
type: source
tags: [multi-agent, coding-agent, SOPs, role-assignment, meta-programming]
sources: []
date: 2024-08-01
source_file: raw/arxiv-2411.09529-metagpt.md
---

## Summary

MetaGPT is a multi-agent framework that incorporates Standardized Operating Procedures (SOPs) into LLM-based collaborations. It encodes SOPs as prompt sequences, allowing agents to verify intermediate results and reduce errors from cascading hallucinations. The assembly-line paradigm assigns diverse roles to agents who work together on complex tasks like software engineering.

## Key Claims

- Addresses logic inconsistencies from cascading hallucinations in naive LLM chaining
- Uses **assembly line paradigm** to assign diverse roles to agents
- Generates more coherent solutions than previous chat-based multi-agent systems on software engineering benchmarks
- SOP-encoded prompts inject human-like domain expertise into agent workflows
- Breaks down complex tasks into subtasks involving multiple agents working together

## Technique/Method

- **SOP encoding**: Standardized Operating Procedures encoded as structured prompts
- **Role assignment**: different agents given different professional roles (e.g., architect, engineer, tester)
- **Intermediate verification**: agents check each other's outputs against expected artifacts
- **Structured output**: agents produce structured messages (e.g., design docs, code, tests) rather than free-form text

## Connections

- Multi-agent coordination as harness design
- Connects to Voyager's skill library concept via structured agent collaboration
- Relevant to meta-programming and harness engineering for coding agents

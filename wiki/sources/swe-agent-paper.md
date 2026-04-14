---
title: "SWE-Agent: Agentic LLM Systems for Automated Software Repair"
type: source
tags: [coding-agent, SWE-bench, agentic, software-repair, benchmark]
sources: []
date: 2023-08-22
source_file: raw/arxiv-2308.03688-swe-agent.md
---

## Summary

SWE-Agent is a system for autonomous software engineering that uses LLMs to autonomously resolve issues in real GitHub repositories. It introduces an Agent Computer Interface (ACI) that structures LLM-tool interactions to be more efficient and reliable for software engineering tasks. The system demonstrates that with proper tooling design, LLMs can effectively repair real-world software bugs.

## Key Claims

- Autonomous bug resolution in real GitHub repositories
- Agent Computer Interface (ACI) design improves LLM tool use for SE tasks
- Demonstrates LLM-as-agent capability for full software engineering workflow
- Open-source implementation available

## Technique/Method

- **Agent Computer Interface (ACI)**: structured interface between LLM and development tools
- **Specialized tool definitions** for git, code search, file editing
- **Iterative refinement** through feedback from tool outputs
- **Repository context management** for handling large codebases

## Connections

- Related to [[SWE-Shepherd]] — PRM-based step-level guidance
- Related to [[OpenHands]] — open-source platform for coding agents
- Related to [[SWE-bench]] — benchmark for software engineering agents

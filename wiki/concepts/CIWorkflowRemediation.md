---
title: "CIWorkflowRemediation"
type: concept
tags: []
date: 2026-07-30
---

## Summary
CIWorkflowRemediation refers to workflow-level changes (YAML edits, disabling jobs, configuration fixes) that address future CI execution. This is conceptually separate from per-run causal proof, which requires direct inspection of historical run logs.

## Key Distinction
- **Workflow Remediation**: Fixing workflow YAML, disabling a job, updating configuration — addresses future runs
- **Per-Run Causal Proof**: Direct inspection of historical run logs to determine why a specific run failed

## Related Concepts
- [[AuditIntegrity]] — honesty in failure classification
- [[CausalHonesty]] — empirical proof requirements

## Sources
- [Exhaustive CI audit category & causal honesty (2026-07-30)](../sources/feedback-2026-07-30-ci-audit-category-and-causal-honesty.md)

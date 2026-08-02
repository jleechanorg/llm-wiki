---
title: "CausalHonesty"
type: concept
tags: [ci, audit, evidence]
sources: [feedback-2026-07-30-ci-audit-category-and-causal-honesty]
last_updated: 2026-07-31
---

# CausalHonesty

A mandatory audit integrity principle requiring that CI failure classifications remain UNKNOWN/NO_VERIFIED_FIX when historical run logs have not been directly inspected. This prevents retrofitting false causal narratives from current workflow states.

## Core Rule

- If a historical run's logs or telemetry were not directly inspected and proven, its failure status MUST remain classified as UNKNOWN/NO_VERIFIED_FIX.
- Current disabled/YAML-absent state cannot prove why historical runs failed.
- Workflow remediation addresses future execution, not past causal proof.

## Connections

- [[AuditIntegrity]] — broader audit honesty framework
- [[CIWorkflowRemediation]] — workflow-level fixes vs empirical analysis
- [[WorldArchitectAI]] — project that established this rule via PR #8675
- [[feedback-2026-07-30-ci-audit-category-and-causal-honesty]] — source document

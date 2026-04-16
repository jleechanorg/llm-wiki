---
title: "Prompt Registry"
type: concept
tags: [prompt-registry, versioning, rbac, governance]
date: 2026-04-15
---

## Overview

A Prompt Registry externalizes prompt versioning outside the codebase, enabling RBAC-based access control and release labels. PromptLayer is the canonical implementation.

## Key Properties

- **External versioning**: Prompts stored outside codebase with release labels
- **RBAC**: Granular roles for engineers, operators, reviewers
- **SSO integration**: Enterprise identity provider integration
- **Self-hosting**: On-premise deployment for compliance
- **PromptLayer quote**: "Manage workspace permissions with granular roles for engineers, operators, and reviewers"

## Connection to Governance

Prompt Registry provides governance for LLM interactions — who can modify prompts, what versions are in production, audit trail for changes. Relevant to PR #452's GOVERNANCE.md concept.

## See Also
- [[PromptLayer]]
- [[GovernanceLayer]]
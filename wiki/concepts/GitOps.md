---
title: "GitOps"
type: concept
tags: [gitops, kubernetes, approval-workflows, deployment-governance]
date: 2026-04-15
---

## Overview

GitOps is a deployment paradigm where Git is the source of truth for infrastructure and application state. Weaveworks pioneered it; ArgoCD and Flux are canonical tools. Git-based approval workflows provide governance for deployments.

## Key Properties

- **Git as source of truth**: All infrastructure and app state in Git
- **Approval workflows**: Git-based review and approval before deployment
- **Automated sync**: Systems automatically reconcile with Git state
- **Tools**: Weaveworks, ArgoCD, Flux (CNCF)
- **Quote**: "GitOps provides governance for deployment pipelines"

## Connection to Governance

GitOps provides a governance model for deployment — PRs as approval mechanism, Git history as audit trail, automated sync ensures compliance. Apply to AO: PR review for governance changes, automated sync for policy enforcement.

## See Also
- [[Weaveworks]]
- [[ArgoCD]]
- [[Flux]]
- [[GovernanceLayer]]
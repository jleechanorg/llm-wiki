---
title: "Delegation Flow"
type: concept
tags: [delegation, workflow, orchestration, routing]
sources: [smartclaw-routing-delegation-failures-postmortem.md]
last_updated: 2026-04-07
---

## Description
A workflow pattern where work is delegated to an AI agent for execution in a specific repository context. The March 2026 postmortem identified failures in this flow due to missing explicit source/target repo contracts in dispatch prompts.

## Key Patterns
- **Source/Target Contract**: Explicit declaration of SOURCE_REPO and TARGET_REPO in dispatch headers
- **Pre-PR Validation**: Mandatory checks (git remote -v, gh repo view) before PR creation
- **Proof Bundle**: Required evidence before declaring work complete (file paths, commit URL, PR URL)

## Related Concepts
- [[CrossRepoDelegation]] — delegating work across different repositories
- [[RepoIdentityCheck]] — validating repository context before operations

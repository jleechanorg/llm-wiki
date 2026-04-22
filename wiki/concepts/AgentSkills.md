---
title: "Agent Skills"
type: concept
tags: [agent-skills, tool-config, mongodb, per-tenant-isolation]
date: 2026-04-15
---

## Overview

Agent Skills is MongoDB's concept for externalizing agent tool configurations and schema design heuristics. It enables per-tenant isolation of agent capabilities and permissions.

## Key Properties

- **Externalized config**: Tool controls and schemas outside agent code
- **Per-tenant isolation**: Document model enables tenant-specific skill configurations
- **Configurable permissions**: Runtime permission configuration for agents
- **Key quote**: "Agents are generalists by design, and they don't inherently know the best practices and design patterns that real-world production systems demand" — MongoDB

## Connection to Governance

Agent Skills externalize governance — tool permissions and constraints are not hardcoded but configured per-tenant. This directly addresses the PR #452 goal of filesystem-based editable governance.

## See Also
- [[MongoDB]]
- [[GovernanceLayer]]
- [[PerTenantIsolation]]
---
title: "MongoDB"
type: entity
tags: [database, mcp-server, agent-skills, vector-search]
date: 2026-04-15
---

## Overview

MongoDB provides a Vector Search and MCP Server for AI agent governance. Its Agent Skills feature externalizes schema design heuristics and tool controls for per-tenant agent authorization.

## Key Properties

- **MCP Server**: Manages authentication and defines exactly what agents can access
- **Agent Skills**: Configurable tool controls per agent
- **Authorization**: Native authorization ensures agents operate with only needed permissions
- **Key quote**: "Agents are generalists by design, and they don't inherently know the best practices and design patterns that real-world production systems demand."

## Connections

- [[ModelContextProtocol]] — MongoDB MCP Server implementation
- [[AgentSkills]] — MongoDB externalizes agent skill configurations
- [[PerTenantIsolation]] — MongoDB's document model enables per-tenant isolation

## See Also
- [[ModelContextProtocol]]
- [[AgentSkills]]
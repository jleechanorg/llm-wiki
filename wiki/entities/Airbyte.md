---
title: "Airbyte"
type: entity
tags: [data-integration, mcp, ai-agent, context-store]
date: 2026-04-15
---

## Overview

Airbyte is an open-source data integration platform that also provides an Agent Engine with real-time connectors and context stores for AI agent data access. It implements the Model Context Protocol (MCP) for AI agent-data source interaction.

## Key Properties

- **Architecture**:
  - Agent Engine: Real-time connectors + context store for AI agent data access
  - Data Replication Engine: Batch and CDC connectors
- **AI pipeline features**:
  - Agent-optimized connectors for AI agents
  - MCP Server (Model Context Protocol) implementation
  - Context stores for agent workflow state
  - Connects to Snowflake, Databricks, BigQuery, Apache Iceberg, ClickHouse

## Connections

- [[ModelContextProtocol]] — Airbyte implements MCP for agent-data source interaction
- [[WorkflowEngine]] — Airbyte Agent Engine orchestrates data pipelines for agents
- [[Temporal]] — competing workflow engine with durable execution

## See Also
- [[ModelContextProtocol]]
- [[WorkflowEngine]]

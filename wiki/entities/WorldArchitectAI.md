---
title: "WorldArchitect.AI"
type: entity
tags: [company, product, ai, game, dnd]
sources: [unified-api-implementation]
last_updated: 2026-04-08
---

## Description
AI-powered tabletop RPG campaign management platform using Gemini for narrative generation. The system loads world content from the World of Assiah campaign setting and provides both Flask web and MCP server interfaces.

## Key Components
- **Unified API Layer**: Python module providing consistent JSON interfaces for Flask and MCP
- **World Content Loader**: Loads campaign settings and banned names
- **Firestore Integration**: Firebase backend for campaign data persistence
- **Game State Management**: TypedDict-based state tracking for campaigns

## Connections
- [[Firebase]] — backend database service
- [[World of Assiah]] — default campaign setting

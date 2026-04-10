---
title: "Entity Enhancement"
type: concept
tags: [narrative, entities, context-injection]
sources: [parallel-dual-pass-frontend-implementation-task-019]
last_updated: 2026-04-08
---

## Description
The process of enriching a narrative response by injecting additional context about entities (people, places, organizations, items) mentioned in the story. Entity enhancement detects missing entity information and retrieves relevant details to add depth to the narrative.

## Process
1. **Detection** — Backend identifies which entities in the response lack complete context
2. **Missing Entity List** — Returns array of `missing_entities` with the initial response
3. **Background Fetch** — Frontend calls enhancement endpoint with missing entity list
4. **Context Injection** — Enhancement endpoint retrieves entity details from database
5. **Response Replacement** — Enhanced narrative replaces the original seamlessly

## Data Flow
```
Initial Response → Check enhancement_needed → 
If true: call enhance-entities endpoint → 
Receive enhanced_response + entities_injected count → 
Replace story entry
```

## Connections
- [[Parallel Dual-Pass Optimization]] — The optimization framework using enhancement
- [[TASK-019]] — Implementation task for entity enhancement

---
title: "JSON Schema Response Format"
type: concept
tags: [api-schema, structured-output, response-formatting]
sources: []
last_updated: 2026-04-08
---

LLM API response formatting technique using JSON Schema definitions instead of legacy json_object mode. The strict:false parameter keeps planning_block flexible for dynamic choice keys, preventing schema echo where API returns {"type": "object"} instead of actual content.

**Problem solved:**
- Legacy json_object causes some providers to echo schema config
- json_schema (strict:false) allows dynamic keys while maintaining structure
- Used by Cerebras provider to ensure content generation over schema reflection

**Related pages:** [[CerebrasDirectApiProviderImplementation]]

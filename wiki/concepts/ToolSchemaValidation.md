---
title: "Tool Schema Validation"
type: concept
tags: [testing, tool-definition, schema]
sources: [faction-tools-schema-execution-unit-tests]
last_updated: 2026-04-08
---

## Definition
A testing pattern that verifies JSON tool schemas conform to the expected structure, including parameter types, required fields, and property definitions. Tool schemas define the interface between the LLM and backend functions.

## Application
In this test suite, schema validation confirms that faction tools declare correct required parameters (e.g., soldiers, spies, elites for power calculation) and have properly structured parameter objects.

## Related Concepts
- [[MockPatching]] — isolation technique used in these tests
- [[ToolExecutionMapping]] — linking tool names to handler functions

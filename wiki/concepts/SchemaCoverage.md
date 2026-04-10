---
title: "Schema Coverage"
type: concept
tags: [testing, coverage, schema]
sources: [schema-strictness-schema-coverage-guard-tests]
last_updated: 2026-04-08
---

Testing practice of verifying code paths exercise all schema-defined fields. The check_schema_coverage.py script identifies missing paths where code doesn't reference schema properties, ensuring guards are properly connected to actual game state mutations.

## Validation Process
1. Parse schema to extract defined paths
2. Scan code for references to those paths
3. Report missing paths that lack code coverage
4. Fail if --fail-under threshold not met

## Related
- [[CheckSchemaCoverage]] — script that performs coverage validation
- [[SchemaStrictness]] — what coverage validates

---
title: "CheckSchemaCoverage"
type: entity
tags: [script, testing, validation]
sources: [schema-strictness-schema-coverage-guard-tests]
last_updated: 2026-04-08
---

Python script that validates schema coverage by checking code paths against schema-defined fields. Supports --report-json, --fail-under, and --required-path flags. Exit code 0 indicates no missing paths.

## Usage
```bash
python scripts/check_schema_coverage.py --report-json --fail-under 0 --required-path combat_state.rewards_processed
```

## Related
- [[SchemaCoverage]] — concept tested by this script
- [[GameStateSchema]] — schema being validated

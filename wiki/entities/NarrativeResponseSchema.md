---
title: "narrative_response_schema.py"
type: entity
tags: [file, json-parsing, bug-fix]
sources: []
last_updated: 2026-04-07
---

## Description
File in `mvp_site/` that contains `parse_structured_response()` function. Modified to include code execution artifact removal logic to handle responses where code output precedes JSON.

## Related
- [[CodeExecutionJSONParsingFixVerification]] — fix verified against this file
- [[CodeExecutionJSONParsingTests]] — test file for this fix

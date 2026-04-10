---
title: "Contract Manifest"
type: concept
tags: [configuration, versioning, contracts, json]
sources: []
last_updated: 2026-04-08
---

JSON configuration file that centrally lists all contracts (prompts, schemas, tool interfaces) with their versions and integrity hashes. Provides a single source of truth for tracking what version of each component is deployed.

## Manifest Structure
```json
{
  "manifest_version": "1.0",
  "contracts": [
    {
      "id": "contract_id",
      "type": "prompt|tool_schema|tool_interface",
      "version": "1.0.0",
      "path": "relative/path/to/file",
      "sha256": "hexadecimal hash"
    }
  ]
}
```

## Usage
- Change detection via hash comparison
- Dependency resolution for deployments
- Audit trail for prompt/tool updates
- Integration with [[PromptVariantLoadingSystem]]

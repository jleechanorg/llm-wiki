---
title: "Prompt Versioning"
type: concept
tags: [prompt-engineering, versioning, contracts]
sources: []
last_updated: 2026-04-08
---

System for tracking changes to prompts using semantic version numbers (major.minor.patch) and SHA256 integrity hashes. Enables precise dependency management and change detection in AI system instructions.

## In WorldArchitect.AI Context
The Prompt Contract Manifest tracks 6 prompts with versions ranging from 1.0.0 to 1.0.1. Each update requires:
1. Version increment following semver rules
2. SHA256 hash recalculation
3. Manifest update with new version and hash

## Related Concepts
- [[PromptVariantLoadingSystem]] — loads different prompt versions based on strategy
- [[ContractManifest]] — centralized tracking of versioned assets

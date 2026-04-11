---
title: "Prompt Contract Manifest"
type: source
tags: [prompt-engineering, versioning, contracts, mvp, worldarchitect]
source_file: "raw/prompt_contract_manifest.json"
sources: []
last_updated: 2026-04-08
---

## Summary
JSON manifest defining the contract versioning system for WorldArchitect.AI MVP site, tracking 6 core prompts and tools with SHA256 integrity verification. Each contract specifies version, file path, and cryptographic hash for change detection.

## Key Claims
- **Centralized Contract Tracking** — Single manifest file lists all prompt and tool contracts with version numbers
- **SHA256 Integrity Verification** — Each contract entry includes cryptographic hash for change detection
- **Version Precision** — Versions tracked at 3-digit semver (e.g., 1.0.1, 1.0.2) for precise dependency management
- **Type Differentiation** — Contracts categorized as prompt, tool_schema, or tool_interface for clear purpose identification

## Key Contracts
| ID | Type | Version | Path |
|---|---|---|---|
| master_directive_prompt | prompt | 1.0.1 | mvp_site/prompts/master_directive.md |
| game_state_instruction_prompt | prompt | 1.0.1 | mvp_site/prompts/game_state_instruction.md |
| planning_protocol_prompt | prompt | 1.0.1 | mvp_site/prompts/planning_protocol.md |
| narrative_response_schema | tool_schema | 1.0.0 | mvp_site/narrative_response_schema.py |
| mcp_api_tool_contract | tool_interface | 1.0.2 | mvp_site/mcp_api.py |
| character_template_prompt | prompt | 1.0.0 | mvp_site/prompts/character_template.md |

## Connections
- [[PromptVariantLoadingSystem]] — complements this manifest by providing variant loading based on dice strategy
- [[MCPClientLibraryforWorldArchitectAI]] — integrates with the mcp_api_tool_contract
- [[NarrativeDirectivesLite]] — relates to the character_template_prompt for character creation flows

## Contradictions
- None identified

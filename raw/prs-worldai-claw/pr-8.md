# PR #8: Add prompt contract manifest, 9-layer assertions, and LLM output schema/tests

**Repo:** jleechanorg/worldai_claw
**Merged:** 2026-02-22
**Author:** jleechan2015
**Stats:** +394/-0 in 8 files

## Summary
- Adds prompt contract manifest for system instruction prompt with SHA-256 tracking and versioning.
- Adds Jest assertions that system instruction still contains required 9-layer contract phrases and canonical field-name contract.
- Adds JSON schema for the LLM turn response envelope (strict top-level keys, banned legacy field prevention, mechanic/ui block shapes).
- Adds docs ↔ code prompt registration regression checks and keeps registry wiring in source.
- Adds prompt contract regression test

## Raw Body
## Summary
- Adds prompt contract manifest for system instruction prompt with SHA-256 tracking and versioning.
- Adds Jest assertions that system instruction still contains required 9-layer contract phrases and canonical field-name contract.
- Adds JSON schema for the LLM turn response envelope (strict top-level keys, banned legacy field prevention, mechanic/ui block shapes).
- Adds docs ↔ code prompt registration regression checks and keeps registry wiring in source.
- Adds prompt contract regression test to detect prompt hash drift without manifest version bump.

## Notes
- Commit: ea686f0
- Branch created from origin/main as requested.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Primarily adds schemas and regression tests; runtime behavior change is limited to exporting a prompt registry constant, with no changes to request handling or persistence logic.
> 
> **Overview**
> Adds a *prompt contract* manifest (`prompt_contracts.json`) that pins the system-instruction prompt to a SHA-256 + version, with Jest coverage that fails if prompt content changes without a version bump.
> 
> Introduces a canonical `SYSTEM_INSTRUCTION_PROMPT_REGISTRY` and tests to ensure it exactly matches all `docs/system_instructions/*.md` files (and references no missing files), plus new assertions that the loaded `SYSTEM_INSTRUCTION` still contains required “9-layer” contract phrases.
> 
> Defines a draft-07 JSON Schema for the LLM turn response envelope (`llm_turn_response.schema.json`) with strict top-level keys/required fields and schema-referenced `mechanic_request`/`ui_block` shapes, and adds AJV-based tests (including `date-time` format validation via `ajv-formats`) to enforce it.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 3295a43dd4b818b6140dfbe3fc93a2087bb53589. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->


<!-- COPILOT_TRACKING_STA

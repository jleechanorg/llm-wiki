# PR #6: feat: Make agent names globally unique and allow flexible project keys

**Repo:** jleechanorg/mcp_agent_mail
**Merged:** 2025-11-06
**Author:** jleechan2015
**Stats:** +430/-57 in 5 files

## Summary
(none)

## Raw Body
Changes:
1. Agent names are now globally unique across all projects
   - Added _agent_name_exists_globally() to check uniqueness across all projects
   - Updated _generate_unique_agent_name() to use global uniqueness check
   - Updated _get_or_create_agent() to validate global uniqueness when user provides a name
   - In strict mode, throws error if name exists in another project
   - In coerce mode, auto-generates unique name if conflict detected

2. Project keys can now be any string identifier
   - Removed absolute path validation requirement in ensure_project()
   - Updated documentation to reflect flexible project key patterns
   - Supports absolute paths, repo names, or custom identifiers
   - Maintains backward compatibility with existing absolute path usage

These changes prevent agent name confusion and provide more flexibility in project organization.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> Enforces globally unique (case-insensitive) agent names with DB migration/index and expands project keys to any string; updates tools/docs and adds tests.
> 
> - **DB/Schema**:
>   - Global, case-insensitive uniqueness for `Agent.name` via `uq_agents_name_ci` on `agents(lower(name))`.
>   - Migration auto-renames duplicate agent names (`_check_and_fix_duplicate_agent_names`).
>   - Removed per-project unique constraint; model updated accordingly.
> - **Identity/Agents**:
>   - New global lookup `_agent_name_exists_globally`; name generation now checks global availability only.
>   - Catch `IntegrityError` on agent upsert/create and surface as `ToolExecutionError(NAME_TAKEN)` with recoverable metadata.
>   - Coerce/strict modes: in strict, reject taken names; in coerce, auto-generate unique alternative; case-insensitive updates within same project.
>   - Sanitization: non-alphanumerics stripped; max length 128; clearer docs.
> - **Projects**:
>   - `ensure_project` now accepts any string `human_key` (not just absolute paths); docs/examples updated.
> - **

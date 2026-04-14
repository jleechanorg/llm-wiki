# PR #1: Allow unrestricted cross-project messaging

**Repo:** jleechanorg/mcp_agent_mail
**Merged:** 2025-11-05
**Author:** jleechan2015
**Stats:** +435/-94 in 16 files

## Summary
- auto-create cross-project links whenever a recipient is specified, even without prior contact approval
- add global agent lookup so names without project qualifiers can fan out to remote repos when unique
- default CONTACT_ENFORCEMENT_ENABLED to false so no handshake is needed by default

## Raw Body
## Summary
- auto-create cross-project links whenever a recipient is specified, even without prior contact approval
- add global agent lookup so names without project qualifiers can fan out to remote repos when unique
- default CONTACT_ENFORCEMENT_ENABLED to false so no handshake is needed by default

## Testing
- source .venv/bin/activate && python -m compileall src/mcp_agent_mail/app.py

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> Adds automatic cross‑project recipient resolution/linking when contact enforcement is disabled and relaxes agent-name rules to accept sanitized freeform names; updates docs/config and tests accordingly.
> 
> - **Core/Messaging**:
>   - Auto cross‑project routing: on unknown local recipient, globally resolve unique matches and auto‑create approved `AgentLink`s; support explicit `project:<id>#<Name>` and `Name@<project>` addressing.
>   - New helpers: `_ensure_cross_project_link`, `_lookup_agents_any_project`; sender aliasing on target projects.
>   - Recipient handling: auto‑register missing local agents, structured errors for unknown recipients, and improved enforcement checks.
> - **Policy/Config**:
>   - Default `CONTACT_ENFORCEMENT_ENABLED` → `false` (config + README), routing paths updated to respect this.
> - **Identity**:
>   - Relax naming: remove strict adjective+noun validation; `register_agent` now accepts sanitized freeform names.
> - **Tests**:
>   - New tests for cross‑project auto‑linking on/off and for freeform agent names.
> - **Docs/Tooling**:
>   - Update `README.md`, `AGENTS.md`, add `CLAUDE.md` notes.
>   - Add/update MCP client configs (`*.mcp.json`, `.claude/settings.json`) with bearer token and hooks; minor script cleanup in `run_server_with_token.sh`.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit ddf238f6fa0fab976fb1866b29f7d47556997646. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<

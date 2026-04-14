# PR #1: docs: update roadmap with gateway fix

**Repo:** jleechanorg/thinclaw
**Merged:** 2026-04-08
**Author:** jleechan2015
**Stats:** +14/-0 in 1 files

## Summary
- Updated thinclaw roadmap with 2026-04-08 activity documenting the gateway tools config fix
- Gateway tools (list_agents) now working - root cause was config path confusion (`gateway.tools.allow` vs `tools.allow`)

## Test Plan
- [x] Gateway starts successfully
- [x] agents_list tool returns valid response via /tools/invoke
- [x] Roadmap docs updated

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Low risk documentation-only change; no runtime behavior or configuration is modified in this PR.
> 
> **Overview**
> Updates `roadmap/README.md` to add a new *2026-04-08* entry and records that the `list_agents`/Gateway tool exposure issue was fixed due 

## Raw Body
## Summary
- Updated thinclaw roadmap with 2026-04-08 activity documenting the gateway tools config fix
- Gateway tools (list_agents) now working - root cause was config path confusion (`gateway.tools.allow` vs `tools.allow`)

## Evidence
Gateway running and agents_list tool responding:
```
curl .../tools/invoke -d '{"tool":"agents_list"}'
# Returns: {"ok":true,"result":{"agents":[{"id":"main","configured":false}]}}
```

Git provenance:
- HEAD: e580ceb9667f950682dac5bf6f011767f1b82f35
- Branch: pr/gateway-tools-fix

## Test plan
- [x] Gateway starts successfully
- [x] agents_list tool returns valid response via /tools/invoke
- [x] Roadmap docs updated

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Low risk documentation-only change; no runtime behavior or configuration is modified in this PR.
> 
> **Overview**
> Updates `roadmap/README.md` to add a new *2026-04-08* entry and records that the `list_agents`/Gateway tool exposure issue was fixed due to a config path mismatch (`gateway.tools.allow` vs `tools.allow`).
> 
> <sup>Reviewed by [Cursor Bugbot](https://cursor.com/bugbot) for commit e580ceb9667f950682dac5bf6f011767f1b82f35. Bugbot is set up for automated code reviews on this repo. Configure [here](https://www.cursor.com/dashboard/bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

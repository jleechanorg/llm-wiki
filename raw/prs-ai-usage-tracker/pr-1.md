# PR #1: Add PyPI/npm packages with --version and auto-install

**Repo:** jleechanorg/ai-usage-tracker
**Merged:** 2026-02-12
**Author:** jleechan2015
**Stats:** +945/-181 in 13 files

## Summary
- Published `ai-usage-tracker` to both **PyPI** (v0.1.2) and **npm** (v0.1.2)
- Added `--version` / `-V` flag support to both Python and Node.js CLIs
- Added dependency auto-detection: when `ccusage` or `ccusage-codex` are missing, prompts to install them interactively instead of crashing
- Fixed npm package throwing ugly stack traces on missing dependencies — now shows clean error with install instructions
- Correct npm package name used: `@ccusage/codex` (not `ccusage-codex`)
- Updated README 

## Test Plan
- [x] `pip install ai-usage-tracker && ai-usage-tracker --version` → `ai-usage-tracker 0.1.2`
- [x] `npm install -g ai-usage-tracker && ai-usage-tracker-js --version` → `ai-usage-tracker 0.1.2`
- [x] Both CLIs show clean error + install prompt when dependencies are missing
- [x] Both CLIs produce matching output when dependencies are present
- [x] Verified from `/tmp` (not local dir) to confirm packages run from site-packages/global node_modules

🤖 Generated with [Claude Code](https://claude.com

## Raw Body
## Summary
- Published `ai-usage-tracker` to both **PyPI** (v0.1.2) and **npm** (v0.1.2)
- Added `--version` / `-V` flag support to both Python and Node.js CLIs
- Added dependency auto-detection: when `ccusage` or `ccusage-codex` are missing, prompts to install them interactively instead of crashing
- Fixed npm package throwing ugly stack traces on missing dependencies — now shows clean error with install instructions
- Correct npm package name used: `@ccusage/codex` (not `ccusage-codex`)
- Updated README with `pip install` and `npm install -g` instructions

## Test plan
- [x] `pip install ai-usage-tracker && ai-usage-tracker --version` → `ai-usage-tracker 0.1.2`
- [x] `npm install -g ai-usage-tracker && ai-usage-tracker-js --version` → `ai-usage-tracker 0.1.2`
- [x] Both CLIs show clean error + install prompt when dependencies are missing
- [x] Both CLIs produce matching output when dependencies are present
- [x] Verified from `/tmp` (not local dir) to confirm packages run from site-packages/global node_modules

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Adds new distributable CLIs that execute external commands and can prompt-run `npm install -g`, so behavior changes are user-environment dependent and may affect installs/permissions. Core reporting logic is mostly refactored/reused, limiting data-handling risk.
> 
> **Overview**
> **Publishes installable CLIs for both Python and Node.js.** Adds a Python package (`pyproject.toml`, `ai_usage_tracker/`) with the `ai-usage-tracker` entrypoint and a new TypeScript-based npm package (`npm/`) exposing `ai-usage-tracker-js`.
> 
> **Improves CLI ergonomics and dependency handling.** Both CLIs add `--version/-V`, fetch Claude/Codex usage in parallel, and proactively detect missing `ccusage`/`ccusage-codex` (mapped to `@ccusage/codex`) with an interactive prompt to install via npm; Node errors are surfaced cleanly instead of stack traces.
> 
> **

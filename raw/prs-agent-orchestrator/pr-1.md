# PR #1: fix: wire extraBotAuthors config through plugin pipeline

**Repo:** jleechanorg/agent-orchestrator
**Merged:** 2026-03-16
**Author:** jleechan2015
**Stats:** +135/-2 in 5 files

## Summary
- Add plugins top-level field to OrchestratorConfig for plugin-specific settings
- Extend extractPluginConfig() in plugin-registry.ts to handle SCM slot
- Fix getSCM() in plugins.ts to pass config to plugin.create()
- Add unit tests covering extraBotAuthors config in scm-github plugin

## Raw Body
## Summary
- Add plugins top-level field to OrchestratorConfig for plugin-specific settings
- Extend extractPluginConfig() in plugin-registry.ts to handle SCM slot
- Fix getSCM() in plugins.ts to pass config to plugin.create()
- Add unit tests covering extraBotAuthors config in scm-github plugin

## Testing
All 74 tests in scm-github package pass.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Moderate risk because it changes the validated `OrchestratorConfig` shape and how SCM plugins are instantiated, which could affect plugin loading/behavior if config keys are mis-specified or unexpected types are provided.
> 
> **Overview**
> Adds a top-level `plugins` config map to `OrchestratorConfig` (and Zod validation) to support plugin-specific settings.
> 
> Wires SCM plugin configuration through the plugin pipeline: `plugin-registry` now extracts `scm` configs from `config.plugins["scm-<name>"]`, and the CLI’s `getSCM()` passes that config into `plugin.create()`.
> 
> Extends `scm-github` tests to verify `extraBotAuthors` can be provided via `create(config)` and affects bot filtering in `getAutomatedComments`/`getPendingComments`.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 278b0b0305d2f1bd7c75c0e3acdfbf7b5e101ba8. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Summary by CodeRabbit

## Release Notes

* **New Features**
  * SCM plugins now support optional configuration parameters for enhanced customization and flexibility.
  * GitHub SCM plugin now supports configurable bot author recognition, allowing users to define custom bot accounts for improved comment filtering.

<!-- end of auto-generated comment: release notes by coderabbit.ai -->

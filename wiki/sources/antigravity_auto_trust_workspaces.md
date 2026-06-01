# Automatic Workspace Trust Injection in Antigravity CLI

**Source**: Claude memory — `feedback_2026-05-31_antigravity_auto_trust_workspaces.md`
**Date**: 2026-05-31
**Project**: agent-orchestrator
**Bead**: bd-fpzd

## Summary

When an AO worker processes a task inside a repository or project folder using the Antigravity CLI (`agy`), the CLI requires permission to read, edit, and execute files inside that folder. If the folder is not marked as trusted, `agy` prompts the user interactively:
`Do you trust the contents of this project? ... Antigravity CLI requires permission to read, edit, and execute files here.`
In headless background sessions or AO worker threads, this prompt blocks indefinitely because there is no terminal interaction possible.

## Technical Detail

1. Antigravity CLI tracks trusted workspace paths inside `~/.gemini/trustedFolders.json` using the format `{"<path>": "TRUST_FOLDER"}`.
2. In `packages/plugins/agent-antigravity/src/index.ts`, the session configuration is isolated by redirecting `$HOME` to `~/.ao-sessions/<sessionId>` and copying/symlinking the `.gemini/` configuration.
3. If the project workspace path (e.g. `launchConfig.projectConfig.path`) is not pre-registered in `trustedFolders.json` in the session's temporary folder, the interactive prompt blocks the background worker.

## The Fix / Policy

- **Automatic Trust Injection**: When preparing the session environment inside `getEnvironment`, dynamically load the session's `.gemini/trustedFolders.json` (or create a fresh one if absent) and register the `launchConfig.projectConfig.path` (and its fully-resolved real path) with `"TRUST_FOLDER"` clearance.
- **Fail-Open Writes**: Wrap the file write in a `try-catch` to avoid blocking session startup if file I/O errors occur.

## Related Concepts

- [[AntigravityWorkspaceTrust]]
- [[HeadlessInteractiveBlocker]]
- [[SessionIsolationConfig]]
- [[ZeroTouchAutomation]]

---
name: macOS Keychain ACL and Partition List Perms Fix
description: Prevent repeated Keychain authentication dialog prompts when CLI tools or GUI applications access Keychain generic passwords.
type: feedback
bead: none
---

# macOS Keychain ACL and Partition List Perms Fix

## Context
When CLI applications (e.g. `claude-code`) or GUI tools (e.g. `CodexBar`) access Keychain generic passwords (such as `Claude Code-credentials`), macOS Keychain security restricts cross-app reading and resets access control whenever binary signatures change or tools are updated/recompiled. This causes repeated macOS Keychain password prompts even after clicking "Always Allow".

## Fix Applied
FIX: Updated access control partition list on `Claude Code-credentials` via `security set-generic-password-partition-list -s "Claude Code-credentials" -a "jleechan" -S "apple:,apple-keychain:" ~/Library/Keychains/login.keychain-db` on 2026-07-25.

## Reusable Pattern / Rule
1. Whenever a tool or user experiences recurring macOS Keychain password prompts for credentials (e.g., `Claude Code-credentials`, `GitHub PAT`, `GOG Keyring`):
   - Update the Access Control List (ACL) partition list using `security set-generic-password-partition-list -s "<service>" -a "<account>" -S "apple:,apple-keychain:" ~/Library/Keychains/login.keychain-db` or set "Allow all applications to access this item" in Keychain Access.app.
2. Never force the user to repeatedly grant one-off permissions when permanent ACL partition list configuration can eliminate prompt friction across app updates.

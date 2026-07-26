---
title: "macOS Keychain ACL and Partition List Perms Fix"
type: source
tags: [macos, keychain, permissions, SecurityCLI, feedback]
date: 2026-07-25
source_file: raw/feedback_2026-07-25_macos_keychain_partition_list_acl.md
---

## Summary
Prevents repeated macOS Keychain authentication dialog prompts when CLI tools (such as `claude-code`) or GUI applications (such as `CodexBar`) access Keychain generic passwords. Updating the access control partition list via `security set-generic-password-partition-list` permanently authorizes access across app binary rebuilds and updates.

## Key Claims
- macOS Keychain ties "Always Allow" access to the binary cryptographic signature (CDHash), which resets whenever tools or app binaries update or recompile.
- Cross-app reading of items created by other apps triggers repeated password prompts.
- Updating partition list or setting Access Control to allow all applications eliminates password prompt friction.

## Connections
- [[macOS-Keychain]] — Access control management and security ACLs
- [[SecurityCLI]] — macOS security command-line interface for keychain manipulation

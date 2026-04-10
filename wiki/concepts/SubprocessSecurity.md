---
title: "Subprocess Security"
type: concept
tags: [security, subprocess, python]
sources: [subprocess-security-vulnerabilities-copilot-utils]
last_updated: 2026-04-08
---

## Description
Practice of using subprocess module securely in Python to prevent command injection vulnerabilities.

## Best Practices
1. **Never use shell=True** - Avoids shell interpretation of arguments
2. **Use list arguments** - Pass command as list: ["git", "status"]
3. **Validate input** - Sanitize any user-provided values
4. **Use shell=False explicitly** - Make intent clear

## Testing
Security tests should verify:
- All subprocess.run calls use list arguments
- shell parameter is False or unset
- Malicious input cannot be injected

## Related
- [[ShellInjection]]
- [[GitCommands]]

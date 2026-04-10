---
title: "Shell Injection"
type: concept
tags: [security, vulnerability, subprocess]
sources: [subprocess-security-vulnerabilities-copilot-utils]
last_updated: 2026-04-08
---

## Description
Security vulnerability that occurs when user input is passed to shell execution (shell=True in subprocess), allowing attackers to inject arbitrary commands via shell metacharacters like ;, |, &&, etc.

## Attack Example
With shell=True, input like "123; rm -rf /" would execute both the intended command and the malicious command.

## Prevention
- Use shell=False in subprocess calls
- Pass commands as lists, not strings: subprocess.run(["git", "status"]) not subprocess.run("git status", shell=True)
- Validate and sanitize all user input

## Related
- [[GitCommands]]
- [[SubprocessSecurity]]

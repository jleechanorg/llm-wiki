# PR #2: docs: add README.md and install.sh for SmartClaw prototype

**Repo:** jleechanorg/smartclaw
**Merged:** 2026-03-29
**Author:** jleechan2015
**Stats:** +0/-0 in 0 files

## Summary
- Add comprehensive README.md with WIP prototype disclaimer
- Differentiate SmartClaw from Agent-Orchestrator (jleechanclaw)
- Add install.sh with prerequisite checking and environment setup
- Add .env.example for safe configuration (never commit secrets)

## Background
SmartClaw is a prototype reference repo for the OpenClaw autonomous orchestrator. This establishes the initial documentation and installation scripts.

## Test Plan
- [ ] Verify README.md renders correctly
- [ ] Verify install.sh is executable
- [ ] Verify .env.example contains template values only

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Low risk because changes are limited to documentation and a local install script/environment template, with no runtime logic changes. Main risk is minor user-environment side effects from `install.sh` creating/linking `.env` files.
> 
> **Overv

## Raw Body
## Summary
- Add comprehensive README.md with WIP prototype disclaimer
- Differentiate SmartClaw from Agent-Orchestrator (jleechanclaw)
- Add install.sh with prerequisite checking and environment setup
- Add .env.example for safe configuration (never commit secrets)

## Background
SmartClaw is a prototype reference repo for the OpenClaw autonomous orchestrator. This establishes the initial documentation and installation scripts.

## Test plan
- [ ] Verify README.md renders correctly
- [ ] Verify install.sh is executable
- [ ] Verify .env.example contains template values only

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Low risk because changes are limited to documentation and a local install script/environment template, with no runtime logic changes. Main risk is minor user-environment side effects from `install.sh` creating/linking `.env` files.
> 
> **Overview**
> Adds initial onboarding materials for the SmartClaw prototype: a WIP-focused `README.md` describing scope, dependencies, setup, and security guidance.
> 
> Introduces `install.sh` to check prerequisites and bootstrap a local `.env` (copying from `.env.example` or linking `~/.smartclaw.env`), plus adds `.env.example` with placeholder configuration values to avoid committing secrets.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 6f420ebdcae781b5cd1ef5c2c2ba59d4de3962e0. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **Documentation**
  * Expanded README with project overview, install instructions, dependency requirements, environment-variable setup guidance, security notes, and usage/development commands.

* **Chores**
  * Added an interactive install/setup script to automate initial configuration a

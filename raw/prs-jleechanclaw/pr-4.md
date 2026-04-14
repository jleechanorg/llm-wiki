# PR #4: Add recurring content backup cron job

**Repo:** jleechanorg/jleechanclaw
**Merged:** 2026-02-14
**Author:** jleechan2015
**Stats:** +1148/-40 in 21 files

## Summary
- Adds a reusable backup installer script to set up a 2:00 AM daily cron backup of OpenClaw configuration and LaunchAgent.
- Adds script under both repo root and openclaw-config so it can be copied into ~/.openclaw.

## Raw Body
## Summary
- Adds a reusable backup installer script to set up a 2:00 AM daily cron backup of OpenClaw configuration and LaunchAgent.
- Adds script under both repo root and openclaw-config so it can be copied into ~/.openclaw.

## Notes
The existing backup docs already describe setup; this commit provides the concrete recurring job implementation via cron.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Adds cron and LaunchAgent-adjacent scripts that automatically restart services and create backups, which can impact host behavior if misconfigured. Also introduces new WhatsApp/Slack setup flows and writes backup archives containing credentials, so operational/security review is warranted.
> 
> **Overview**
> Adds an automated backup installer (`enable-auto-backup.sh`) that writes a `backup-content.sh` job and installs a **2:00 AM daily cron** tarball backup of `~/.openclaw` (optionally including the LaunchAgent plist) with **30-day retention**.
> 
> Introduces operational scripts for macOS reliability: a `health-check.sh` that verifies the gateway is loaded/running/responding (and restarts/installs via `launchctl`/`openclaw` as needed) and a `startup-check.sh` that sends a WhatsApp startup confirmation using `OPENCLAW_WHATSAPP_TARGET`; both add basic hardening (CLI presence checks, log directory creation, explicit failure handling). Also updates config/docs to remove hardcoded IDs/numbers (templated Slack/WhatsApp values), adds `slack-setup.sh`, and includes new setup/security/identity “memory” documents plus TTS settings in `openclaw-config/openclaw.json`.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit c73ea0fd31010df4bd9cc59ddf4234edeef2426a. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **Documentation**
  * Added comp

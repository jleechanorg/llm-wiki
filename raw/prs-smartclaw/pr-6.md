# PR #6: docs: add OpenClaw Docker staging setup guide

**Repo:** jleechanorg/smartclaw
**Merged:** 2026-04-02
**Author:** jleechan2015
**Stats:** +352/-0 in 1 files

## Summary
(none)

## Raw Body
Adds `docs/openclaw-docker-staging-setup.md` as a sibling to `openclaw-staging-setup.md`.

Covers:
- Docker-based staging gateway vs native launchd
- docker-compose configuration with staging credentials  
- Loopback-only port binding (127.0.0.1:18810 → container :18789)
- Control UI origin patching for non-loopback bind
- Start/stop/manage/update/teardown commands

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Low risk documentation-only change; no runtime code or configuration defaults are modified, but the guide includes handling of tokens/secrets that readers must apply carefully.
> 
> **Overview**
> Adds a new `docs/openclaw-docker-staging-setup.md` guide for running the OpenClaw *staging* gateway in Docker alongside a host-installed gateway.
> 
> The doc walks through GHCR auth + image pulling, a sample `docker-compose` with loopback-only port mapping, volume mounts, healthchecks, and a companion CLI container, plus required `openclaw.json` patching for Control UI `allowedOrigins` when binding to `lan`, and includes update/teardown and troubleshooting steps.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 8aefd6df854961a8cbc1083003a592c95459c8a3. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **Documentation**
  * Added a comprehensive step‑by‑step Docker guide for running staging in isolation: stopping the native staging service, authenticating and pulling images, composing gateway and CLI services, mounting config/workspace, setting required environment variables, configuring a healthcheck and control UI origins, and optional troubleshooting flags. Includes commands for start/verify/inspect/logs/update/teardown, a Docker vs native comparison, and troubleshooting for connection resets, healthcheck failures, token/webso

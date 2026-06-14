---
title: "Feedback 2026 06 10 Dual Gateway Drift"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-10
source_file: .claude/projects/-Users-jleechan--hermes/memory/feedback_2026-06-10_dual_gateway_drift.md
---

## Summary

Investigation 2026-06-10: two launchd gateway labels on disk is **migration drift**, not intentional dual production. **Canonical (install-launchagents.sh):**
- Prod: `ai.hermes.prod` → `HERMES_HOME=~/.hermes_prod` → port **8643** → live Slack
- Staging (optional): `ai.hermes.staging` → `~/.hermes/` → port **8644** → off between deploys
- Installer **bootouts/deletes** legacy `ai.hermes.gateway.plist` when prod installs

**Orphan on live machine:** `~/Library/LaunchAgents/ai.hermes.gateway.plist...

## Original

Investigation 2026-06-10: two launchd gateway labels on disk is **migration drift**, not intentional dual production.

**Canonical (install-launchagents.sh):**
- Prod: `ai.hermes.prod` → `HERMES_HOME=~/.hermes_prod` → port **8643** → live Slack
- Staging (optional): `ai.hermes.staging` → `~/.hermes/` → port **8644** → off between deploys
- Installer **bootouts/deletes** legacy `ai.hermes.gateway.plist` when prod installs

**Orphan on live machine:** `~/Library/LaunchAgents/ai.hermes.gateway.plist` runs Python `hermes_cli.main` from `projects_other/hermes-agent` with `HERMES_HOME=~/.hermes` — dev checkout, not prod.

**Repo gap:** `install-launchagents.sh` references `launchd/ai.hermes.prod.plist` but that file is **missing from repo** (only `ai.hermes.gateway.plist` / `com.hermes.gateway.plist` templates exist).

**Why:** Incomplete migration npm/18789 → Python prod/8643 → split `~/.hermes` (repo/staging) vs `~/.hermes_prod` (runtime). Label `ai.hermes.gateway` has meant staging alias, Node prod, and dev venv at different times.

**How to apply:** Before any gateway work: `grep HERMES_PROD_LABEL ~/.hermes/scripts/deploy.sh`; expect **`ai.hermes.prod` only** for Slack. Remove orphan `ai.hermes.gateway` plist; add prod plist to repo; use `curl :8643/health` not `:18789`.

**Tracking:** bead `jleechan-eeql`, GH [#602](https://github.com/jleechanorg/jleechanclaw/issues/602)

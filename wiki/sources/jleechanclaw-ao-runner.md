---
title: "jleechanclaw-ao-runner"
type: source
tags: [jleechanclaw, docker, github-actions, runner]
date: 2026-04-14
source_file: jleechanclaw/ao_runner/runner.py
---

## Summary
Docker container lifecycle management for GitHub Actions self-hosted runners. Fetches runner registration tokens from GitHub API, writes .env files with pre-fetched short-lived tokens (not long-lived PATs), starts/stops runner containers via docker, supports per-repo and global operations.

## Key Claims
- RUNNER_TOKEN (short-lived, fetched per-session) vs ACCESS_TOKEN (long-lived PAT, must not be used)
- Runner token fetched via GitHub API: POST /repos/{owner}/{repo}/actions/runners/registration-token
- .env file written to ~/.ao-runner.d/{slug}/.env with chmod 0o600
- start-runner.sh script located at ~/.local/share/ao-runner/start-runner.sh
- Runner count, labels, ephemeral, disable_auto_update all configurable per repo
- Docker filter format: name=ao-runner-{slug} for ps/rm operations

## Connections
- [[jleechanclaw-canary]] — unrelated but both use Slack for different purposes
- [[jleechanclaw-pr-review-decision]] — unrelated but both interact with GitHub

## Contradictions
- None identified
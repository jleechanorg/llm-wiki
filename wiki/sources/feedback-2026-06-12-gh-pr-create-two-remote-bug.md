---
title: "gh pr create two-remote resolution bug + REST pulls workaround (2026-06-12)"
type: source
tags: [gh-cli, bug, two-remotes, fork, jleechanclaw, hermes-agent, rest-workaround, body-file, write-api-flake]
date: 2026-06-12
source_file: raw/feedback_2026-06-12_gh_pr_create_two_remote_bug.md
---

## Summary
In `~/.hermes` (and any clone with two remotes — `origin`=`jleechanorg/jleechanclaw` plus `hermes-agent`=`jleechanorg/hermes-agent`), `gh pr create` fails persistently with `GraphQL: Could not resolve to a Repository with the name 'jleechanorg/jleechanclaw'`, and `gh repo set-default` rejects the slug. This is a gh-CLI client-side bug in its batched base/head repo resolution across the fork chain, NOT a permissions or auth problem. Workaround: create the PR via the REST pulls endpoint.

## Key Claims
- `gh api repos/<owner>/<repo>`, `gh api graphql -f query=...`, and `git push` all work fine with the same keyring token — only `gh pr create` / `gh repo set-default` fail
- Workaround: `gh api --method POST repos/<owner>/<repo>/pulls -f title=... -f head=<branch> -f base=main -F body=@/tmp/body.md --jq '...'`
- `-F body=@file` reads the body from a file; to PATCH title/body later use `gh api --method PATCH ...`
- rtk shell wrapper mangles `cat > file <<'EOF'` heredocs and `wc -c < file` — heredoc content actually wrote, but `wc -c < file` reported `0`; write body files with the Write tool, verify with Read, not wc
- Transient GitHub write-API 404 incident: `POST/PATCH .../pulls` intermittently returned `{"message":"Not Found","status":"404"}` while GETs succeeded; a 404 response can still mutate server-side; list open PRs by head branch to get true state before retrying

## Key Quotes
> "This is a **gh-CLI client-side bug** in its batched base/head repo resolution across the fork chain, NOT a permissions or auth problem."

> "Always **list open PRs by head branch to get true state** before retrying, then retry the write with backoff (it cleared within ~minutes)."

## Connections
- [[GHCLITwoRemoteBug]] — fork-chain resolution failure
- [[RESTPullsWorkaround]] — bypass gh's remote resolution
- [[RTKHeredocBug]] — `cat > file <<'EOF'` + `wc -c < file` mangling
- [[GitHubWriteAPIFlake]] — 404-still-mutates transient incident
- [[PRWatchdog]] — PR #612 reference (Agnt-F SOUL mapping)

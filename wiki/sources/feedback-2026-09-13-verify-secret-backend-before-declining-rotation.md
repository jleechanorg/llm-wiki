---
title: "Verify a credential's actual storage backend before declining rotation"
type: source
tags: [security, credentials, github-actions, secret-rotation, anti-pattern]
date: 2026-09-13
source_file: feedback_2026-09-13_verify_secret_backend_before_declining_rotation.md
---

## Summary
During PR #9842 (worldarchitect.ai, Cloud Run cold-start fix), a live
`SMOKE_TOKEN` credential leaked into committed Cloud Logging evidence
captures. The agent initially told the user rotation was "outside agent
authority, no access to rotate production secrets" — an unverified
assumption that it was a GCP Secret Manager secret. Grepping the actual
usage site showed it is a GitHub Actions repository secret
(`secrets.SMOKE_TOKEN`), rotatable directly via `gh secret set` using access
already established in-session for PR operations.

## Key Claims
- "Production secret" is not one storage backend — GitHub Actions secrets, GCP Secret Manager, and plain env/dotfiles have completely different access models and different agent-authority implications.
- Only some credential backends are genuinely outside a session's existing write access; declining on an unverified label wastes the user's time and forces them to either do the rotation manually or push back.
- The concrete check: `grep -rn <SECRET_NAME> .github/workflows/ scripts/ <source>/` before declaring an action out of scope. `secrets.X` in a workflow → GitHub Actions secret, rotatable with `gh secret set`. `secretKeyRef` in a Cloud Run/K8s manifest → GCP Secret Manager, needs IAM/console access the session may genuinely lack.
- After rotating, the old value can still be live on already-running revisions until they're redeployed — for a dev/preview credential, triggering an immediate redeploy (`gh workflow run deploy-dev.yml`) closes that window rather than waiting for the next natural deploy.

## Key Quotes
> "why cant you rotate it?" — the user's pushback that prompted re-checking the assumption, which turned out to be wrong.

## Connections
- [[BrProjectConfigRegistryShadowing]] — same session, same underlying discipline: verify the actual resolved target/backend before acting on — or declining — an action, rather than trusting an assumption about where something lives.

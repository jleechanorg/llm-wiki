---
title: "Adding Anthropic API Key to GitHub Secrets"
type: source
tags: [github, secrets, anthropic, api-key, ci-cd]
sources: []
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary
Step-by-step guide for adding an Anthropic API key as a GitHub repository secret to enable Claude Code in PR workflows.

## Key Claims
- **Secret name must be exactly `ANTHROPIC_API_KEY`** (all caps, underscores)
- **API key format**: starts with `sk-ant-`
- **Secret type**: Repository secret (not Environment or Organization)
- **Testing**: After setup, comment `@claude help` on any PR to verify

## Key Steps
1. Navigate to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `ANTHROPIC_API_KEY`, Secret: `<your-api-key>`
4. Verify it appears in the secrets list

## Troubleshooting
- "Bad credentials" → re-check key, no extra spaces, regenerate if needed
- "Secret not found" → verify name is exact, check it's Repository not Organization
- Always check Actions tab for detailed error logs

## Security Notes
- GitHub Secrets are encrypted at rest
- Only accessible to workflows in the repo
- Rotate keys regularly for security
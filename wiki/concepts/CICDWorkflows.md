---
title: "CI/CD Workflows"
type: concept
tags: [cicd, automation, devops]
sources: [cloud-run-commit-sha-tracking]
last_updated: 2026-04-07
---

CI/CD Workflows automate the process of integrating code changes and deploying to production. This implementation uses GitHub Actions workflows (auto-deploy-dev.yml, deploy-production.yml) that automatically capture `GITHUB_SHA` for commit tracking during deployment.

## Workflow Components
1. **Trigger**: Push to main (dev) or release tags (production)
2. **Environment Variable**: `GITHUB_SHA` contains commit SHA
3. **Deployment**: Tags container with commit SHA
4. **Tracking**: Cloud Run labels preserve metadata

## Wiki Connections
- Referenced in: [[Cloud Run Commit SHA Tracking]]

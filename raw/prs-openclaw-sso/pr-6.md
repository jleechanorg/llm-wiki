# PR #6: feat(gcp): add Cloud Run deployment for gateway + relay services

**Repo:** jleechanorg/openclaw_sso
**Merged:** 2026-04-05
**Author:** jleechan2015
**Stats:** +2475/-39 in 49 files

## Summary
- **deploy.sh**: local/dev/staging/prod deploy script using `gcloud run deploy`
- **cloudbuild.yaml**: Cloud Build pipeline (shared → gateway → relay images to GCR)
- **deploy-dev.yml**: GitHub Actions — PR previews + main-branch pushes deploy to Cloud Run dev/staging
- **deploy-production.yml**: GitHub Actions — manual workflow_dispatch for prod with environment approval gate
- **smoke-test.yml** + **scripts/gcp-smoke-test.mjs**: E2E smoke test (gateway health + relay health + streaming error)


## Raw Body
## Summary

- **deploy.sh**: local/dev/staging/prod deploy script using `gcloud run deploy`
- **cloudbuild.yaml**: Cloud Build pipeline (shared → gateway → relay images to GCR)
- **deploy-dev.yml**: GitHub Actions — PR previews + main-branch pushes deploy to Cloud Run dev/staging
- **deploy-production.yml**: GitHub Actions — manual workflow_dispatch for prod with environment approval gate
- **smoke-test.yml** + **scripts/gcp-smoke-test.mjs**: E2E smoke test (gateway health + relay health + streaming error)
- **README.md**: one-time GCP setup, secrets reference, service URLs per environment

## Testing

- `npm test` (unit + integration) passes via existing `ci.yml`
- Local smoke test: `node scripts/gcp-smoke-test.mjs --gateway-url <url> --relay-url <url>`
- Manual smoke test workflow: `workflow_dispatch` with `gateway_url` + `relay_url` inputs

- GCP smoke test requires live Cloud Run services + Firebase credentials in Secret Manager
- Pre-production: run `scripts/gcp-smoke-test.mjs` against staging after first deploy

## Notes

- Reuses ai_universe deployment patterns (gcloud run deploy, Secret Manager, async Cloud Build, health check loops)
- Secrets `openclaw-firebase-sa-dev/prod`, `openclaw-relay-secret`, `openclaw-audit-hmac` must be created in GCP Secret Manager before first deploy
- Production requires `GCP_SA_KEY` GH Actions secret with Cloud Run + Secret Manager roles

- Closes bd-efsd

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **High Risk**
> High risk because it adds new authentication/token issuance paths and substantial production deployment automation (Cloud Run/Cloud Build) that could affect availability and security if misconfigured.
> 
> **Overview**
> Adds **end-to-end GCP deployment automation**: new `cloudbuild.yaml`, `deploy.sh`, and GitHub Actions workflows to build/push images and deploy gateway/relay to Cloud Run for dev/preview, staging, and production (with health checks, PR comm

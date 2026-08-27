---
title: "Canonical Cloud Run deploys must restore latest traffic"
type: source
tags: [cloud-run, deployment, traffic-routing, worldarchitect-ai, incident]
date: 2026-08-25
source_file: raw/feedback_2026-08-25_cloud_run_deploy_must_restore_latest_traffic.md
---

## Summary
An autoscaling experiment pinned `mvp-site-app-dev`'s base traffic to a named revision (`mvp-site-app-dev-04682-2zz`). The canonical auto-deploy pipeline kept creating new Ready revisions for newer commits, but they received 0% traffic because `spec.traffic` still named the pinned revision. The service URL health check returned 200 from the old routed revision, so CI reported deployment success while gameplay continued to run stale code. Fixed in PR #9398 (`scripts/deploy_common.sh` now passes `--to-latest`), verified live via `gcloud run services update-traffic --to-latest`.

## Key Claims
- A named-revision experiment pin on a Cloud Run service can survive past the experiment and silently block all subsequent "successful" deploys from ever serving traffic.
- Revision readiness, traffic routing, and endpoint resolution are three separate facts that must each be checked — a Ready revision or a 200 health check proves neither of the other two.
- Every normal/canonical Cloud Run deployment must explicitly pass `--to-latest` rather than relying on default traffic behavior.
- After any temporary named-revision routing experiment, `latestRevision: true` must be restored and asserted in a regression test — not just manually fixed once.

## Key Quotes
> "Do not infer user traffic from revision creation, readiness, or a service-URL health check when `spec.traffic` names a revision." — durable rule, feedback_2026-08-25_cloud_run_deploy_must_restore_latest_traffic.md

> "1. a revision was created and is Ready; 2. traffic is actually routed to that revision; and 3. the endpoint under test resolves to that routed revision." — reusable pattern for Cloud Run routing investigations

## Fix and Verification
- FIX: `scripts/deploy_common.sh` adds `--to-latest` to canonical deployment arguments (2026-08-25 PT), merged via PR #9398, commit `e919ab53f2c1f2138ea1ea6b1363cb977c3bcde6`.
- `scripts/tests/test_shared_config_concurrency_defaults.sh` stubs `gcloud` and asserts the canonical deployment includes `--to-latest`; full scoped script passed 25 checks.
- Live repair: `gcloud run services update-traffic mvp-site-app-dev --to-latest --region=us-central1 --project=worldarchitecture-ai`, verified 100% latest traffic on `mvp-site-app-dev-04773-zks` and a healthy service endpoint.

## Connections
- [[CloudRun]] — the platform where this traffic-routing failure occurred
- [[GoogleCloudRun]] — deployment target; canonical deploy scripts live in `scripts/deploy_common.sh`
- [[CloudRunTrafficRouting]] — new concept capturing the revision/traffic/endpoint distinction
- [[DeploymentValidation]] — related deployment-correctness discipline

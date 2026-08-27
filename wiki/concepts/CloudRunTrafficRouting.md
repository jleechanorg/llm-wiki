---
title: "Cloud Run Traffic Routing"
type: concept
tags: [cloud-run, deployment, traffic-routing, devops]
sources: [feedback-2026-08-25-cloud-run-deploy-must-restore-latest-traffic]
last_updated: 2026-08-25
---

Cloud Run separates three facts that are easy to conflate when verifying a deployment:

1. **Revision created and Ready** — the new code built and passed health checks.
2. **Traffic routed to that revision** — `spec.traffic` / `status.traffic` actually assign percentage to it.
3. **Endpoint resolves to the routed revision** — the service URL under test is hitting the revision traffic claims to serve.

A Ready revision or a 200 response from the service URL proves only fact 1 (and weakly fact 3) — never fact 2. If `spec.traffic` names a specific revision (e.g. left over from an autoscaling/canary experiment), newer Ready revisions can sit at 0% traffic indefinitely while CI reports deploy success and the running service silently serves stale code.

## Durable Rule
Canonical/normal deploys must explicitly pass `--to-latest` (`gcloud run deploy ... --to-latest` or `gcloud run services update-traffic --to-latest`) rather than relying on default traffic behavior. After any temporary named-revision routing experiment, restore `latestRevision: true` and assert it in a regression test — not just fix it once manually.

## Incident
WorldArchitect.AI's `mvp-site-app-dev` had `spec.traffic` pinned to `mvp-site-app-dev-04682-2zz` by an autoscaling experiment. The canonical auto-deploy kept creating Ready revisions at 0% traffic for every subsequent commit; health checks passed against the old pinned revision. Fixed by adding `--to-latest` to `scripts/deploy_common.sh` (PR #9398) and repairing live traffic via `gcloud run services update-traffic --to-latest`.

## Related
- [[CloudRun]] — platform this applies to
- [[GoogleCloudRun]] — WorldArchitect.AI's Cloud Run deployment target
- [[DeploymentValidation]] — broader deployment-correctness discipline

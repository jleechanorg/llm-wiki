---
name: Canonical Cloud Run deploys must restore latest traffic
description: A named-revision experiment pin can make ready deployments serve 0 percent of user traffic.
type: feedback
bead: rev-jcszt
---

# Canonical Cloud Run deploys must restore latest traffic

Classification: Mandatory

## Context

An autoscaling experiment explicitly set `mvp-site-app-dev` base traffic to
`mvp-site-app-dev-04682-2zz`. The canonical auto-deploy then created ready
revisions for newer commits at 0% traffic. Its URL health check returned 200
from the old routed revision, so CI reported deployment success while gameplay
continued to execute stale code.

## Durable rule

Every normal Cloud Run deployment must explicitly pass `--to-latest`. Do not
infer user traffic from revision creation, readiness, or a service-URL health
check when `spec.traffic` names a revision. Verify both `spec.traffic` and
`status.traffic` after any experiment or deployment that can change routing.

## Fix and verification

FIX: `scripts/deploy_common.sh` adds `--to-latest` in canonical deployment
arguments (2026-08-25 PT), merged by PR #9398 as
`e919ab53f2c1f2138ea1ea6b1363cb977c3bcde6`.

`scripts/tests/test_shared_config_concurrency_defaults.sh` stubs `gcloud` and
asserts canonical deployment includes `--to-latest`; the full scoped script
passed 25 checks. The live repair ran `gcloud run services update-traffic
mvp-site-app-dev --to-latest --region=us-central1 --project=worldarchitecture-ai`.
It verified 100% latest traffic on `mvp-site-app-dev-04773-zks` and a healthy
service endpoint.

## Reusable pattern

For Cloud Run routing investigations, treat these as separate facts:

1. a revision was created and is Ready;
2. traffic is actually routed to that revision; and
3. the endpoint under test resolves to that routed revision.

After any temporary named-revision routing, restore `latestRevision: true` and
assert it in the deployment adapter's regression test.

---
name: Gemini shared-cache measurement roadmap
beschreibung: Measurement-first disposition for PR 7263 shared Gemini cache
# description kept ASCII-compatible below for index readability
description: PR 7263 cache mechanism works, but production savings need Cloud Logging hit-rate and BigQuery billing proof before merge-as-cost-reduction.
type: project
bead: rev-9piwk
---

PR #7263's shared system/tools Gemini cache is working engineering, but not proven hard-dollar production cost reduction. The 74.6% evidence is a real explicit-cache token discount measured with per-campaign cache disabled; stable production may already have per-campaign cache on warm turns, while the shared cache is only fall-through and excludes the 89% test/CI cost center.

Measurement roadmap: first add/read Cloud Logging hit-rate metrics (`SHARED_CACHE_USED`, `shared_cache HIT`, `shared_cache CREATED`, `SHARED_CACHE_FALLTHROUGH_FAILED`), then reconcile post-merge day windows with BigQuery Billing Export cached-input/cache-storage SKUs. Do not claim dollar savings until logs and billing agree net of storage.

**Why:** Prior cache work over-relied on token-proxy A/Bs and non-prod baselines; the next decision must compare against deployed stable config and measured traffic mix.

**How to apply:** When reviewing or merging shared-cache PRs, require baseline fidelity, realtime hit-rate telemetry, and delayed billing export reconciliation. Frame PR #7263 as experiment/building block unless hard-dollar proof exists.

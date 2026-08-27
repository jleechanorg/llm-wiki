# WorldArchitect Cloud Run capacity centralization

Source: worldarchitect.ai PR 9330, exact head
`bcb6391943dafc59d934f95da3091207b6e429dc`.

The repository centralizes all app-service Cloud Run capacity in
`scripts/shared_config.sh` and routes dev, staging, stable/production, preview,
and preview-pool bootstrap through
`deploy_common::deploy_worldarchitect_service`. Capacity values are readonly,
hostile incoming values are replaced, repeated sourcing is idempotent, and a
conflicting already-readonly value fails closed. Documentation points to the
canonical deployment skill instead of copying capacity flags.

Preview failure handling deliberately retains reservation labels. Removing them
after a failed old job is unsafe because the pool may already have reassigned
the service to a newer PR; normal eviction reclaims stale reservations.

The unified CPU8/16Gi/concurrency180/workers1/threads180 profile is an explicit
aggressive-learning choice. It does not prove zero-error operation,
memory-heavy safety, deterministic autoscaling timing, or non-dev runtime
validation.

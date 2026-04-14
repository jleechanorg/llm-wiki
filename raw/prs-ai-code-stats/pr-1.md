# PR #1: Add linked table of contents to ProdLens design evaluation

**Repo:** jleechanorg/ai_code_stats
**Merged:** 2025-10-12
**Author:** jleechan2015
**Stats:** +148/-0 in 1 files
**Labels:** codex

## Summary
- convert the table of contents into a linked markdown list so readers can jump directly to each section
- enumerate subsections under each primary heading to ensure coverage of ingestion, caching, analytics, deployment, and operational topics is visible from the contents

## Raw Body
## Summary
- convert the table of contents into a linked markdown list so readers can jump directly to each section
- enumerate subsections under each primary heading to ensure coverage of ingestion, caching, analytics, deployment, and operational topics is visible from the contents

## Testing
- not run (documentation only)


------
https://chatgpt.com/codex/tasks/task_e_68eb093f3bc0832f960f8f899756b115

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> Adds a comprehensive ProdLens MVP v1.2 design evaluation doc with linked TOC detailing metrics, ingestion, storage, analytics, deployment, integrations, and pilot plan aligned to Dev-Agent-Lens.
> 
> - **Documentation**:
>   - Adds `dev-agent-lens/docs/prodlens-mvp-v1_2-design-eval.md` outlining:
>     - **Metrics**: Explicit daily KPIs (latency, acceptance, model selection, error/token efficiency, PR/commit/merge/rework, lagged correlations).
>     - **Ingestion & Tracing**: Use of `claude-lens` via LiteLLM proxy; OpenTelemetry spans to Arize/Phoenix; normalization to canonical schema persisted as parquet/SQLite with validation/DLQ.
>     - **Storage/Caching**: SQLite-backed GitHub ETL with ETags/checkpoints; indexed cache tables and `etl_runs`.
>     - **Analytics**: Python CLI `prod-lens report` with pandas/scipy/difflib; lagged Pearson/Spearman, sample-size notes, BH correction, optional visuals.
>     - **Deployment**: Docker Compose profiles (Arize/Phoenix), env/setup/Make targets, profile detection, reproducibility guidance.
>     - **Integrations**: LiteLLM proxy API, OpenTelemetry exporters, GitHub REST, SDK hooks (Python/TypeScript), optional FastAPI webhook.
>     - **Pipeline**: End-to-end steps from session capture to reporting/feedback.
>     - **Pilot Plan**: Setup, daily runs, success criteria, stakeholder reviews.
>     - **Risk Mitigation**: Data quality, privacy, scalability, API limits, change management.
>     - **Roadmap & Deliverables**: v1.3 targets, testing strategy, dashboards, requirements/env docs

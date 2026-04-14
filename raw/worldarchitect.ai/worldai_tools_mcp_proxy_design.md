# WorldAI Tools MCP Proxy Design

Status: Proposed (design-only)
Date: 2026-03-03
Owner: Platform / MCP

## Table of Contents

- [Grounding In Existing Repository Files](#grounding-in-existing-repository-files)
- [Goals](#goals)
- [Non-Goals](#non-goals)
- [Architecture Overview](#architecture-overview)
- [Components](#components)
- [Tool Catalog](#tool-catalog)
  - [A. Passthrough Existing WorldAI MCP Tools](#a-passthrough-existing-worldai-mcp-tools)
  - [B. New Diagnostic/Admin Tools](#b-new-diagnosticadmin-tools)
  - [C. GCP/Firebase Ops Tools (Guardrailed)](#c-gcpfirebase-ops-tools-guardrailed)
- [AuthN / AuthZ Model](#authn--authz-model)
- [Safety Model](#safety-model)
- [Data Flows](#data-flows)
- [Rate Limiting](#rate-limiting)
- [Observability](#observability)
- [Local / Production Deploy Model](#local--production-deploy-model)
- [Decision Required Before Phase 1](#decision-required-before-phase-1)
- [Rollout Plan](#rollout-plan)
- [Phased Implementation Plan](#phased-implementation-plan)
- [Phased Test Plan](#phased-test-plan)
- [Compatibility Notes](#compatibility-notes)
- [Open Questions](#open-questions)

## Grounding In Existing Repository Files

This design is intentionally grounded in current behavior from:
- [`mvp_site/mcp_api.py`](../mvp_site/mcp_api.py): existing MCP tool/resource schemas and JSON-RPC handlers (`tools/list`, `tools/call`, `resources/list`, `resources/read`), plus auth-derived `user_id` injection behavior.
- [`mvp_site/mcp_client.py`](../mvp_site/mcp_client.py): JSON-RPC client shape, `/mcp` path convention, timeout defaults, and non-idempotent POST retry constraints.
- [`mvp_site/firestore_service.py`](../mvp_site/firestore_service.py): Firestore access patterns (`get_db`, campaign reads, game state reads, user settings APIs).
- [`scripts/copy_campaign.py`](../scripts/copy_campaign.py): campaign copy semantics and subcollection behavior (`story`, `game_states`, `notes`, `characters`).
- [`scripts/download_campaign.py`](../scripts/download_campaign.py): campaign export behavior and file generation patterns (story + game state artifacts).
- [`scripts/audit_dice_rolls.py`](../scripts/audit_dice_rolls.py): dice audit extraction logic, statistical analysis outputs, and warning model.
- [`scripts/start_mcp_production.sh`](../scripts/start_mcp_production.sh): production MCP startup path using dual transport.
- [`scripts/start_mcp_server.sh`](../scripts/start_mcp_server.sh): local MCP startup modes and port-driven execution pattern.
- [`scripts/setup_production_env.sh`](../scripts/setup_production_env.sh): production env hardening (`PRODUCTION_MODE=true`, mock/testing cleanup).
- [`scripts/server-config.sh`](../scripts/server-config.sh) and [`scripts/server-utils.sh`](../scripts/server-utils.sh): port management and service utility conventions.
- [`scripts/debug_firebase_connection.py`](../scripts/debug_firebase_connection.py): Firebase/Firestore diagnostic patterns.
- [`scripts/investigate_campaign_issues.py`](../scripts/investigate_campaign_issues.py): campaign diagnosis patterns for dice/god-mode issues.
- [`scripts/README_MCP.md`](../scripts/README_MCP.md): MCP operational expectations in repo scripts/docs.

## Goals

1. Provide an MCP proxy that exposes all existing WorldAI MCP tools from the real upstream MCP server without tool-by-tool rewrites.
2. Add safe diagnostic/admin tools for:
   - Dice evaluation.
   - Copy campaign from one user to another.
   - Download campaign artifacts.
   - Download specific campaign entries.
3. Enforce download behavior: artifacts are written only under a resolved local Downloads root (`$HOME/Downloads` on Unix/macOS; `%USERPROFILE%\Downloads` on Windows), and tool responses return path/metadata only (no file body payloads).
4. Add controlled GCP/Firebase operations tools for:
   - `gcloud` log reads.
   - Firestore read/query helpers.
   - Run/deploy controls for local/prod MCP services.
5. Preserve compatibility with existing repo conventions and deployment scripts.

## Non-Goals

1. Replacing or changing business logic in `mvp_site/world_logic.py`, `mvp_site/mcp_api.py`, or game mechanics.
2. Replacing existing HTTP API routes in `mvp_site/main.py`.
3. Introducing broad write-capable Firestore admin tools beyond explicitly scoped campaign copy.
4. Returning raw downloaded content in MCP responses.
5. Implementing this design in this document.

## Architecture Overview

The proxy runs as its own MCP server and forwards unknown tools/resources to the real WorldAI MCP server. It hosts a small set of local admin/diagnostic/ops tools.

```text
+-------------------------+        JSON-RPC over /mcp        +---------------------------+
| MCP Client (Claude/etc) |  ------------------------------>  | WorldAI Tools MCP Proxy   |
|                         |                                   | (new server)              |
+-------------------------+                                   |                           |
                                                              | 1) Passthrough Layer      |
                                                              |    - tools/list merge     |
                                                              |    - tools/call forward   |
                                                              |    - resources passthrough|
                                                              |                           |
                                                              | 2) Local Tool Layer       |
                                                              |    - diag_*               |
                                                              |    - admin_*              |
                                                              |    - ops_*                |
                                                              +-------------+-------------+
                                                                            |
                         +--------------------------------------------------+--------------------------+
                         |                                                                             |
          upstream MCP (real game tools)                                                local admin integrations
+------------------------------------------------------+                   +----------------------------------------------+
| WorldAI MCP Server (`mvp_site/mcp_api.py` via /mcp) |                   | Firestore + scripts + gcloud command wrappers |
+------------------------------------------------------+                   +----------------------------------------------+
```

## Components

1. Proxy MCP server process (`worldai_tools_mcp_proxy` module, planned).
2. Upstream connector:
   - Uses `mvp_site/mcp_client.py` JSON-RPC conventions.
   - No automatic retries for non-idempotent tool calls.
3. Local tool executor:
   - Safe wrappers around existing script logic and Firestore read helpers.
4. Policy engine:
   - AuthN/AuthZ checks.
   - Path restrictions for artifacts.
   - Command allowlist + parameter validation.
5. Observability layer:
   - Unified logger and structured audit events.

## Tool Catalog

### A. Passthrough Existing WorldAI MCP Tools

Proxy must expose all tools returned by upstream `tools/list` dynamically.

Minimum known baseline (from current `mvp_site/mcp_api.py`):
- `create_campaign(user_id, title, character?, setting?, description?, selected_prompts?, custom_options?, god_mode?)`
- `get_campaign_state(user_id, campaign_id)`
- `process_action(user_id, campaign_id, user_input, mode?)`
- `update_campaign(user_id, campaign_id, updates)`
- `export_campaign(user_id, campaign_id, format)`
- `get_campaigns_list(user_id, limit?, sort_by?)`
- `get_user_settings(user_id)`
- `update_user_settings(user_id, settings)`
- Optional: `roll_dice(notation?, purpose?)` when enabled upstream.

Passthrough signature contract:
```json
{
  "name": "<any upstream tool name>",
  "arguments": {"...": "forwarded unchanged except auth-derived user_id policy"}
}
```

Result contract:
- Return upstream `result` unchanged unless redaction policy applies.
- Preserve upstream JSON-RPC error code/message.

### B. New Diagnostic/Admin Tools

Tool naming is prefixed to avoid collisions.

Collision policy:
- Upstream tools keep original names as returned by upstream `tools/list`.
- Local proxy-owned tools are reserved under `diag_`, `admin_`, `ops_`.
- If upstream ever introduces a reserved-prefix tool name, proxy startup fails fast with a collision error until one side is renamed/versioned.

1. `diag_evaluate_campaign_dice`

Signature:
```json
{
  "campaign_id": "string",
  "include_recent": "integer (default 20, max 100)",
  "save_report": "boolean (default false)"
}
```

Behavior:
- Reuses logic pattern from `scripts/audit_dice_rolls.py`.
- Returns summary stats, warnings, and recent roll metadata.
- If `save_report=true`, writes JSON report under `<DOWNLOADS_ROOT>/worldai_dice_audits/` and returns path metadata.

Response:
```json
{
  "campaign_id": "string",
  "summary": {
    "total_rolls": "integer",
    "entries_with_dice": "integer",
    "by_source": {"source": "count"}
  },
  "warnings": ["string"],
  "report_artifact": {
    "path": "string",
    "bytes": "integer",
    "sha256": "string"
  }
}
```

2. `admin_copy_campaign_user_to_user`

Signature:
```json
{
  "source_user_id": "string",
  "reason": "string (required)",
  "ticket_id": "string (required)",
  "source_campaign_id": "string",
  "dest_user_id": "string",
  "suffix": "string (default '(copy)')",
  "dry_run": "boolean (default true)"
}
```

Behavior:
- Mirrors semantics from `scripts/copy_campaign.py`.
- Copies campaign document and subcollections (`story`, `game_states`, `notes`, `characters`).
- `dry_run=true` returns copy plan/counts only.

Response:
```json
{
  "dry_run": "boolean",
  "new_campaign_id": "string|null",
  "copied_counts": {
    "campaign": "integer",
    "story": "integer",
    "game_states": "integer",
    "notes": "integer",
    "characters": "integer"
  }
}
```

3. `admin_download_campaign`

Signature:
```json
{
  "target_user_id": "string",
  "campaign_id": "string",
  "reason": "string (required)",
  "ticket_id": "string (required)",
  "format": "string (txt|docx|pdf, default txt)",
  "include_game_state": "boolean (default true)"
}
```

Behavior:
- Reuses export behavior from `scripts/download_campaign.py` and `firestore_service.get_campaign_by_id/get_campaign_game_state`.
- Writes artifacts to `<DOWNLOADS_ROOT>/worldai_campaign_exports/<timestamp>/`.
- Never returns file contents.

Response:
```json
{
  "campaign_id": "string",
  "artifacts": [
    {
      "kind": "story|game_state",
      "path": "string",
      "bytes": "integer",
      "sha256": "string",
      "mime_type": "string"
    }
  ],
  "entry_count": "integer"
}
```

4. `admin_download_campaign_entries`

Signature:
```json
{
  "target_user_id": "string",
  "campaign_id": "string",
  "reason": "string (required)",
  "ticket_id": "string (required)",
  "entry_ids": ["string"] (mutually exclusive with time-window parameters),
  "from_timestamp": "string (ISO8601) (mutually exclusive with entry_ids)",
  "to_timestamp": "string (ISO8601) (required if using time-window)",
  "limit": "integer (default 500, max 5000)",
  "format": "string (json|jsonl, default jsonl)"
}
```

Behavior:
- Fetches selected entries from `users/{uid}/campaigns/{cid}/story`.
- Supports either explicit `entry_ids` OR a time-window (`from_timestamp` + `to_timestamp`), but not both in one request.
- Writes output file only under `<DOWNLOADS_ROOT>/worldai_campaign_entries/`.
- Returns metadata only.

Response:
```json
{
  "campaign_id": "string",
  "entries_written": "integer",
  "artifact": {
    "path": "string",
    "bytes": "integer",
    "sha256": "string",
    "format": "json|jsonl"
  }
}
```

### C. GCP/Firebase Ops Tools (Guardrailed)

1. `ops_gcloud_logs_read`

Signature:
```json
{
  "service": "string",
  "project_id": "string (must be in WORLDTOOLS_GCLOUD_PROJECT_ALLOWLIST)",
  "reason": "string (required)",
  "ticket_id": "string (required)",
  "lookback_minutes": "integer (default 60, max 1440)",
  "limit": "integer (default 100, max 500)",
  "severity": "string|null",
  "contains": "string|null"
}
```

Behavior:
- Executes allowlisted `gcloud logging read` command variants only.
- Read-only.
- Returns parsed metadata/messages with redaction.

2. `ops_firestore_read_document`

Signature:
```json
{
  "document_path": "string (must match allowlisted prefixes)",
  "reason": "string (required)",
  "ticket_id": "string (required)",
  "field_mask": ["string"]
}
```

Behavior:
- Read-only Firestore document fetch.
- Uses `firestore_service.get_db()` initialization pattern.
- Only allows approved path prefixes (for example: `users/{uid}/campaigns/*`, `users/{uid}/settings/*`); rejects all other roots by default.
- Redacts sensitive settings fields (`*_api_key`, tokens).

3. `ops_firestore_query_collection_group`

Signature:
```json
{
  "collection_group": "string",
  "reason": "string (required)",
  "ticket_id": "string (required)",
  "filters": [
    {"field": "string", "op": "string", "value": "any"}
  ],
  "order_by": "string|null",
  "limit": "integer (default 50, max 200)"
}
```

Behavior:
- Read-only scoped query helper.
- Enforces small limits and query timeout.

4. `ops_run_mcp_local`

Signature:
```json
{
  "mode": "string (dual|http-only|stdio-only)",
  "reason": "string (required)",
  "ticket_id": "string (required)",
  "port": "integer (default 8081)",
  "dry_run": "boolean (default true)"
}
```

Behavior:
- Wraps `scripts/start_mcp_server.sh` semantics.
- `dry_run=true` returns command plan only.
- `dry_run=false` starts background process and returns pid/log path.

5. `ops_run_mcp_production`

Signature:
```json
{
  "dry_run": "boolean (default true)",
  "reason": "string (required)",
  "ticket_id": "string (required)"
}
```

Behavior:
- Wraps `scripts/setup_production_env.sh` + `scripts/start_mcp_production.sh` behavior.
- Requires elevated authorization role.

6. `ops_deploy_mcp_service`

Signature:
```json
{
  "target": "string (preview|prod)",
  "service": "string",
  "region": "string",
  "image": "string",
  "revision_suffix": "string|null",
  "confirm": "string (exact: CONFIRMED or DEPLOY-{target}-{YYYYMMDD-HHMMSS})",
  "reason": "string (required)",
  "ticket_id": "string (required)"
}
```

Behavior:
- Controlled wrapper for allowlisted deploy command chain (`gcloud run deploy ...`).
- Requires explicit confirmation token and deploy role.
- Confirmation validation is case-sensitive and target-aware (`target` must match token target segment).
- Example valid token: `DEPLOY-prod-20260303-091500`.
- Returns command transcript metadata.

## AuthN / AuthZ Model

### Authentication

1. Accept Firebase Bearer token as primary auth for production, consistent with `mvp_site/main.py` behavior.
2. Preserve non-production local bypass behavior only for explicitly configured local/dev mode.
3. Preserve preview smoke-token path only for preview environments where applicable.
4. Never trust caller-supplied `user_id` for passthrough gameplay tools when authenticated identity exists.
5. For admin tools, caller identity comes from auth context while target identity is explicitly modeled as `target_user_id` or source/destination IDs in the tool schema.

### Authorization

Role model:
- `player`: can use passthrough gameplay tools scoped to own user context.
- `support_admin`: can use diagnostic and download tools for support workflows.
- `ops_admin`: can use GCP/Firebase read ops and local run tools.
- `deploy_admin`: can invoke deploy/run production tools.

Role sources:
- Firebase custom claims first (canonical claims: `worldtools_roles.support_admin`, `worldtools_roles.ops_admin`, `worldtools_roles.deploy_admin`).
- Optional fallback allowlists from env vars for controlled bootstrap:
  - `WORLDTOOLS_SUPPORT_ADMINS`: comma-separated lowercase emails (spaces allowed, trimmed), e.g. `alice@example.com,bob@example.com`
  - `WORLDTOOLS_OPS_ADMINS`: comma-separated lowercase emails (spaces allowed, trimmed), e.g. `ops1@example.com,ops2@example.com`
  - `WORLDTOOLS_DEPLOY_ADMINS`: comma-separated lowercase emails (spaces allowed, trimmed), e.g. `release1@example.com,release2@example.com`

Allowlist bootstrap and fail-closed behavior:
- Parse allowlist env vars at startup (`split(',')`, trim, lowercase, dedupe).
- Missing allowlists are permitted only for local/dev mode; in production mode, `ops_*`/`deploy_*` tools remain disabled unless relevant allowlists or claims mappings are present.
- `WORLDTOOLS_GCLOUD_PROJECT_ALLOWLIST` is required for `ops_gcloud_logs_read` enablement in production (comma-separated project IDs). If empty/missing in production, that tool is disabled by policy.

Policy enforcement:
- Inject/override `user_id` only on passthrough tools that require caller identity.
- `admin_*` and `ops_*` tools must include `reason` and `ticket_id`; requests missing either field are rejected.

## Safety Model

1. Namespace isolation:
   - Local tools use reserved prefixes `diag_`, `admin_`, `ops_`.
2. Command allowlist:
   - `ops_*` command execution is template-based, never arbitrary shell.
3. Artifact write boundary:
   - Canonicalize path and enforce prefix under `<DOWNLOADS_ROOT>` (`$HOME/Downloads` Unix/macOS, `%USERPROFILE%\Downloads` Windows).
   - Reject symlink escape or `..` traversal.
4. Response data minimization:
   - Download tools return metadata only, never file body.
   - Logs/firestore reads redact secrets (`authorization`, `*_api_key`, tokens).
5. High-risk action gates:
   - `ops_deploy_mcp_service` requires `confirm` token format, deploy role, and optional two-step confirm mode.
6. Timeouts:
   - Use repo timeout guardrail (600s request max) as hard ceiling.
   - Per-tool shorter defaults (e.g., logs read 60s, Firestore query 30s).
7. Idempotency handling:
   - No automatic retries for write paths (`admin_copy_campaign_user_to_user`, deploy actions), aligned with `mcp_client.py` POST policy.

## Data Flows

### Flow 1: Passthrough Gameplay Tool

1. Client calls proxy `tools/call` with gameplay tool.
2. Proxy authenticates user and injects authoritative `user_id` only for passthrough gameplay tools that expect caller identity.
3. Proxy forwards JSON-RPC to upstream `/mcp`.
4. Proxy returns upstream result unchanged except redaction/audit metadata.

### Flow 2: Campaign Copy (Admin)

1. Admin calls `admin_copy_campaign_user_to_user` with `dry_run=true`.
2. Proxy validates role and fetches source campaign/subcollection counts.
3. Proxy returns execution plan.
4. Admin re-calls with `dry_run=false`.
5. Proxy performs copy transaction-like sequence and returns new campaign ID + counts.

### Flow 3: Campaign Download

1. Admin calls `admin_download_campaign`.
2. Proxy reads campaign + story + game state using Firestore service patterns.
3. Proxy writes files under `<DOWNLOADS_ROOT>/worldai_campaign_exports/...`.
4. Proxy returns only path/bytes/hash/metadata.

### Flow 4: GCP Logs Read

1. Ops admin calls `ops_gcloud_logs_read`.
2. Proxy validates args and builds allowlisted command.
3. Proxy executes read-only command with timeout.
4. Proxy redacts sensitive fields and returns parsed entries.

## Rate Limiting

Rate limiting is internal to proxy tool execution, independent from route-level limiter exemptions.

Proposed defaults:
- Passthrough gameplay tools: 60 calls/min per user, burst 20.
- Diagnostic/download admin tools: 10 calls/min per admin, concurrency 2.
- Firestore/logs ops tools: 6 calls/min per admin, concurrency 2.
- Deploy/run-prod tools: 1 call/15 min globally and per admin.

Additional controls:
- Max payload size for `tools/call` arguments.
- Queue depth cap for long-running admin/ops tasks.
- Circuit-breaker behavior for repeated upstream failures.

## Observability

Logging:
- Use unified logger conventions (`logging_util.setup_unified_logging(...)`).
- Emit structured fields: `request_id`, `tool_name`, `role`, `actor_user_hash`, `latency_ms`, `status`, `upstream_status`.

Metrics:
- `proxy_tool_calls_total{tool,status}`
- `proxy_tool_latency_ms{tool}`
- `proxy_upstream_errors_total{code}`
- `proxy_admin_actions_total{tool}`
- `proxy_artifacts_written_total{tool}`
- `proxy_artifact_bytes_total{tool}`

Audit trail:
- For `admin_*` and `ops_*`, persist an append-only audit event including requester, reason, ticket, parameters hash, and outcome.
- Primary sink: Cloud Logging structured audit stream (`worldtools_audit`).
- Optional secondary sink: Firestore collection `worldtools_audit_events` for support search/retention workflows.
- In production mode, if audit sink initialization fails, `admin_*` and `ops_*` tools fail closed.

Tracing:
- Propagate correlation/request IDs from client headers when available.

## Local / Production Deploy Model

### Local

1. Upstream MCP server runs locally using script patterns from `scripts/start_mcp_server.sh`.
2. Proxy runs as separate local MCP process and points to local upstream `/mcp`.
3. Use `scripts/server-config.sh` and `scripts/server-utils.sh` port utilities for conflict handling.
4. Download artifacts always land in local `<DOWNLOADS_ROOT>`.

### Production

1. Environment setup follows `scripts/setup_production_env.sh` semantics (`PRODUCTION_MODE=true`, mock/testing vars unset).
2. Upstream MCP production startup follows `scripts/start_mcp_production.sh` pattern.
3. Proxy is deployed as a separate service only (per phase-gate decision below).
4. Production deploy actions are gated via `ops_deploy_mcp_service` and authorization controls.


## Decision Required Before Phase 1

Decision: **Use a separate MCP proxy service deployment model** (not embedded into the existing Flask `/mcp` route).

Rationale:
- Isolates operational/admin tool risk from gameplay MCP runtime.
- Allows independent scaling and tighter IAM/service-account boundaries.
- Keeps passthrough parity and operational concerns decoupled for testing/release.

Artifact strategy implication:
- Artifact-producing tools (`diag_*` report saves and `admin_*` downloads) are **local/support execution only** in this design and write to `<DOWNLOADS_ROOT>`.
- In production-hosted deployments, these artifact-producing tools are disabled unless a future design explicitly introduces object storage semantics.

Security/scaling/testing implication:
- Separate service permits stricter authz on `admin_*`/`ops_*` without risking existing gameplay path behavior.
- Phase 1 validation must include upstream passthrough parity and explicit checks that artifact-producing local tools are disabled in production mode.

## Rollout Plan

1. Stage 0: Design and schema freeze.
2. Stage 1: Read-only passthrough proxy (no admin tools), shadow validation against existing upstream.
3. Stage 2: Add `diag_*` and download tools with artifact boundary enforcement.
4. Stage 3: Add campaign copy tool with dry-run default and audit logging.
5. Stage 4: Add read-only `ops_*` tools (logs + Firestore reads).
6. Stage 5: Add controlled run/deploy ops tools behind deploy-admin role.
7. Stage 6: Harden limits/observability and promote to default support endpoint.

## Phased Implementation Plan

### Phase 1: Proxy Core

Deliverables:
- MCP server skeleton.
- Upstream connector.
- Dynamic tool/resource passthrough.
- Auth-derived `user_id` override for passthrough tools.

Exit criteria:
- `tools/list` parity with upstream.
- `tools/call` parity for baseline tools.

### Phase 2: Diagnostic + Download

Deliverables:
- `diag_evaluate_campaign_dice`.
- `admin_download_campaign`.
- `admin_download_campaign_entries`.
- Artifact metadata response formatter and hash utility.

Exit criteria:
- Verified writes constrained to `<DOWNLOADS_ROOT>`.
- No file body leakage in responses.

### Phase 3: Campaign Copy

Deliverables:
- `admin_copy_campaign_user_to_user` with dry-run default.
- Subcollection copy counters.
- Audit events.

Exit criteria:
- Copy correctness for all targeted subcollections.
- Idempotency/duplicate-call behavior documented and tested.

### Phase 4: Ops Read Tools

Deliverables:
- `ops_gcloud_logs_read` allowlisted command wrapper.
- `ops_firestore_read_document`.
- `ops_firestore_query_collection_group`.

Exit criteria:
- No arbitrary shell execution path.
- Sensitive fields redacted.

### Phase 5: Ops Run/Deploy

Deliverables:
- `ops_run_mcp_local`.
- `ops_run_mcp_production`.
- `ops_deploy_mcp_service` with confirmation guardrails.

Exit criteria:
- Role-gated execution only.
- Full audit event coverage.

## Phased Test Plan

1. Unit tests:
   - Tool routing (passthrough vs local namespace).
   - AuthZ matrix by role/tool.
   - Path normalization and `<DOWNLOADS_ROOT>` boundary checks.
   - Redaction logic.
   - Rate-limit behavior.

2. Integration tests:
   - JSON-RPC passthrough parity with upstream for baseline tools.
   - Download artifacts created and metadata accurate.
   - Campaign copy creates expected target docs/subcollections.
   - Firestore/log tools return bounded read-only outputs.

3. Operational tests:
   - Local startup and port conflict behavior.
   - Production-mode auth hardening behavior.
   - Timeout and cancellation behavior for long operations.

4. Safety tests:
   - Attempted path traversal in download filenames.
   - Unauthorized role attempts for `admin_*` and `ops_*`.
   - Deploy tool invocation without confirmation token.

5. Evidence expectations:
   - Keep tests deterministic and aligned with repo policy.
   - For `testing_mcp/` and `testing_ui/`, run in real-service mode per repo policy.

## Compatibility Notes

1. Keep imports module-level only.
2. Use unified logging utility in `mvp_site` modules.
3. Reuse existing script/service logic rather than duplicating export/copy/audit behavior.
4. Keep JSON-RPC protocol contracts compatible with current `/mcp` endpoint behavior.
5. Preserve production security posture (`PRODUCTION_MODE=true` behavior, no broad bypass paths).

## Open Questions

1. Should deploy tools be disabled by default in production and enabled only in preview/ops projects?
2. Should admin audit events be stored only in logs or also in Firestore for retention/search?
3. Should campaign copy support selective subcollections in addition to full copy?


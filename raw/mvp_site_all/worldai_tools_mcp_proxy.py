"""WorldAI Tools MCP Proxy runtime.

This service exposes local diagnostic/admin/ops MCP tools and forwards all
other tools/resources to an upstream WorldAI MCP server.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import traceback
from dataclasses import dataclass
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import requests

from mvp_site import document_generator, firestore_service, logging_util

MAX_REQUEST_SIZE = int(os.getenv("WORLDTOOLS_PROXY_MAX_CONTENT_LENGTH", str(10 * 1024 * 1024)))

RESERVED_PREFIXES = ("diag_", "admin_", "ops_")
SENSITIVE_FIELD_PATTERN = re.compile(r"(authorization|token|api[_-]?key|secret)", re.I)
DEPLOY_CONFIRM_RE = re.compile(r"^DEPLOY-(preview|prod)-(\d{8}-\d{6})$")
GCLOUD_SERVICE_RE = re.compile(r"^[a-z0-9_-]+$")
DEFAULT_PROXY_TIMEOUT_SECONDS = int(os.getenv("WORLDARCH_TIMEOUT_SECONDS", "600") or "600")
MAX_DEPLOY_CONFIRM_TOKEN_AGE_SECONDS = int(
    os.getenv("WORLDTOOLS_DEPLOY_CONFIRM_MAX_AGE_SECONDS", "600") or "600"
)
MAX_DEPLOY_CONFIRM_TOKEN_FUTURE_SKEW_SECONDS = int(
    os.getenv("WORLDTOOLS_DEPLOY_CONFIRM_FUTURE_SKEW_SECONDS", "120") or "120"
)
ALLOWED_FIRESTORE_OPS = {
    "==",
    "!=",
    "<",
    "<=",
    ">",
    ">=",
    "in",
    "not-in",
    "array-contains",
    "array-contains-any",
}

LOCAL_TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "name": "diag_evaluate_campaign_dice",
        "description": "Evaluate campaign dice telemetry and optionally save a report.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "campaign_id": {"type": "string"},
                "include_recent": {"type": "integer", "default": 20, "maximum": 100},
                "save_report": {"type": "boolean", "default": False},
            },
            "required": ["campaign_id"],
        },
    },
    {
        "name": "admin_copy_campaign_user_to_user",
        "description": "Copy campaign + subcollections from source user to destination user.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_user_id": {"type": "string"},
                "source_campaign_id": {"type": "string"},
                "dest_user_id": {"type": "string"},
                "suffix": {"type": "string", "default": "(copy)"},
                "dry_run": {"type": "boolean", "default": True},
                "reason": {"type": "string"},
                "ticket_id": {"type": "string"},
            },
            "required": [
                "source_user_id",
                "source_campaign_id",
                "dest_user_id",
                "reason",
                "ticket_id",
            ],
        },
    },
    {
        "name": "admin_download_campaign",
        "description": "Download campaign artifacts to local Downloads root.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target_user_id": {"type": "string"},
                "campaign_id": {"type": "string"},
                "format": {"type": "string", "enum": ["txt", "docx", "pdf"], "default": "txt"},
                "include_game_state": {"type": "boolean", "default": True},
                "reason": {"type": "string"},
                "ticket_id": {"type": "string"},
            },
            "required": ["target_user_id", "campaign_id", "reason", "ticket_id"],
        },
    },
    {
        "name": "admin_download_campaign_entries",
        "description": "Download selected campaign story entries as JSON/JSONL artifact.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target_user_id": {"type": "string"},
                "campaign_id": {"type": "string"},
                "entry_ids": {"type": "array", "items": {"type": "string"}},
                "from_timestamp": {"type": "string"},
                "to_timestamp": {"type": "string"},
                "limit": {"type": "integer", "default": 500, "maximum": 5000},
                "format": {"type": "string", "enum": ["json", "jsonl"], "default": "jsonl"},
                "reason": {"type": "string"},
                "ticket_id": {"type": "string"},
            },
            "required": ["target_user_id", "campaign_id", "reason", "ticket_id"],
        },
    },
    {
        "name": "ops_gcloud_logs_read",
        "description": "Read Cloud Logging entries through an allowlisted gcloud wrapper.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "project_id": {"type": "string"},
                "lookback_minutes": {"type": "integer", "default": 60, "maximum": 1440},
                "limit": {"type": "integer", "default": 100, "maximum": 500},
                "severity": {"type": ["string", "null"]},
                "contains": {"type": ["string", "null"]},
                "reason": {"type": "string"},
                "ticket_id": {"type": "string"},
            },
            "required": ["service", "project_id", "reason", "ticket_id"],
        },
    },
    {
        "name": "ops_firestore_read_document",
        "description": "Read a Firestore document by allowlisted path prefix.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "document_path": {"type": "string"},
                "field_mask": {"type": "array", "items": {"type": "string"}},
                "reason": {"type": "string"},
                "ticket_id": {"type": "string"},
            },
            "required": ["document_path", "reason", "ticket_id"],
        },
    },
    {
        "name": "ops_firestore_query_collection_group",
        "description": "Query a Firestore collection group with small guardrailed limits.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "collection_group": {"type": "string"},
                "filters": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "field": {"type": "string"},
                            "op": {"type": "string"},
                            "value": {},
                        },
                        "required": ["field", "op", "value"],
                    },
                },
                "order_by": {"type": ["string", "null"]},
                "limit": {"type": "integer", "default": 50, "maximum": 200},
                "reason": {"type": "string"},
                "ticket_id": {"type": "string"},
            },
            "required": ["collection_group", "reason", "ticket_id"],
        },
    },
    {
        "name": "ops_run_mcp_local",
        "description": "Run local MCP server wrapper script (dry-run by default).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mode": {"type": "string", "enum": ["dual", "http-only", "stdio-only"], "default": "dual"},
                "port": {"type": "integer", "default": 8081},
                "dry_run": {"type": "boolean", "default": True},
                "reason": {"type": "string"},
                "ticket_id": {"type": "string"},
            },
            "required": ["reason", "ticket_id"],
        },
    },
    {
        "name": "ops_run_mcp_production",
        "description": "Run production MCP startup wrapper script (dry-run by default).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dry_run": {"type": "boolean", "default": True},
                "reason": {"type": "string"},
                "ticket_id": {"type": "string"},
            },
            "required": ["reason", "ticket_id"],
        },
    },
    {
        "name": "ops_deploy_mcp_service",
        "description": "Guardrailed gcloud run deploy wrapper with confirmation token.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "enum": ["preview", "prod"]},
                "service": {"type": "string"},
                "region": {"type": "string"},
                "image": {"type": "string"},
                "revision_suffix": {"type": ["string", "null"]},
                "confirm": {"type": "string"},
                "reason": {"type": "string"},
                "ticket_id": {"type": "string"},
            },
            "required": [
                "target",
                "service",
                "region",
                "image",
                "confirm",
                "reason",
                "ticket_id",
            ],
        },
    },
]


class ProxyJsonRpcError(Exception):
    """JSON-RPC error wrapper."""

    def __init__(self, code: int, message: str, data: Any = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data


@dataclass
class AuthContext:
    actor_user_id: str | None
    actor_email: str | None
    roles: set[str]


class WorldAIToolsProxy:
    """JSON-RPC proxy runtime for local + passthrough tools."""

    passthrough_identity_tools = {
        "create_campaign",
        "get_campaign_state",
        "process_action",
        "update_campaign",
        "export_campaign",
        "get_campaigns_list",
        "get_user_settings",
        "update_user_settings",
    }

    def __init__(self, upstream_url: str, request_timeout: int = DEFAULT_PROXY_TIMEOUT_SECONDS):
        self.upstream_url = upstream_url
        self.request_timeout = request_timeout
        self.upstream_bearer_token = os.getenv("WORLDTOOLS_BEARER_TOKEN", "").strip()
        self.repo_root = Path(__file__).resolve().parent.parent
        self.production_mode = os.getenv("PRODUCTION_MODE", "").lower() == "true"
        self.allow_unsafe_local_tool_bypass = (
            os.getenv("WORLDTOOLS_UNSAFE_SKIP_AUTH", "").lower() == "true"
        )
        self.support_admin_allowlist = _parse_csv_set(os.getenv("WORLDTOOLS_SUPPORT_ADMINS", ""))
        self.ops_admin_allowlist = _parse_csv_set(os.getenv("WORLDTOOLS_OPS_ADMINS", ""))
        self.deploy_admin_allowlist = _parse_csv_set(os.getenv("WORLDTOOLS_DEPLOY_ADMINS", ""))
        self.gcloud_project_allowlist = _parse_csv_set(
            os.getenv("WORLDTOOLS_GCLOUD_PROJECT_ALLOWLIST", "")
        )
        self.firestore_path_prefixes = _parse_csv_list(
            os.getenv("WORLDTOOLS_FIRESTORE_PATH_PREFIXES", "users/")
        )

    def handle_jsonrpc(self, request_data: dict[str, Any], auth: AuthContext) -> dict[str, Any]:
        request_id = request_data.get("id")
        method = request_data.get("method")
        params = request_data.get("params", {}) or {}

        try:
            if method == "tools/list":
                return _jsonrpc_result(self._tools_list(), request_id)
            if method == "tools/call":
                return self._tools_call(params, request_id, auth)
            if method in ("resources/list", "resources/read"):
                return self._passthrough_jsonrpc(method, params, request_id)
            raise ProxyJsonRpcError(-32601, f"Method not found: {method}")
        except ProxyJsonRpcError as err:
            return _jsonrpc_error(err.code, err.message, request_id, err.data)
        except Exception as err:  # noqa: BLE001
            logging_util.error("Unhandled MCP proxy error: %s", err)
            logging_util.error(traceback.format_exc())
            data = None if self.production_mode else traceback.format_exc()
            return _jsonrpc_error(-32603, str(err), request_id, data)

    def _tools_list(self) -> dict[str, Any]:
        local_tools = [dict(tool) for tool in LOCAL_TOOL_SCHEMAS]

        upstream_tools: list[dict[str, Any]] = []
        upstream_error: dict[str, Any] | None = None
        try:
            upstream_response = self._passthrough_jsonrpc("tools/list", {}, "upstream-tools-list")
            if "error" in upstream_response:
                upstream_error = upstream_response["error"]
            else:
                upstream_tools = upstream_response.get("result", {}).get("tools", []) or []
        except Exception as err:  # noqa: BLE001
            upstream_error = {"message": str(err)}

        for upstream in upstream_tools:
            name = str(upstream.get("name", ""))
            if name.startswith(RESERVED_PREFIXES):
                raise ProxyJsonRpcError(
                    -32010,
                    f"Upstream tool collision with reserved prefix: {name}",
                )

        merged = list(upstream_tools)
        merged.extend(local_tools)
        result: dict[str, Any] = {"tools": merged}
        if upstream_error:
            result["upstream_error"] = upstream_error
        return result

    def _tools_call(
        self,
        params: dict[str, Any],
        request_id: Any,
        auth: AuthContext,
    ) -> dict[str, Any]:
        name = params.get("name")
        arguments = params.get("arguments", {}) or {}

        if not isinstance(name, str) or not name:
            raise ProxyJsonRpcError(-32602, "tools/call requires non-empty params.name")
        if not isinstance(arguments, dict):
            raise ProxyJsonRpcError(-32602, "tools/call params.arguments must be an object")

        if name in _local_tool_names():
            self._validate_common_admin_ops_requirements(name, arguments)
            self._authorize_local_tool(name, auth)
            result = self._run_local_tool(name, arguments, auth)
            mcp_result = {"content": [{"type": "text", "text": json.dumps(result, default=firestore_service.json_default_serializer)}]}
            return _jsonrpc_result(mcp_result, request_id)

        passthrough_args = dict(arguments)
        if auth.actor_user_id and (
            "user_id" in passthrough_args or name in self.passthrough_identity_tools
        ):
            passthrough_args["user_id"] = auth.actor_user_id

        return self._passthrough_jsonrpc(
            "tools/call",
            {"name": name, "arguments": passthrough_args},
            request_id,
        )

    def _authorize_local_tool(self, tool_name: str, auth: AuthContext) -> None:
        if self.allow_unsafe_local_tool_bypass:
            logging_util.warning(
                "WORLDTOOLS_UNSAFE_SKIP_AUTH enabled; bypassing local tool auth for %s",
                tool_name,
            )
            return

        if tool_name.startswith("diag_") or tool_name.startswith("admin_"):
            if "support_admin" not in auth.roles:
                raise ProxyJsonRpcError(-32001, "support_admin role required")
            return

        if tool_name in {
            "ops_gcloud_logs_read",
            "ops_firestore_read_document",
            "ops_firestore_query_collection_group",
            "ops_run_mcp_local",
        }:
            if "ops_admin" not in auth.roles:
                raise ProxyJsonRpcError(-32001, "ops_admin role required")
            return

        if tool_name in {"ops_run_mcp_production", "ops_deploy_mcp_service"}:
            if "deploy_admin" not in auth.roles:
                raise ProxyJsonRpcError(-32001, "deploy_admin role required")
            return

        raise ProxyJsonRpcError(-32001, f"No authorization policy for tool '{tool_name}'")

    def _validate_common_admin_ops_requirements(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> None:
        if not (tool_name.startswith("admin_") or tool_name.startswith("ops_")):
            return
        if not str(arguments.get("reason", "")).strip():
            raise ProxyJsonRpcError(-32602, "reason is required for admin_/ops_ tools")
        if not str(arguments.get("ticket_id", "")).strip():
            raise ProxyJsonRpcError(-32602, "ticket_id is required for admin_/ops_ tools")

    def _run_local_tool(
        self, tool_name: str, arguments: dict[str, Any], auth: AuthContext
    ) -> dict[str, Any]:
        handlers = {
            "diag_evaluate_campaign_dice": self._tool_diag_evaluate_campaign_dice,
            "admin_copy_campaign_user_to_user": self._tool_admin_copy_campaign_user_to_user,
            "admin_download_campaign": self._tool_admin_download_campaign,
            "admin_download_campaign_entries": self._tool_admin_download_campaign_entries,
            "ops_gcloud_logs_read": self._tool_ops_gcloud_logs_read,
            "ops_firestore_read_document": self._tool_ops_firestore_read_document,
            "ops_firestore_query_collection_group": self._tool_ops_firestore_query_collection_group,
            "ops_run_mcp_local": self._tool_ops_run_mcp_local,
            "ops_run_mcp_production": self._tool_ops_run_mcp_production,
            "ops_deploy_mcp_service": self._tool_ops_deploy_mcp_service,
        }
        handler = handlers.get(tool_name)
        if not handler:
            raise ProxyJsonRpcError(-32601, f"Unknown local tool: {tool_name}")
        return handler(arguments, auth)

    def _tool_diag_evaluate_campaign_dice(
        self, arguments: dict[str, Any], auth: AuthContext
    ) -> dict[str, Any]:
        del auth
        campaign_id = str(arguments.get("campaign_id", "")).strip()
        if not campaign_id:
            raise ProxyJsonRpcError(-32602, "campaign_id is required")

        include_recent = int(arguments.get("include_recent", 20) or 20)
        include_recent = max(1, min(include_recent, 100))
        save_report = bool(arguments.get("save_report", False))

        command = [sys.executable, "scripts/audit_dice_rolls.py", campaign_id,
                   "--recent", str(include_recent)]
        process = _run_command(
            command,
            cwd=str(self.repo_root),
            timeout=120,
        )

        by_source_match = re.search(r"By source:\s*(\{.*\})", process.stdout)
        by_source: dict[str, Any] = {}
        if by_source_match:
            by_source_blob = by_source_match.group(1)
            try:
                parsed_by_source = ast.literal_eval(by_source_blob)
            except (ValueError, SyntaxError) as err:
                raise ProxyJsonRpcError(
                    -32020,
                    "Failed to parse dice audit by_source summary",
                    {
                        "stdout_preview": process.stdout[:500],
                        "stderr_preview": process.stderr[:500],
                    },
                ) from err
            if not isinstance(parsed_by_source, dict):
                raise ProxyJsonRpcError(
                    -32020,
                    "Dice audit by_source summary must be a dictionary",
                    {
                        "stdout_preview": process.stdout[:500],
                        "stderr_preview": process.stderr[:500],
                    },
                )
            by_source = parsed_by_source

        summary = {
            "total_rolls": _extract_int(process.stdout, r"Total rolls with results:\s*(\d+)/"),
            "entries_with_dice": _extract_int(process.stdout, r"Entries with dice rolls:\s*(\d+)"),
            "by_source": by_source,
        }
        warnings = _extract_warning_lines(process.stdout)

        report_artifact = None
        if save_report:
            report_dir = self._ensure_artifact_subdir("worldai_dice_audits")
            filename = f"dice_audit_{campaign_id}_{_timestamp_slug()}.json"
            report_path = _safe_join_under_root(report_dir, filename)
            payload = {
                "campaign_id": campaign_id,
                "include_recent": include_recent,
                "command": process.command,
                "exit_code": process.exit_code,
                "stdout": process.stdout,
                "stderr": process.stderr,
            }
            report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            report_artifact = _artifact_metadata(report_path)

        if process.exit_code != 0:
            raise ProxyJsonRpcError(
                -32020,
                "Dice audit command failed",
                {
                    "command": process.command,
                    "exit_code": process.exit_code,
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                    "report_artifact": report_artifact,
                },
            )

        return {
            "campaign_id": campaign_id,
            "summary": summary,
            "warnings": warnings,
            "recent_limit": include_recent,
            "report_artifact": report_artifact,
            "command": process.command,
        }

    def _tool_admin_copy_campaign_user_to_user(
        self, arguments: dict[str, Any], auth: AuthContext
    ) -> dict[str, Any]:
        del auth
        source_user_id = str(arguments.get("source_user_id", "")).strip()
        source_campaign_id = str(arguments.get("source_campaign_id", "")).strip()
        dest_user_id = str(arguments.get("dest_user_id", "")).strip()
        suffix = str(arguments.get("suffix", "(copy)") or "(copy)")
        dry_run_arg = arguments.get("dry_run", True)
        dry_run = bool(True if dry_run_arg is None else dry_run_arg)

        if not source_user_id or not source_campaign_id or not dest_user_id:
            raise ProxyJsonRpcError(
                -32602,
                "source_user_id, source_campaign_id, dest_user_id are required",
            )

        # Early return for dry_run - skip all Firestore reads
        if dry_run:
            return {
                "dry_run": True,
                "new_campaign_id": None,
                "copied_counts": {
                    "campaign": 1,
                    "story": 0,
                    "game_states": 0,
                    "notes": 0,
                    "characters": 0,
                },
                "source": f"users/{source_user_id}/campaigns/{source_campaign_id}",
                "dest_user": dest_user_id,
            }

        db = _get_firestore_db()
        source_ref = (
            db.collection("users")
            .document(source_user_id)
            .collection("campaigns")
            .document(source_campaign_id)
        )
        source_doc = source_ref.get()
        if not source_doc.exists:
            raise ProxyJsonRpcError(
                -32021,
                f"Source campaign not found: users/{source_user_id}/campaigns/{source_campaign_id}",
            )

        subcollections = ["story", "game_states", "notes", "characters"]
        counts = {"campaign": 1, "story": 0, "game_states": 0, "notes": 0, "characters": 0}
        for subcollection in subcollections:
            docs = list(source_ref.collection(subcollection).stream())
            counts[subcollection] = len(docs)

        campaign_data = source_doc.to_dict() or {}
        campaign_title = str(campaign_data.get("title") or "Untitled Campaign")
        campaign_data["title"] = f"{campaign_title} {suffix}".strip()

        dest_campaigns = db.collection("users").document(dest_user_id).collection("campaigns")
        new_campaign_ref = dest_campaigns.document()
        new_campaign_ref.set(campaign_data)

        for subcollection in subcollections:
            for doc in source_ref.collection(subcollection).stream():
                new_campaign_ref.collection(subcollection).document(doc.id).set(doc.to_dict() or {})

        return {
            "dry_run": False,
            "new_campaign_id": new_campaign_ref.id,
            "copied_counts": counts,
            "source": f"users/{source_user_id}/campaigns/{source_campaign_id}",
            "destination": f"users/{dest_user_id}/campaigns/{new_campaign_ref.id}",
        }

    def _tool_admin_download_campaign(
        self, arguments: dict[str, Any], auth: AuthContext
    ) -> dict[str, Any]:
        del auth
        if self.production_mode:
            raise ProxyJsonRpcError(
                -32022,
                "admin_download_campaign is disabled in production mode",
            )

        target_user_id = str(arguments.get("target_user_id", "")).strip()
        campaign_id = str(arguments.get("campaign_id", "")).strip()
        export_format = str(arguments.get("format", "txt") or "txt").lower()
        include_game_state = bool(arguments.get("include_game_state", True))

        if export_format not in {"txt", "docx", "pdf"}:
            raise ProxyJsonRpcError(-32602, "format must be one of txt|docx|pdf")
        if not target_user_id or not campaign_id:
            raise ProxyJsonRpcError(-32602, "target_user_id and campaign_id are required")

        campaign_data, story_context = firestore_service.get_campaign_by_id(target_user_id, campaign_id)
        if not campaign_data:
            raise ProxyJsonRpcError(-32023, "campaign not found")
        if not isinstance(story_context, list):
            raise ProxyJsonRpcError(-32024, "campaign story data unavailable")

        out_dir = self._ensure_artifact_subdir(
            f"worldai_campaign_exports/{_timestamp_slug()}_{campaign_id[:8]}"
        )

        campaign_title = str(campaign_data.get("title") or "Untitled Campaign")
        safe_title = "".join(c if c.isalnum() or c in "-_ " else "_" for c in campaign_title).strip()[:60]
        base = f"{safe_title or 'campaign'}_{campaign_id[:8]}"

        story_text = document_generator.get_story_text_from_context_enhanced(
            story_context,
            include_scenes=True,
        )

        story_path = _safe_join_under_root(out_dir, f"{base}.{export_format}")
        if export_format == "txt":
            document_generator.generate_txt(story_text, str(story_path), campaign_title)
        elif export_format == "docx":
            document_generator.generate_docx(story_text, str(story_path), campaign_title)
        else:
            document_generator.generate_pdf(story_text, str(story_path), campaign_title)

        artifacts = [
            {
                "kind": "story",
                **_artifact_metadata(story_path),
                "mime_type": _guess_mime_type(export_format),
            }
        ]

        if include_game_state:
            game_state = firestore_service.get_campaign_game_state(target_user_id, campaign_id)
            game_state_payload = game_state.to_dict() if game_state is not None else {}
            game_state_path = _safe_join_under_root(out_dir, f"{base}_game_state.json")
            game_state_path.write_text(
                json.dumps(
                    game_state_payload,
                    indent=2,
                    default=firestore_service.json_default_serializer,
                ),
                encoding="utf-8",
            )
            artifacts.append(
                {
                    "kind": "game_state",
                    **_artifact_metadata(game_state_path),
                    "mime_type": "application/json",
                }
            )

        return {
            "campaign_id": campaign_id,
            "artifacts": artifacts,
            "entry_count": len(story_context),
        }

    def _tool_admin_download_campaign_entries(
        self, arguments: dict[str, Any], auth: AuthContext
    ) -> dict[str, Any]:
        del auth
        if self.production_mode:
            raise ProxyJsonRpcError(
                -32025,
                "admin_download_campaign_entries is disabled in production mode",
            )

        target_user_id = str(arguments.get("target_user_id", "")).strip()
        campaign_id = str(arguments.get("campaign_id", "")).strip()
        entry_ids = arguments.get("entry_ids") or []
        from_ts = arguments.get("from_timestamp")
        to_ts = arguments.get("to_timestamp")
        entry_format = str(arguments.get("format", "jsonl") or "jsonl").lower()
        limit = int(arguments.get("limit", 500) or 500)
        limit = max(1, min(limit, 5000))

        if entry_format not in {"json", "jsonl"}:
            raise ProxyJsonRpcError(-32602, "format must be json or jsonl")
        if not target_user_id or not campaign_id:
            raise ProxyJsonRpcError(-32602, "target_user_id and campaign_id are required")
        if entry_ids and (from_ts or to_ts):
            raise ProxyJsonRpcError(-32602, "entry_ids cannot be combined with time-window fields")
        if (from_ts and not to_ts) or (to_ts and not from_ts):
            raise ProxyJsonRpcError(-32602, "from_timestamp and to_timestamp must be provided together")

        db = _get_firestore_db()
        story_ref = (
            db.collection("users")
            .document(target_user_id)
            .collection("campaigns")
            .document(campaign_id)
            .collection("story")
        )

        entries: list[dict[str, Any]] = []

        if entry_ids:
            for entry_id in entry_ids[:limit]:
                doc = story_ref.document(str(entry_id)).get()
                if doc.exists:
                    payload = doc.to_dict() or {}
                    payload["id"] = doc.id
                    entries.append(payload)
        elif from_ts and to_ts:
            try:
                from_dt = _parse_timestamp(str(from_ts))
                to_dt = _parse_timestamp(str(to_ts))
            except ValueError as err:
                raise ProxyJsonRpcError(
                    -32602, "from_timestamp/to_timestamp must be ISO-8601"
                ) from err
            for doc in story_ref.stream():
                payload = doc.to_dict() or {}
                ts_value = payload.get("timestamp")
                normalized = _normalize_datetime(ts_value)
                if normalized and from_dt <= normalized <= to_dt:
                    payload["id"] = doc.id
                    entries.append(payload)
            entries.sort(
                key=lambda entry: _normalize_datetime(entry.get("timestamp"))
                or datetime.min.replace(tzinfo=UTC)
            )
            entries = entries[:limit]
        else:
            for doc in story_ref.limit(limit).stream():
                payload = doc.to_dict() or {}
                payload["id"] = doc.id
                entries.append(payload)

        out_dir = self._ensure_artifact_subdir("worldai_campaign_entries")
        filename = f"entries_{campaign_id[:8]}_{_timestamp_slug()}.{entry_format}"
        output_path = _safe_join_under_root(out_dir, filename)

        if entry_format == "json":
            output_path.write_text(
                json.dumps(entries, indent=2, default=firestore_service.json_default_serializer),
                encoding="utf-8",
            )
        else:
            lines = [
                json.dumps(entry, default=firestore_service.json_default_serializer)
                for entry in entries
            ]
            output_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

        return {
            "campaign_id": campaign_id,
            "entries_written": len(entries),
            "artifact": {
                **_artifact_metadata(output_path),
                "format": entry_format,
            },
        }

    def _tool_ops_gcloud_logs_read(
        self, arguments: dict[str, Any], auth: AuthContext
    ) -> dict[str, Any]:
        del auth
        service = str(arguments.get("service", "")).strip()
        project_id = str(arguments.get("project_id", "")).strip()
        lookback_minutes = int(arguments.get("lookback_minutes", 60) or 60)
        limit = int(arguments.get("limit", 100) or 100)
        severity = arguments.get("severity")
        contains = arguments.get("contains")

        if not service or not project_id:
            raise ProxyJsonRpcError(-32602, "service and project_id are required")
        # Sanitize service name: only allow alphanumeric, hyphens, underscores
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,128}", service):
            raise ProxyJsonRpcError(-32602, "service name contains invalid characters")
        # Sanitize severity: must be a known Cloud Logging severity level
        _VALID_SEVERITIES = {"DEFAULT", "DEBUG", "INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"}
        if severity and str(severity).upper() not in _VALID_SEVERITIES:
            raise ProxyJsonRpcError(-32602, f"severity must be one of {sorted(_VALID_SEVERITIES)}")
        if severity:
            severity = str(severity).upper()
        lookback_minutes = max(1, min(lookback_minutes, 1440))
        limit = max(1, min(limit, 500))

        if self.production_mode and not self.gcloud_project_allowlist:
            raise ProxyJsonRpcError(
                -32026,
                "WORLDTOOLS_GCLOUD_PROJECT_ALLOWLIST is required in production mode",
            )
        project_id_lower = project_id.lower()
        if self.gcloud_project_allowlist and project_id_lower not in self.gcloud_project_allowlist:
            raise ProxyJsonRpcError(
                -32027,
                f"project_id '{project_id}' is not allowlisted",
            )

        if not GCLOUD_SERVICE_RE.match(service):
            raise ProxyJsonRpcError(-32602, "service must match ^[a-z0-9_-]+$")

        query_parts = [
            "resource.type=cloud_run_revision",
            f"resource.labels.service_name={service}",
        ]
        if severity:
            safe_severity = _sanitize_logs_severity(str(severity))
            query_parts.append(f"severity>={safe_severity}")
        if contains:
            safe_contains = _sanitize_logs_contains(str(contains))
            query_parts.append(f'textPayload:"{safe_contains}"')
        query = " AND ".join(query_parts)

        command = [
            "gcloud",
            "logging",
            "read",
            query,
            "--project",
            project_id,
            "--freshness",
            f"{lookback_minutes}m",
            "--limit",
            str(limit),
            "--format",
            "json",
        ]

        process = _run_command(command, cwd=str(self.repo_root), timeout=60)
        if process.exit_code != 0:
            raise ProxyJsonRpcError(
                -32028,
                "gcloud logging read failed",
                {
                    "command": process.command,
                    "exit_code": process.exit_code,
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                },
            )

        entries = []
        if process.stdout.strip():
            try:
                parsed = json.loads(process.stdout)
                if isinstance(parsed, list):
                    entries = [_redact_value(item) for item in parsed]
                else:
                    raise ProxyJsonRpcError(
                        -32029,
                        "gcloud logging output was not a JSON array",
                        {"stdout_preview": process.stdout[:500], "stderr_preview": process.stderr[:500]},
                    )
            except json.JSONDecodeError as err:
                raise ProxyJsonRpcError(
                    -32029,
                    f"Failed to parse gcloud logging JSON output: {err}",
                    {"stdout_preview": process.stdout[:500], "stderr_preview": process.stderr[:500]},
                ) from err

        return {
            "command": process.command,
            "entry_count": len(entries),
            "entries": entries,
        }

    def _tool_ops_firestore_read_document(
        self, arguments: dict[str, Any], auth: AuthContext
    ) -> dict[str, Any]:
        del auth
        document_path = str(arguments.get("document_path", "")).strip().strip("/")
        field_mask = arguments.get("field_mask") or []

        if not document_path:
            raise ProxyJsonRpcError(-32602, "document_path is required")
        if not any(_path_matches_prefix(document_path, prefix) for prefix in self.firestore_path_prefixes):
            raise ProxyJsonRpcError(
                -32029,
                f"document_path '{document_path}' is outside allowlisted prefixes",
            )

        db = _get_firestore_db()
        doc = db.document(document_path).get()
        data = doc.to_dict() if doc.exists else None

        if isinstance(data, dict) and field_mask:
            data = {field: data.get(field) for field in field_mask}

        return {
            "document_path": document_path,
            "exists": bool(doc.exists),
            "data": _redact_value(data),
        }

    def _tool_ops_firestore_query_collection_group(
        self, arguments: dict[str, Any], auth: AuthContext
    ) -> dict[str, Any]:
        del auth
        collection_group = str(arguments.get("collection_group", "")).strip()
        filters = arguments.get("filters") or []
        order_by = arguments.get("order_by")
        limit = int(arguments.get("limit", 50) or 50)
        limit = max(1, min(limit, 200))

        if not collection_group:
            raise ProxyJsonRpcError(-32602, "collection_group is required")

        db = _get_firestore_db()
        query = db.collection_group(collection_group)

        for item in filters:
            if not isinstance(item, dict):
                continue
            field = str(item.get("field", "")).strip()
            op = str(item.get("op", "")).strip()
            value = item.get("value")
            if not field or not op:
                continue
            if op not in ALLOWED_FIRESTORE_OPS:
                raise ProxyJsonRpcError(-32602, f"Unsupported Firestore filter op: {op}")
            query = query.where(field, op, value)

        if order_by:
            query = query.order_by(str(order_by))

        docs = []
        for doc in query.limit(limit).stream():
            docs.append(
                {
                    "path": doc.reference.path,
                    "id": doc.id,
                    "data": _redact_value(doc.to_dict() or {}),
                }
            )

        return {
            "collection_group": collection_group,
            "count": len(docs),
            "documents": docs,
        }

    def _tool_ops_run_mcp_local(
        self, arguments: dict[str, Any], auth: AuthContext
    ) -> dict[str, Any]:
        del auth
        mode = str(arguments.get("mode", "dual") or "dual")
        port = int(arguments.get("port", 8081) or 8081)
        dry_run_arg = arguments.get("dry_run", True)
        dry_run = bool(True if dry_run_arg is None else dry_run_arg)

        flag_by_mode = {
            "dual": "--dual",
            "http-only": "--http-only",
            "stdio-only": "--stdio-only",
        }
        if mode not in flag_by_mode:
            raise ProxyJsonRpcError(-32602, "mode must be dual|http-only|stdio-only")

        command = [
            "bash",
            "scripts/start_mcp_server.sh",
            flag_by_mode[mode],
            "--port",
            str(port),
        ]

        if dry_run:
            return {"dry_run": True, "command": command}

        log_path = _create_secure_ops_log_file("run_local")
        log_path_str = str(log_path)
        with log_path.open("wb") as log_file:
            proc = subprocess.Popen(
                command,
                cwd=self.repo_root,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )

        return {
            "dry_run": False,
            "command": command,
            "pid": proc.pid,
            "log_path": log_path_str,
        }

    def _tool_ops_run_mcp_production(
        self, arguments: dict[str, Any], auth: AuthContext
    ) -> dict[str, Any]:
        del auth
        dry_run_arg = arguments.get("dry_run", True)
        dry_run = bool(True if dry_run_arg is None else dry_run_arg)
        command = ["bash", "scripts/start_mcp_production.sh"]

        if dry_run:
            return {"dry_run": True, "command": command}

        log_path = _create_secure_ops_log_file("run_prod")
        log_path_str = str(log_path)
        with log_path.open("wb") as log_file:
            proc = subprocess.Popen(
                command,
                cwd=self.repo_root,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )

        return {
            "dry_run": False,
            "command": command,
            "pid": proc.pid,
            "log_path": log_path_str,
        }

    def _tool_ops_deploy_mcp_service(
        self, arguments: dict[str, Any], auth: AuthContext
    ) -> dict[str, Any]:
        del auth
        target = str(arguments.get("target", "")).strip()
        service = str(arguments.get("service", "")).strip()
        region = str(arguments.get("region", "")).strip()
        image = str(arguments.get("image", "")).strip()
        revision_suffix = arguments.get("revision_suffix")
        confirm = str(arguments.get("confirm", "")).strip()

        if target not in {"preview", "prod"}:
            raise ProxyJsonRpcError(-32602, "target must be preview|prod")
        if not service or not region or not image:
            raise ProxyJsonRpcError(-32602, "service, region, image are required")

        _validate_deploy_confirm_token(
            confirm,
            target,
            allow_unsafe_bypass=self.allow_unsafe_local_tool_bypass,
        )

        command = [
            "gcloud",
            "run",
            "deploy",
            service,
            "--region",
            region,
            "--image",
            image,
            "--quiet",
        ]
        if revision_suffix:
            command.extend(["--revision-suffix", str(revision_suffix)])

        if os.getenv("WORLDTOOLS_ENABLE_DEPLOY_EXECUTION", "").lower() != "true":
            return {
                "executed": False,
                "execution_mode": "plan_only",
                "confirm": confirm,
                "command": command,
                "note": "Set WORLDTOOLS_ENABLE_DEPLOY_EXECUTION=true to execute deployment",
            }

        process = _run_command(command, cwd=str(self.repo_root), timeout=600)
        if process.exit_code != 0:
            raise ProxyJsonRpcError(
                -32030,
                "deploy command failed",
                {
                    "command": process.command,
                    "exit_code": process.exit_code,
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                },
            )

        return {
            "executed": True,
            "confirm": confirm,
            "command": process.command,
            "exit_code": process.exit_code,
            "stdout": process.stdout,
            "stderr": process.stderr,
        }

    def _ensure_artifact_subdir(self, relative_dir: str) -> Path:
        root = _downloads_root()
        destination = _safe_join_under_root(root, relative_dir)
        destination.mkdir(parents=True, exist_ok=True)
        return destination

    def _passthrough_jsonrpc(self, method: str, params: dict[str, Any], request_id: Any) -> dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params,
        }
        upstream_headers = {}
        if self.upstream_bearer_token:
            upstream_headers["Authorization"] = f"Bearer {self.upstream_bearer_token}"
        try:
            response = requests.post(
                self.upstream_url,
                json=payload,
                headers=upstream_headers or None,
                timeout=self.request_timeout,
            )
        except requests.RequestException as err:
            raise ProxyJsonRpcError(-32031, "Upstream request failed", {"detail": str(err)}) from err

        if response.status_code != 200:
            raise ProxyJsonRpcError(
                -32032,
                f"Upstream HTTP error: {response.status_code}",
                {"body": response.text[:8000]},
            )

        try:
            upstream_data = response.json()
        except json.JSONDecodeError as err:
            raise ProxyJsonRpcError(
                -32033,
                "Upstream returned non-JSON response",
                {"body_preview": response.text[:500]},
            ) from err

        if not isinstance(upstream_data, dict):
            raise ProxyJsonRpcError(-32034, "Upstream JSON-RPC response must be an object")

        return upstream_data


def _jsonrpc_result(result: Any, request_id: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "result": result, "id": request_id}


def _jsonrpc_error(code: int, message: str, request_id: Any, data: Any = None) -> dict[str, Any]:
    error = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "error": error, "id": request_id}


_LOCAL_TOOL_NAMES: frozenset[str] = frozenset(tool["name"] for tool in LOCAL_TOOL_SCHEMAS)


def _local_tool_names() -> frozenset[str]:
    return _LOCAL_TOOL_NAMES


def _parse_csv_set(value: str) -> set[str]:
    return {item.strip().lower() for item in value.split(",") if item.strip()}


def _parse_csv_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _downloads_root() -> Path:
    configured = os.getenv("WORLDTOOLS_DOWNLOADS_ROOT", "").strip()
    if configured:
        root = Path(configured).expanduser().resolve()
    else:
        root = (Path.home() / "Downloads").resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


def _safe_join_under_root(root: Path, relative_path: str) -> Path:
    candidate = (root / relative_path).resolve()
    root_resolved = root.resolve()
    if candidate != root_resolved and root_resolved not in candidate.parents:
        raise ProxyJsonRpcError(-32040, "Artifact path escapes Downloads root")
    return candidate


def _artifact_metadata(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    return {"path": str(path), "bytes": len(data), "sha256": sha}


def _guess_mime_type(export_format: str) -> str:
    if export_format == "txt":
        return "text/plain"
    if export_format == "docx":
        return (
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        )
    return "application/pdf"


def _extract_warning_lines(stdout: str) -> list[str]:
    warnings: list[str] = []
    for line in stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("-"):
            warnings.append(stripped[1:].strip())
    return warnings


def _extract_int(text: str, pattern: str) -> int:
    match = re.search(pattern, text)
    if not match:
        return 0
    return int(match.group(1))


def _parse_timestamp(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed


def _normalize_datetime(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value
    if isinstance(value, str):
        try:
            parsed = _parse_timestamp(value)
            if parsed.tzinfo is None:
                return parsed.replace(tzinfo=UTC)
            return parsed
        except ValueError:
            return None
    return None


def _redact_value(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, inner in value.items():
            if SENSITIVE_FIELD_PATTERN.search(str(key)):
                redacted[key] = "[REDACTED]"
            else:
                redacted[key] = _redact_value(inner)
        return redacted
    if isinstance(value, list):
        return [_redact_value(item) for item in value]
    return value


@dataclass
class CommandResult:
    command: list[str]
    exit_code: int
    stdout: str
    stderr: str


def _run_command(command: list[str], cwd: str, timeout: int) -> CommandResult:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return CommandResult(
            command=command,
            exit_code=completed.returncode,
            stdout=completed.stdout[-20000:],
            stderr=completed.stderr[-20000:],
        )
    except FileNotFoundError as err:
        raise ProxyJsonRpcError(-32041, f"Command not found: {command[0]}") from err
    except subprocess.TimeoutExpired as err:
        raise ProxyJsonRpcError(-32042, "Command timed out", {"command": command}) from err


def _get_firestore_db():
    try:
        return firestore_service.get_db()
    except Exception as err:  # noqa: BLE001
        raise ProxyJsonRpcError(-32043, "Failed to initialize Firestore", str(err)) from err


def _timestamp_slug() -> str:
    return datetime.now(tz=UTC).strftime("%Y%m%d-%H%M%S")


def _validate_deploy_confirm_token(
    confirm: str, target: str, allow_unsafe_bypass: bool = False
) -> None:
    if allow_unsafe_bypass and confirm == "CONFIRMED":
        return

    match = DEPLOY_CONFIRM_RE.match(confirm)
    if not match:
        raise ProxyJsonRpcError(
            -32602,
            "confirm must be DEPLOY-{target}-{YYYYMMDD-HHMMSS}",
        )

    token_target = match.group(1)
    if token_target != target:
        raise ProxyJsonRpcError(
            -32602,
            f"confirm token target '{token_target}' does not match target '{target}'",
        )

    timestamp_blob = match.group(2)
    try:
        parsed = datetime.strptime(timestamp_blob, "%Y%m%d-%H%M%S").replace(tzinfo=UTC)
    except ValueError as err:
        raise ProxyJsonRpcError(
            -32602,
            "confirm token timestamp must be YYYYMMDD-HHMMSS",
        ) from err

    now = datetime.now(tz=UTC)
    age_seconds = (now - parsed).total_seconds()
    if age_seconds > MAX_DEPLOY_CONFIRM_TOKEN_AGE_SECONDS:
        raise ProxyJsonRpcError(-32602, "confirm token is stale")
    if age_seconds < -MAX_DEPLOY_CONFIRM_TOKEN_FUTURE_SKEW_SECONDS:
        raise ProxyJsonRpcError(-32602, "confirm token timestamp is too far in the future")


def _create_secure_ops_log_file(prefix: str) -> Path:
    log_dir = Path("/tmp/worldai_tools_proxy_ops")
    log_dir.mkdir(parents=True, exist_ok=True)
    fd, log_path = tempfile.mkstemp(prefix=f"{prefix}_", suffix=".log", dir=log_dir)
    os.close(fd)
    return Path(log_path)


def _path_matches_prefix(document_path: str, prefix: str) -> bool:
    normalized_path = document_path.strip().strip("/")
    normalized_prefix = prefix.strip().strip("/")
    if not normalized_prefix:
        return False
    return normalized_path == normalized_prefix or normalized_path.startswith(
        f"{normalized_prefix}/"
    )


def _sanitize_logs_severity(value: str) -> str:
    allowed_severities = {
        "DEFAULT",
        "DEBUG",
        "INFO",
        "NOTICE",
        "WARNING",
        "ERROR",
        "CRITICAL",
        "ALERT",
        "EMERGENCY",
    }
    normalized = value.strip().upper()
    if normalized not in allowed_severities:
        raise ProxyJsonRpcError(-32602, f"Invalid severity: {value}. Must be one of {sorted(allowed_severities)}")
    return normalized


def _sanitize_logs_contains(value: str) -> str:
    sanitized = value.replace("\\", " ").replace('"', " ")
    sanitized = re.sub(r"\b(AND|OR|NOT)\b", " ", sanitized, flags=re.I)
    sanitized = re.sub(r"[()<>:=]", " ", sanitized)
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized[:200]


def _build_auth_context(headers: Any, proxy: WorldAIToolsProxy) -> AuthContext:
    actor_user_id = headers.get("X-Worldtools-User-Id") if headers else None
    # actor_email is AUDIT-ONLY: it is an unverified claim from the caller and is
    # recorded in evidence artifacts for tracing purposes. Role grants below are
    # cross-checked against server-side env-var allowlists; production deployments
    # MUST enforce identity verification via a trusted reverse proxy or mTLS before
    # this handler so that the email claim can be treated as authoritative.
    actor_email = (headers.get("X-Worldtools-Actor-Email") if headers else None) or ""
    actor_email = actor_email.strip().lower() or None

    roles: set[str] = set()

    support = proxy.support_admin_allowlist
    ops = proxy.ops_admin_allowlist
    deploy = proxy.deploy_admin_allowlist

    trust_actor_headers = os.getenv("WORLDTOOLS_TRUST_ACTOR_EMAIL_HEADERS", "").lower() in {
        "1",
        "true",
        "yes",
    }
    if actor_email and trust_actor_headers:
        if actor_email in support:
            roles.add("support_admin")
        if actor_email in ops:
            roles.add("ops_admin")
        if actor_email in deploy:
            roles.add("deploy_admin")

    return AuthContext(actor_user_id=actor_user_id, actor_email=actor_email, roles=roles)


def _build_auth_context_for_stdio(proxy: WorldAIToolsProxy) -> AuthContext:
    """Build AuthContext for stdio adapter from env vars; populates roles from allowlists.

    Uses WORLDTOOLS_ACTOR_EMAIL and WORLDTOOLS_ACTOR_USER_ID. When
    WORLDTOOLS_TRUST_ACTOR_EMAIL_HEADERS is set, actor_email is matched against
    WORLDTOOLS_SUPPORT_ADMINS, WORLDTOOLS_OPS_ADMINS, WORLDTOOLS_DEPLOY_ADMINS.
    """
    actor_user_id = os.getenv("WORLDTOOLS_ACTOR_USER_ID") or None
    actor_email = (os.getenv("WORLDTOOLS_ACTOR_EMAIL") or "").strip().lower() or None

    roles: set[str] = set()
    trust = os.getenv("WORLDTOOLS_TRUST_ACTOR_EMAIL_HEADERS", "").lower() in {
        "1",
        "true",
        "yes",
    }
    if actor_email and trust:
        if actor_email in proxy.support_admin_allowlist:
            roles.add("support_admin")
        if actor_email in proxy.ops_admin_allowlist:
            roles.add("ops_admin")
        if actor_email in proxy.deploy_admin_allowlist:
            roles.add("deploy_admin")

    return AuthContext(actor_user_id=actor_user_id, actor_email=actor_email, roles=roles)


def create_proxy_handler(proxy: WorldAIToolsProxy):
    class ProxyHandler(BaseHTTPRequestHandler):
        def _write_json_response(self, status_code: int, payload: dict[str, Any]) -> None:
            encoded = json.dumps(payload).encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def do_GET(self):  # noqa: N802
            if self.path != "/health":
                self.send_response(404)
                self.end_headers()
                return

            payload = {
                "status": "healthy",
                "service": "worldai-tools-mcp-proxy",
                "upstream_url": proxy.upstream_url,
                "production_mode": proxy.production_mode,
            }
            encoded = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def do_POST(self):  # noqa: N802
            if self.path != "/mcp":
                self.send_response(404)
                self.end_headers()
                return

            request_data: dict[str, Any] | None = None
            try:
                content_length_header = self.headers.get("Content-Length")
                if content_length_header is None:
                    self._write_json_response(
                        400,
                        _jsonrpc_error(-32600, "Missing Content-Length header", None),
                    )
                    return
                try:
                    content_length = int(content_length_header)
                except ValueError:
                    self._write_json_response(
                        400,
                        _jsonrpc_error(-32600, "Invalid Content-Length header", None),
                    )
                    return
                if content_length < 0:
                    self._write_json_response(
                        400,
                        _jsonrpc_error(-32600, "Content-Length cannot be negative", None),
                    )
                    return
                if content_length > MAX_REQUEST_SIZE:
                    self._write_json_response(
                        413,
                        _jsonrpc_error(
                            -32600,
                            f"Content-Length exceeds max size {MAX_REQUEST_SIZE}",
                            None,
                        ),
                    )
                    return
                body = self.rfile.read(content_length)
                request_data = json.loads(body.decode("utf-8"))
                auth = _build_auth_context(self.headers, proxy)
                response_data = proxy.handle_jsonrpc(request_data, auth)
                encoded = json.dumps(
                    response_data,
                    default=firestore_service.json_default_serializer,
                ).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)
            except json.JSONDecodeError:
                self._write_json_response(400, _jsonrpc_error(-32700, "Parse error", None))
            except Exception as err:  # noqa: BLE001
                logging_util.error("Proxy HTTP handler error: %s", err)
                error_data = None if proxy.production_mode else traceback.format_exc()
                response_data = _jsonrpc_error(
                    -32603,
                    str(err),
                    request_data.get("id") if isinstance(request_data, dict) else None,
                    error_data,
                )
                self._write_json_response(500, response_data)

        def log_message(self, format: str, *args: Any) -> None:
            del format, args

    return ProxyHandler


def run_server() -> None:
    parser = argparse.ArgumentParser(description="WorldAI Tools MCP Proxy")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    parser.add_argument("--port", type=int, default=8091, help="Port to bind")
    parser.add_argument(
        "--upstream-url",
        default=os.getenv("WORLDTOOLS_UPSTREAM_MCP_URL", "http://127.0.0.1:8081/mcp"),
        help="Upstream MCP /mcp endpoint URL",
    )
    parser.add_argument(
        "--request-timeout",
        type=int,
        default=int(
            os.getenv("WORLDTOOLS_PROXY_TIMEOUT_SECONDS", str(DEFAULT_PROXY_TIMEOUT_SECONDS))
        ),
        help="Upstream request timeout in seconds",
    )
    args = parser.parse_args()

    logging_util.setup_unified_logging("worldai-tools-mcp-proxy")
    logging_util.info(
        "Starting WorldAI tools MCP proxy on %s:%s -> %s",
        args.host,
        args.port,
        args.upstream_url,
    )

    proxy = WorldAIToolsProxy(args.upstream_url, request_timeout=args.request_timeout)
    handler = create_proxy_handler(proxy)
    httpd = ThreadingHTTPServer((args.host, args.port), handler)
    logging_util.info("WorldAI tools MCP proxy ready at http://%s:%s/mcp", args.host, args.port)
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()

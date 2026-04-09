"""WorldAI MCP STDIO Adapter.

This module provides a stdio-based MCP server that reads JSON-RPC requests
from stdin and writes responses to stdout. It wraps WorldAIToolsProxy for
handling the actual MCP logic.
"""

from __future__ import annotations

import json
import os
import sys
import traceback

from mvp_site import firestore_service
from mvp_site.worldai_tools_mcp_proxy import (
    WorldAIToolsProxy,
    _build_auth_context_for_stdio,
)

def main() -> None:
    """Run the stdio MCP adapter."""
    _dev_mode = os.getenv("WORLDAI_DEV_MODE", "").lower() == "true"
    os.environ["PRODUCTION_MODE"] = "false" if _dev_mode else "true"
    if os.getenv("TESTING_AUTH_BYPASS", "").lower() == "true":
        os.environ["WORLDTOOLS_UNSAFE_SKIP_AUTH"] = "true"

    upstream_url = os.getenv("WORLDTOOLS_UPSTREAM_MCP_URL", "http://127.0.0.1:8081/mcp")

    # Create proxy first (reads allowlists and WORLDTOOLS_UNSAFE_SKIP_AUTH)
    proxy = WorldAIToolsProxy(upstream_url=upstream_url)
    # Build auth with roles populated from allowlists when WORLDTOOLS_TRUST_ACTOR_EMAIL_HEADERS
    auth = _build_auth_context_for_stdio(proxy)

    # Read JSON-RPC requests from stdin using readline() to avoid buffering issues
    sys.stdin.reconfigure(line_buffering=True)
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        request_data = None
        try:
            request_data = json.loads(line)

            # Handle non-dict JSON payloads (e.g., arrays, primitives) - return Invalid Request
            if not isinstance(request_data, dict):
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request: JSON payload must be an object",
                    },
                    "id": None,
                }
                print(json.dumps(error_response, default=firestore_service.json_default_serializer), flush=True)
                continue

            request_id = request_data.get("id")
            method = request_data.get("method")

            # Handle MCP initialize handshake - required before any tool calls
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {},
                            "resources": {},
                        },
                        "serverInfo": {
                            "name": "worldai-mcp-stdio",
                            "version": "1.0.0",
                        },
                    },
                }
                print(json.dumps(response, default=firestore_service.json_default_serializer), flush=True)
            # Skip responses to notifications (absent id) per JSON-RPC 2.0; id:null is a Request
            elif "id" not in request_data:
                # This is a notification - process but don't write response
                proxy.handle_jsonrpc(request_data, auth)
            else:
                response = proxy.handle_jsonrpc(request_data, auth)
                # Write response to stdout with flush
                print(json.dumps(response, default=firestore_service.json_default_serializer), flush=True)
        except json.JSONDecodeError as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {e}",
                },
                "id": None,
            }
            print(json.dumps(error_response, default=firestore_service.json_default_serializer), flush=True)
        except Exception as e:
            _dev = os.getenv("WORLDAI_DEV_MODE", "").lower() == "true"
            error_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": "Internal error" if not _dev else str(e),
                    "data": traceback.format_exc() if _dev else None,
                },
                "id": request_data.get("id") if isinstance(request_data, dict) else None,
            }
            print(json.dumps(error_response, default=firestore_service.json_default_serializer), flush=True)


if __name__ == "__main__":
    main()

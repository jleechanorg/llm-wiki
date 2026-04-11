---
title: "WorldAI Tools MCP Proxy Tests"
type: source
tags: [testing, mcp, proxy, json-rpc, security, python]
source_file: "raw/worldai-tools-mcp-proxy-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating the WorldAI Tools MCP proxy runtime, including tool catalog validation, admin tool authorization, deploy confirm token parsing, input sanitization for gcloud_logs, and campaign dice evaluation wiring.

## Key Claims
- **Tool Catalog**: LOCAL_TOOL_SCHEMAS includes 10 WorldAI MCP tools (diag_evaluate_campaign_dice, admin_copy_campaign_user_to_user, admin_download_campaign, ops_gcloud_logs_read, etc.)
- **Admin Authorization**: Admin tools require both reason and ticket_id parameters; missing either returns -32602 error
- **Deploy Tokens**: Valid format is `DEPLOY-{target}-{timestamp}` where target must match (prod/preview) and timestamp is YYYYmmdd-HHMMSS
- **Input Sanitization**: ops_gcloud_logs_read rejects service names with injection characters (AND, OR, >=) and severity values not in known set
- **Dice Evaluation**: diag_evaluate_campaign_dice wires include_recent parameter and parses entries from script output

## Key Test Cases
- test_local_tools_catalog_contains_expected_names: Validates all 10 MCP tools present in catalog
- test_admin_tools_require_reason_and_ticket: Returns -32602 error when reason/ticket missing
- test_deploy_confirm_token_accepts_exact_format: Accepts DEPLOY-prod/timestamp format
- test_deploy_confirm_token_rejects_wrong_target: Rejects preview token for prod target
- test_deploy_confirm_token_rejects_invalid_shape: Rejects malformed tokens
- test_gcloud_logs_rejects_invalid_service_name: Blocks injection in service param
- test_gcloud_logs_rejects_invalid_severity: Blocks invalid severity values
- test_diag_evaluate_campaign_dice_wires_include_recent_and_parses_entries: Validates wiring

## Connections
- [[WorldAIToolsProxy]] — main class under test
- [[MCP Proxy]] — architectural pattern being tested
- [[Input Validation]] — security validation being tested

## Contradictions
- None identified

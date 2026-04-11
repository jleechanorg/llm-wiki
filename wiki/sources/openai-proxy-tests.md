---
title: "OpenAI Proxy Tests"
type: source
tags: [python, testing, openai, api, proxy, flask]
source_file: "raw/test_openai_proxy_provider.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for the OpenAI-compatible inference proxy. Tests cover payload validation, gateway forwarding (both streaming and non-streaming), Flask route authentication, and various error handling scenarios including 4xx/5xx responses from the gateway.

## Key Claims
- **Payload validation**: parse_chat_completions_payload validates model, messages, stream, temperature, max_tokens, tools, and response_format fields
- **Non-streaming forwarding**: invoke_openclaw_gateway forwards non-streaming requests to the configured gateway URL
- **Streaming forwarding**: invoke_openclaw_gateway_stream handles streaming responses from the gateway
- **Flask route auth**: Tests validate authentication with valid, invalid, and revoked worldai_ API keys
- **Error handling**: Tests cover gateway unreachable (502), invalid JSON body (400), and missing gateway_url in settings (400)
- **Temperature bounds**: Validates temperature is between 0 and 2
- **Max tokens capping**: max_tokens capped at MAX_PROXY_MAX_TOKENS

## Key Test Cases
- test_minimal_valid_payload, test_stream_flag, test_temperature_and_max_tokens
- test_messages_items_must_be_objects_with_role
- test_temperature_rejected_above_2, test_temperature_rejected_below_0
- test_missing_model_rejected, test_empty_messages_rejected
- test_tools_passed_through, test_response_format_passed_through
- test_tool_choice_auto

## Connections
- [[OpenAICompatibleAPI]] — the API standard this proxy implements
- [[ChatCompletions]] — the OpenAI endpoint being proxied
- [[FlaskRouteAuth]] — authentication mechanism for Flask routes

## Contradictions
- None identified

---
title: "JSON Serialization"
type: concept
tags: [python, json, serialization, data-conversion]
sources: [llm-response-serialization-tests]
last_updated: 2026-04-08
---

## Summary
JSON serialization in Python converts Python objects to JSON-compatible string representations. Custom serializers handle non-standard types like datetime objects that aren't natively JSON-serializable.

## Key Details
- **json.dumps()**: Serializes Python objects to JSON string
- **default parameter**: Custom encoder function for non-serializable types (e.g., datetime, sets)
- **model_dump(mode="json")**: Pydantic method that applies JSON type conversions automatically

## WorldAI Usage
The mvp_site.serialization module provides json_default_serializer for handling datetime and other complex types during JSON encoding.

## Related Concepts
- [[PydanticSerialization]] — dict conversion before JSON encoding
- [[LLMResponse]] — response object requiring JSON serialization

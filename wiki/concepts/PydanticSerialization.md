---
title: "Pydantic Serialization"
type: concept
tags: [python, pydantic, serialization, data-conversion]
sources: [llm-response-serialization-tests]
last_updated: 2026-04-08
---

## Summary
Pydantic serialization is the process of converting Pydantic BaseModel objects to dictionary representations for JSON encoding. The model_dump() method converts a Pydantic model to a dict, while model_dump(mode="json") additionally converts datetime objects to ISO 8601 strings.

## Key Details
- **model_dump()**: Converts Pydantic model to plain dict
- **model_dump(mode="json")**: Converts datetime/date objects to ISO 8601 string format for JSON compatibility
- **use_enum_values**: Pydantic option to serialize enums by their value rather than the enum object

## Usage in WorldAI
The LLMResponse.to_dict() method uses model_dump(mode="json") to ensure structured_response containing Pydantic models is properly serialized for API responses.

## Related Concepts
- [[JSONSerialization]] — JSON encoding after dict conversion
- [[LLMResponse]] — class using Pydantic serialization

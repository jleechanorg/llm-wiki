---
title: "Chat Completions"
type: concept
tags: [openai, api, llm, conversation]
sources: []
last_updated: 2026-04-08
---

## Definition
An OpenAI API endpoint that generates conversational responses based on a series of messages (system, user, assistant) as input.

## API Structure
```json
{
  "model": "gemini-3-flash-preview",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "hello"}
  ],
  "temperature": 1.0,
  "max_tokens": 512,
  "stream": false
}
```

## Key Parameters
- **model**: The LLM to use (e.g., gemini-3-flash-preview)
- **messages**: Array of message objects with role and content
- **temperature**: Sampling temperature (0-2)
- **max_tokens**: Maximum tokens to generate
- **stream**: Whether to use server-sent events streaming
- **tools**: Function calling definitions
- **response_format**: Output format constraints (e.g., json_object)

## Related Concepts
- [[OpenAICompatibleAPI]] — the API standard this endpoint follows
- [[PayloadValidation]] — the process of validating request parameters

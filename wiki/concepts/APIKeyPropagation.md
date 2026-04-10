---
title: "API Key Propagation"
type: concept
tags: [api, keys, propagation]
sources: []
last_updated: 2026-04-08
---

Pattern of passing user-provided API keys through multiple layers of the application stack. In GeminiProvider, the api_key parameter flows from get_client through to generate_json_mode_content and ultimately to genai.Client initialization.

## Flow
1. User provides API key in settings
2. get_client(api_key=...) receives key
3. generate_json_mode_content passes key to get_client
4. genai.Client initialized with provided key

## Related
- [[GeminiProvider]] — implements propagation
- [[BYOK]] — pattern this enables

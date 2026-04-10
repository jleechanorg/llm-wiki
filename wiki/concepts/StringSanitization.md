---
title: "String Sanitization"
type: concept
tags: [security, string-processing, sanitization]
sources: ["input-validation-module-tests"]
last_updated: 2026-04-08
---

## Definition
String sanitization is the process of removing or encoding dangerous characters from user input to make it safe for storage, display, or processing.

## Key Techniques
- **Null byte removal**: Null bytes (`\x00`) can truncate strings in C-based systems
- **Length truncation**: Enforce maximum length to prevent buffer overflow
- **Unicode normalization**: Convert combining characters to composed forms (e.g., e\u0301 → é)
- **HTML encoding**: Escape `<`, `>`, `&` for safe display
- **URL encoding**: Encode special characters for URL contexts

## Common Attack Vectors Prevented
- Null byte injection
- Buffer overflow
- Unicode homograph attacks
- Cross-site scripting (XSS)

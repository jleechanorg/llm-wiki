---
title: "HTML Whitespace Handling"
type: concept
tags: [html, whitespace, filtering, choice-matching]
sources: ["test-pdf-generation-and-export"]
last_updated: 2026-04-08
---

## Description
Technique for filtering HTML-encoded whitespace characters (like &#32;) in choice matching. Prevents HTML-encoded whitespace-only choices from matching user input, ensuring choices with encoded whitespace are treated as non-matching (freeform).

## Connections
- [[document_generator]] — implements choice matching with whitespace filtering
- [[PDF Generation]] — tested in same test file
- [[Choice Type Detection]] — returns "freeform" when no match found

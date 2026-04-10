---
title: "document_generator"
type: entity
tags: [python, module, pdf, mvp-site]
sources: ["test-pdf-generation-and-export"]
last_updated: 2026-04-08
---

## Description
Module in mvp_site that handles document generation, including PDF export via generate_pdf and story text extraction from context via get_story_text_from_context.

## Connections
- [[Flask]] — uses Flask for test endpoint
- [[PDF Generation]] — core functionality
- [[get_story_text_from_context]] — extracts text from story context
- [[generate_pdf]] — generates PDF files

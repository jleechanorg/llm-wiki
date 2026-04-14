---
title: "Document Generator"
type: source
tags: [export, pdf, docx, campaign]
sources: [mvp-site-document-generator]
last_updated: 2025-01-15
---

## Summary

Campaign document generation system for multi-format export (PDF, DOCX, TXT). Processes story logs into formatted, exportable documents.

## Key Claims

- **Multi-format export**: PDF, DOCX, TXT support
- **Enhanced story formatting**: Scene numbers, session headers, resources, dice rolls
- **Choice detection**: Identifies freeform vs predefined choice actions
- **Living world integration**: Formats debug events (faction updates, rumors, complications)
- **DejaVu Sans font**: Custom font for Unicode support in PDFs

## Key Functions

| Function | Purpose |
|----------|---------|
| generate_pdf() | PDF generation with FPDF |
| generate_docx() | DOCX generation with python-docx |
| generate_txt() | Plain text export |
| format_story_entry() | Single entry formatting with metadata |
| get_story_text_from_context_enhanced() | Full story log formatting |
| get_selected_choice() | Finds matching planning block choice |

## Connections

- [[mvp-site-firestorm-service]] - Story log retrieval
- [[mvp-site-dice]] - Dice roll formatting

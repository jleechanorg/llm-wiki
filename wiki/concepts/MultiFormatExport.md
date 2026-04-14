---
title: "MultiFormatExport"
type: concept
tags: [export, pdf, docx, txt, document-generation, campaign]
sources: [mvp-site-document-generator]
last_updated: 2026-04-14
---

## Summary

The campaign document generation system in WorldAI that exports story logs into multiple formats: PDF (with FPDF), DOCX (with python-docx), and TXT. Supports enhanced story formatting with scene numbers, session headers, resources, dice rolls, choice detection (freeform vs predefined), and living world integration (faction updates, rumors, complications).

## Key Claims

### Export Formats
| Format | Library | Features |
|--------|---------|----------|
| PDF | FPDF | DejaVu Sans Unicode font, scene headers, dice roll formatting |
| DOCX | python-docx | Full formatting, embedded resources |
| TXT | built-in | Plain text, universal compatibility |

### Formatting Features
- Scene numbers and session headers
- Resource tracking display
- Dice roll formatting (via [[mvp-site-dice]])
- Choice detection: freeform vs predefined action classification
- Living world events: faction updates, rumors, complications

### Core Functions
- `generate_pdf()` — PDF generation with Unicode support
- `generate_docx()` — DOCX generation with full formatting
- `generate_txt()` — Plain text export
- `format_story_entry()` — Single entry formatting with metadata
- `get_story_text_from_context_enhanced()` — Full story log formatting
- `get_selected_choice()` — Planning block choice matching

## Connections

- [[mvp-site-document-generator]] — implementation source
- [[mvp-site-firestorm-service]] — story log retrieval
- [[mvp-site-dice]] — dice roll formatting in exports
- [[PDFGeneration]] — PDF-specific generation details
- [[DOCXGeneration]] — DOCX-specific generation details
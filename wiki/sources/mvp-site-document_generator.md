---
title: "document_generator.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Document generation system for exporting campaign story logs to multiple formats (PDF, DOCX, TXT). Processes story entries with enhanced formatting including scene numbers, session headers, resources, dice rolls, and choice detection.

## Key Claims
- Generates PDF via fpdf, DOCX via python-docx, and TXT formats
- Enhanced formatting includes scene numbers, session headers (timestamps, location, status), resources, dice rolls
- Choice detection distinguishes between planning block choices and freeform player actions via `get_choice_type()` and `get_selected_choice()`
- Debug event formatting extracts living world updates: background events, faction updates, rumors, scene events, complications, NPC status changes
- Uses DejaVu Sans font for Unicode support in PDFs
- Choice matching uses text normalization with multiple fallback methods (direct match, title prefix, exact match)

## Connections
- [[mvp_site_capture]] — works with captured story logs for export
- [[mvp_site_main]] — related to campaign export functionality
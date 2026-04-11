---
title: "Document Generation System"
type: source
tags: [document-generation, export, pdf, docx, campaign, story-log]
source_file: "raw/document-generation-system.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module for generating campaign documents in multiple formats (PDF, DOCX, TXT). Processes story logs from campaigns and converts them into formatted, exportable documents suitable for sharing or archiving.

## Key Claims
- **Multi-format Export**: Supports PDF, DOCX, and TXT formats with consistent formatting
- **Story Context Processing**: Extracts and formats story text from campaign logs
- **Custom Font Support**: Uses DejaVu Sans for better Unicode typography
- **Actor Labeling System**: Categorizes content as Story, God, or Main Character
- **Debug Event Extraction**: Formats living world updates including background events, faction updates, rumors, and scene events

## Architecture
- Format-specific generation functions (generate_pdf, generate_docx, generate_txt)
- Shared story text processing via get_story_text_from_context
- Configurable styling constants
- Safe file handling with cleanup

## Dependencies
- fpdf: PDF generation library
- python-docx: DOCX document creation
- DejaVu Sans font: Custom font for Unicode support

## Connections
- [[WorldArchitect]] — the project this module belongs to
- [[Campaign Export]] — related concept for exporting campaign data

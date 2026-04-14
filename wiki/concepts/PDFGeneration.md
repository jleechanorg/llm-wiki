---
title: "PDFGeneration"
type: concept
tags: [pdf, document-generation, fpdf, unicode, export]
sources: [mvp-site-document-generator]
last_updated: 2026-04-14
---

## Summary

PDF document generation for WorldAI campaign exports using FPDF library. Supports Unicode characters via DejaVu Sans font, enabling proper display of international characters and special symbols in exported campaign documents. Includes scene headers, dice roll formatting, and living world event documentation.

## Key Claims

### Unicode Support
- DejaVu Sans font embedded for Unicode character support
- Non-Latin scripts and special characters rendered correctly

### PDF Features
- Scene numbers and session headers
- Dice roll formatting in PDF output
- Resource tracking display
- Living world integration (faction updates, rumors, complications)

## Connections

- [[MultiFormatExport]] — broader export system with PDF as one format
- [[mvp-site-document-generator]] — implementation source
- [[DOCXGeneration]] — alternative document format
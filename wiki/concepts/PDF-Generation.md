---
title: "PDF Generation"
type: concept
tags: [pdf, document, export, testing]
sources: ["test-pdf-generation-and-export"]
last_updated: 2026-04-08
---

## Description
Process of generating PDF documents from story text and campaign metadata. The document_generator.generate_pdf function creates PDF files that start with %PDF- header. Requires assets/DejaVuSans.ttf font file.

## Connections
- [document_generator](../entities/document_generator.md) — implements PDF generation
- [Flask](Flask.md) — serves PDF via HTTP endpoint
- [[HTML Whitespace Handling]] — related test for choice matching

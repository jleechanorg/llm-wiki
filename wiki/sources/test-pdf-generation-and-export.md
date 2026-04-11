---
title: "PDF Generation and HTML Whitespace Choice Tests"
type: source
tags: [python, testing, flask, pdf, html, whitespace, document-generator]
source_file: "raw/test_pdf_generation_and_export.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test coverage for PDF generation via document_generator and HTML whitespace handling in choice matching. Tests validate that the Flask export endpoint can generate valid PDF files and that HTML-encoded whitespace choices are properly ignored.

## Key Claims
- **PDF generation**: Tests that document_generator.generate_pdf produces valid PDF files (starts with %PDF-)
- **Font dependency**: Test gracefully skips if assets/DejaVuSans.ttf is missing
- **HTML whitespace filtering**: Tests verify that HTML-encoded whitespace like &#32; does not match normal user input
- **Choice type detection**: Returns "freeform" when no matching choice is found rather than crashing

## Key Quotes
> "HTML-encoded whitespace choices should not match any user input"

## Connections
- [[document_generator]] — module under test
- [[Flask]] — testing framework used
- [[PDF Generation]] — core functionality tested
- [[HTML Whitespace Handling]] — concept for filtering encoded whitespace in choices

## Contradictions
- None detected

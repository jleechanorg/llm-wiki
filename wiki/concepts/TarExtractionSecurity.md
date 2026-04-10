---	itle: "Tar Extraction Security"
type: concept
tags: [tar, security, extraction, path-traversal]
sources: []
last_updated: 2026-04-08
---

## Description
Tar extraction security involves validating tar archives before extraction to prevent path traversal attacks. Key checks include:
- Handling archives created with `tar -C dir -cf archive.tar .` (dot-root entries)
- Blocking symlinks with linknames pointing outside the destination directory

## Related Pages
- [[PreflightModelDockerTddTests]] — tests validate _safe_extract_tar function

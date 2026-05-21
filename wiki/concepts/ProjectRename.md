# ProjectRename

A mechanical `s/old/new/g` across all files cannot distinguish between categories of name references. Each category needs different handling:

## Categories

1. **Current identity** — Should be renamed (binary names, package.json, import paths)
2. **Historical references** — Must preserve old name ("formerly OldName", changelog entries)
3. **File format identifiers** — Renaming extensions changes the file format (.py → .yaml is not a rename)
4. **Path references** — Must point to real targets after rename (Docker volumes, repo URLs, binary paths)
5. **Self-referential text** — Where both old and new appear, only the old should change

## Verification

After any rename: `grep -r "oldname" .` — every remaining hit should be intentional (historical, upstream, third-party).

## Related

- [[DockerVolumeMigration]] — Named volumes need explicit rename
- [[GreenGateCI]] — Deterministic CI unaffected by naming
- Source: blind-rename-pitfalls-2026-05-14.md, PR #568

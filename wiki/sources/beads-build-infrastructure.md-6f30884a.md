---
title: "Beads Build and Version Infrastructure"
type: source
tags: [beads, build, versioning, goreleaser, ldflags, devops]
sources: []
source_file: docs/noridoc-build-infrastructure.md
last_updated: 2026-04-07
---

## Summary

The Beads project uses a coordinated build and version reporting system ensuring all installation methods (direct `go install`, `make install`, GitHub releases, Homebrew, npm) produce binaries with complete version information including git commit hash and branch name. This infrastructure is critical for debugging, auditing, and user support.

## Key Claims

- **Version Information Pipeline**: Build time extraction via shell commands (Makefile) or goreleaser templates passes git info to Go compiler via `-X` ldflags, then runtime functions in `version.go` retrieve and display the info
- **Multiple Installation Methods**: Supports `make install`, `go install ./cmd/bd`, GitHub releases (goreleaser), Homebrew, npm, and `./scripts/install.sh` while maintaining version consistency
- **Goreleaser Configuration**: Builds for 5 platforms (Linux amd64/arm64, Darwin amd64/arm64, Windows) with identical ldflag patterns setting Version, Build, Commit, and Branch
- **Critical Design Decision**: Go toolchain auto-embeds VCS info with `go build` but NOT with `go install` — explicit ldflags required to ensure all installation paths include version info

## Key Quotes

> "The Go toolchain (as of 1.18+) can automatically embed VCS information when compiling with `go build`, but this does NOT happen with `go install`. This creates an asymmetry"

> "This ensures: Users who run `make install` get full version info, Users who run `go install ./cmd/bd` need to explicitly pass ldflags"

## Connections

- [[Beads Performance Benchmarks]] — same project, complementary focus (benchmarks vs build system)
- [[beads-benchmarks.md-4fd01b62.md]] — related benchmark infrastructure

## Contradictions

- None identified
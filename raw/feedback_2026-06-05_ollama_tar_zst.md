---
name: ollama-release-format-zst
description: Ollama ≥0.30.x ships .tar.zst not .tgz — Dockerfile needs zstd package
type: feedback
bead: none
---

Ollama releases from v0.30.x use `.tar.zst` (zstandard) format instead of `.tgz`. Docker builds targeting these versions must `apt-get install zstd` and extract with:
```bash
zstd -d /tmp/ollama.tar.zst -o /tmp/ollama.tar
tar -C /usr/local -xf /tmp/ollama.tar
```
Do not use the install.sh approach (requires sudo, environment issues in containers). Do not assume `.tgz` format for Ollama installs.

**Why:** Cloud Build failed silently with a `.tgz`-named binary that was actually `.tar.zst` until we identified the release format change for v0.30.5.

**How to apply:** Every time a Dockerfile installs Ollama, check the GitHub release asset names for the target version before writing the extraction commands.

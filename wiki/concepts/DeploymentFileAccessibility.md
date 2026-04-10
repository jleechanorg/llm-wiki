---
title: "DeploymentFileAccessibility"
type: concept
tags: [deployment, docker, testing, file-paths]
sources: ["deployment-build-world-files-accessibility-tests.md"]
last_updated: 2026-04-08
---

## Description
The challenge of ensuring files are accessible in deployment environments where the directory structure differs from development. Tests validate that file loading works in the target Docker environment, not just locally.

## Key Patterns
- **Relative Path Assumptions**: Code using __file__-relative paths assumes files are co-located in the built image
- **Copy Operations**: deploy.sh must explicitly copy resource files into the Docker context
- **Early Testing**: Unit tests can simulate Docker build context to catch issues before deployment

## Related
- [[DockerBuildContext]] — where file accessibility must be validated
- [[DeploySh]] — the mechanism that makes files accessible

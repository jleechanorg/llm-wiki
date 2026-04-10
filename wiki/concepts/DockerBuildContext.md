---
title: "DockerBuildContext"
type: concept
tags: [deployment, docker, file-paths, context]
sources: ["deployment-build-world-files-accessibility-tests.md"]
last_updated: 2026-04-08
---

## Description
The Docker build context determines what files are available during image construction. When the working directory is changed to mvp_site (simulating Docker build), relative file paths resolve differently than in local development — files at the project root are no longer accessible.

## Key Details
- Docker build context is the directory where Docker runs the build command
- Files outside the context must be explicitly copied in
- __file__-relative paths resolve relative to the module's location within the built image
- World files at project root need to be copied to mvp_site/world during deploy.sh

## Related
- [[WorldLoader]] — uses __file__-relative paths that require files to be in Docker context
- [[DeploySh]] — copies files into Docker build context before image creation

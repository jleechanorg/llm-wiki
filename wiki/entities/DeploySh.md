---
title: "DeploySh"
type: entity
tags: [deployment-script, docker, automation]
sources: ["deployment-build-world-files-accessibility-tests.md"]
last_updated: 2026-04-08
---

## Description
Deployment shell script that copies world content files to the mvp_site directory before Docker build. Without this copy operation, world_loader.py cannot find world files in the Docker build context.

## Key Behavior
- Uses `shutil.copytree` to copy world/ directory to mvp_site/world
- Must run before Docker image build to ensure world files are included
- Failure to copy results in FileNotFoundError at runtime when world content is loaded

## Related
- [[WorldLoader]] — depends on world files being copied by deploy.sh
- [[DockerBuildContext]] — the target environment where files must be accessible

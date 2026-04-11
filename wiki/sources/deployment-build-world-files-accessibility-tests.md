---
title: "Deployment Build World Files Accessibility Tests"
type: source
tags: [python, testing, deployment, docker, file-paths, world-content]
source_file: "raw/test_deployment_build_world_files_accessibility.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating that world files are accessible in Docker deployment context. The tests simulate the Docker build environment to catch deployment issues early, verifying world content loading works correctly after the deploy.sh copy operation.

## Key Claims
- **Pre-Deploy Inaccessibility**: World files are NOT accessible from the mvp_site directory without copying (reproduces the bug)
- **Post-Copy Accessibility**: After deploy.sh copies world files to mvp_site/world, loading succeeds
- **Path Resolution**: world_loader.py uses __file__-relative paths to locate world content
- **Docker Build Simulation**: Tests simulate Docker build context by changing working directory to mvp_site

## Key Test Cases
- `test_world_files_not_accessible_without_copy`: Verifies FileNotFoundError when world files aren't copied
- `test_world_files_accessible_after_copy`: Verifies successful loading after shutil.copytree operation

## Connections
- [[WorldLoader]] — module that loads world content for system instructions
- [[DeploySh]] — deployment script that copies world files to mvp_site
- [[DockerBuildContext]] — Docker build environment where file accessibility differs from local development

## Contradictions
- None identified

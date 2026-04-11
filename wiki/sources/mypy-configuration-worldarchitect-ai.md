---
title: "Mypy Configuration for WorldArchitect.AI"
type: source
tags: [python, mypy, type-checking, configuration, testing]
source_file: "raw/mypy.ini"
sources: []
last_updated: 2026-04-08
---

## Summary
Python mypy configuration file for WorldArchitect.AI project enabling gradual type checking with Python 3.11. Uses a tiered strictness approach: relaxed defaults with targeted strict enforcement for critical modules like firestore_service, gemini_service, and main.

## Key Claims
- **Python 3.11 Target**: Configured for modern Python version
- **Gradual Typing Approach**: Starts with permissive settings, gradually enabling stricter checks
- **Critical Modules Strictness**: firestore_service, gemini_service, main, and schemas.* have disallow_untyped_defs = True
- **Test Isolation**: Excludes testing_framework and defensive_numeric_converter from type checking
- **Third-Party Handling**: Ignores missing imports for firebase_admin and google.*, but enforces pydantic and flask imports

## Key Settings
- **Namespace Packages**: Enabled with namespace_packages = True and explicit_package_bases = True
- **Error Reporting**: Shows error codes and context for better debugging
- **Warning Configuration**: Warns on unused ignores, redundant casts, unreachable code
- **Module Exclusions**: Excludes testing_framework and defensive_numeric_converter from analysis

## Module Strictness Hierarchy
| Module | Strictness |
|--------|------------|
| mvp_site.tests.* | ignore_errors = True |
| mvp_site.mocks.* | ignore_errors = True |
| mvp_site.testing_ui.* | ignore_errors = True |
| mvp_site.firestore_service | disallow_untyped_defs = True |
| mvp_site.gemini_service | disallow_untyped_defs = True |
| mvp_site.main | disallow_untyped_defs = True |
| schemas.* | disallow_untyped_defs = True |

## Connections
- [[TestServiceProvider Implementation]] — test infrastructure that may benefit from type checking
- [[Mock Service Provider Implementation]] — mock services that are excluded from strict checking
- [[Input Validation Utilities]] — validation code that could use stricter type checking

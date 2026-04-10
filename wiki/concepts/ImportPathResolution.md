---
title: "Import Path Resolution"
type: concept
tags: [python, module-import, sys-path]
sources: [standalone-flask-app-starter]
last_updated: 2026-04-08
---

Import path resolution is the process by which Python locates and loads modules when they are imported. The `sys.path` list contains directory paths that Python searches for modules. Adding the current directory to `sys.path` via `sys.path.insert(0, os.path.dirname(__file__))` ensures that modules in the same directory can be imported regardless of the current working directory when the script is executed.

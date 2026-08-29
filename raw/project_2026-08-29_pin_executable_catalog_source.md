# Pin executable catalog source, not only its documentation link

PR #9485 centralized duplicate WorldAI commands and skills into the user-scope
catalog. Linking to `INSTALL.md` at a fixed revision was insufficient because
the document's example cloned the mutable default branch. The corrected flow
checks out catalog SHA `41ce34ba240f4d5e8ff5c479907db4887598ce00`
detached before installation, uses `CLAUDE_HOME` as the installer destination,
and launches verification with `CLAUDE_CONFIG_DIR="$CLAUDE_HOME"`.

Final head `0b3e186877ddc5936e0ffb3ba1d5f168bf738703` passed two independent
25/25-path reviews, exact-head evidence gates, and CI before squash merge
`9a2b26e71a474e3ab86b5486201d6d91fa6f6401`. Reusable rule: independently
verify documentation revision, executable checkout SHA, and runtime discovery.

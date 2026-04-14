Claude Code LA Meetup — Workshop Walkthrough
February 25, 2026


OVERVIEW

Format: 4 unconference tables, 35 minutes each. Pick a table based on interest.

Table 1 — Agents & Subagents: Build your own AI team
Table 2 — Skills & Customization: Teach Claude your patterns
Table 3 — Workflows & Power-User Tips: Level up your daily driver
Table 4 — MCP, Bash & Extending Your Agent: Connect to external systems

After 35 minutes, we regroup and each table shares their best "aha moment."


————————————————————————————————————————


PREREQUISITES (ALL TABLES)

Before starting any table walkthrough:

    # Verify Claude Code is installed
    claude --version

    # Clone the workshop starter repo
    git clone https://github.com/aowen14/dev-agent-workshop-starter.git
    cd dev-agent-workshop-starter

    # Run setup (installs Python + frontend deps, runs tests)
    ./setup.sh

This gives you a product inventory tracker — a full-stack app (FastAPI + React) with 28 products, 24 passing tests, and pre-configured Claude Code assets. Setup takes ~1 minute.

What's in the repo:
  - Backend: FastAPI with CRUD endpoints, filtering, search, and stats (src/)
  - Frontend: React + Tailwind data grid showing products with color-coded statuses (frontend/)
  - Tests: Full pytest suite covering all endpoints (tests/)
  - Claude Code config: A pre-built code-reviewer agent, auto-formatting hooks, and an empty .claude/skills/ directory for you to fill

Start Claude Code:

    claude

Claude reads CLAUDE.md and understands the project immediately.

Bring Your Own Repo: If you'd rather work with your own codebase, all exercises adapt naturally.


————————————————————————————————————————


TABLE 1: AGENTS & SUBAGENTS

Table sign: "Agents & Subagents — Build Your Own AI Team"
Best for: People interested in multi-agent orchestration, delegation, parallel work


Part 1: See Subagents in Action (5 min)

Start a Claude session in your project and paste:

    Use a subagent to investigate this project's structure, list all
    endpoints, and summarize the API surface with request/response schemas.

Watch for: Claude delegates to the Explore agent (Haiku, fast, read-only). The summary comes back clean — all the verbose file reads stayed in the subagent's context.

Run /cost — note how cheap the Explore subagent is.

Try: Compare with asking the same question directly (no subagent):

    /clear
    List all endpoints and summarize the API surface with request/response schemas.

Run /cost again. Discussion: Same result, but the direct approach consumed more of your main context.


Part 2: Use the Pre-Built Agent (10 min)

The repo ships with a code-reviewer agent at .claude/agents/code-reviewer.md. Use it:

    Use the code-reviewer agent to review src/main.py

Discussion: The reviewer can read but NOT edit. Principle of least privilege. It returns findings to your main session as a summary. Look at .claude/agents/code-reviewer.md to see how it's configured — tools, model, review checklist.

Experiment: Create a second agent — a test-writer that's allowed to use Read + Edit + Bash and whose job is to improve test coverage:

    Create a .claude/agents/test-writer.md that:
    - Can Read, Edit, and run Bash commands
    - Uses model: sonnet
    - Its job is to analyze test coverage and write missing tests
    - It should run the tests after writing them to verify they pass

    Then use it: "Use the test-writer agent to improve test coverage for src/database.py"


Part 3: Background Tasks (5 min)

    Run the full test suite in the background

While it runs, keep working:

    Add a PATCH /api/products/{id}/restock endpoint that adds stock to a product

The background task reports results when done. You can also press Ctrl+B to background any running operation.


Part 4: Parallel Subagents (5 min)

    In parallel, use subagents to:
    1. Check this project for security issues
    2. Analyze test coverage and suggest missing tests
    3. Review API design against REST best practices

    Give me a combined report.

Watch: Claude spawns three subagents. Each runs in isolation. Results are synthesized.


Part 5: Build Something Real (10 min)

Choose your own adventure:

Option A — Build a "PR review" agent:

    Create a .claude/agents/pr-reviewer.md that:
    - Checks code quality, security, and test coverage
    - Uses Bash(git diff *) to see what changed
    - Provides feedback in a structured format
    - Has persistent memory (memory: project) so it learns your patterns

    Then use it: "Use the pr-reviewer agent to review all uncommitted changes"

Option B — Build a "documentation" agent:

    Create a .claude/agents/doc-writer.md that:
    - Reads code and generates API documentation
    - Uses Read, Grep, Glob tools (read-only)
    - Uses context: fork for isolation
    - Outputs markdown documentation

    Then use it: "Use the doc-writer agent to generate API docs for this project"

Option C — Try agent teams (experimental):

    # In a new terminal:
    CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude

    Create an agent team with 2 teammates:
    - Backend specialist: review the API implementation
    - QA specialist: review tests and suggest improvements

    Have them coordinate and present findings together.


Table 1 Discussion Prompts
  - When do you use a subagent vs just asking the main agent?
  - What custom agents would be useful in your daily workflow?
  - How do you decide what tools an agent should have access to?


————————————————————————————————————————


TABLE 2: SKILLS & CUSTOMIZATION

Table sign: "Skills — Teach Claude Your Patterns"
Best for: People interested in encoding workflows, team conventions, reusable automation


Part 1: Build a /check-ui Skill from Scratch (12 min)

The .claude/skills/ directory is empty — that's intentional. You're going to build your first skill — one that actually opens the browser and verifies what the UI shows.

The goal: Create a /check-ui skill that combines two techniques: preprocessing (inject API data before Claude sees the prompt) and tool use (Claude opens the browser to visually verify).

First, start the app. In two separate terminals:

    # Terminal 1: backend
    uv run uvicorn src.main:app --reload --port 8000

    # Terminal 2: frontend
    cd frontend && pnpm dev

Open the frontend URL shown (usually http://localhost:5173). You should see a product inventory table with 28 products and colored status badges.

Now, in your Claude session, paste:

    Create .claude/skills/check-ui/SKILL.md with:
    - name: check-ui
    - description: "Verify the inventory app UI by checking what's rendered in the browser"
    - disable-model-invocation: true
    - Dynamic context injection using !`./scripts/check-api.sh 2>&1` to
      pull in the API state as background data
    - Instructions that tell Claude to:
      1. Read the injected API data to understand what the backend reports
      2. Use agent-browser to open the frontend (http://localhost:5173),
         take a snapshot and a screenshot
      3. Compare what the UI shows vs what the API returned — do the stats
         match? Are status badges showing the right colors?
      4. Save screenshot to /tmp/check-ui.png
      5. Report what the API says, what the UI shows, whether they match
      6. Close the browser when done

Test it:

    /check-ui

Claude will:
  1. Inject the API data (28 products, 17/7/4 split) via the ! preprocessor
  2. Open the browser, snapshot the page, take a screenshot
  3. Compare the rendered stats bar and table against the API data
  4. Report that everything matches

Two things happened here:
  - The ! backtick ran check-api.sh unconditionally before Claude saw the prompt (preprocessing)
  - agent-browser was Claude's decision, guided by your instructions

That's the key distinction: ! commands run unconditionally. Tool calls are Claude's choice, guided by your instructions.

Now make a change and check again. In another terminal:

    curl -s -X POST http://localhost:8000/api/products \
      -H "Content-Type: application/json" \
      -d '{"name":"Workshop Badge","category":"Accessories","price":4.99,"stock":0,"sku":"WS-001"}'

Back in Claude:

    /check-ui

The API now reports 29 products / 5 out of stock. Claude opens the browser, sees the new row and updated stats bar, and confirms the UI reflects the change.


Part 2: Auto-Invoked Convention Skill (8 min)

Create a skill that Claude uses automatically when it's relevant:

    Create .claude/skills/api-conventions/SKILL.md with:
    - name: api-conventions
    - description: "API design conventions for this project. Use when creating or modifying endpoints."
    - Contents:
      - All endpoints return JSON directly (no wrapping envelope)
      - Use proper HTTP status codes (201 for creation, 204 for delete, 404 for not found)
      - All input must be validated with Pydantic models
      - Product status is always computed from stock, never stored
      - Use type hints on all function signatures

Test auto-invocation — start a fresh session:

    /clear
    Add a POST /api/products/bulk endpoint that creates multiple products at once

Verify: Claude should follow the conventions (Pydantic validation, proper status codes, computed status) without you mentioning them.


Part 3: Manual Workflow Skill (8 min)

Create a skill for side-effect operations that you trigger explicitly:

    Create .claude/skills/test-and-commit/SKILL.md with:
    - name: test-and-commit
    - description: "Run tests and commit if passing"
    - disable-model-invocation: true
    - argument-hint: [commit message]
    - Instructions:
      1. Run the test suite with pytest
      2. If ALL tests pass: stage changes, commit with the provided message, show the git log
      3. If ANY test fails: show the failures and do NOT commit
      4. Always show a summary of what happened

Test it:

    /test-and-commit "Add bulk product creation endpoint"

Discussion: disable-model-invocation: true prevents Claude from running this automatically. You control when side effects happen.


Part 4: Build Something Real (7 min)

Choose your own adventure:

Option A — Build a "project status" skill with dynamic context:

    Create a skill that generates a project dashboard using:
    - !`git log --oneline -10` for recent commits
    - !`uv run pytest --co -q 2>/dev/null | tail -1` for test count
    - !`curl -s http://localhost:8000/api/stats` for live inventory stats
    Format as a clean dashboard report.

Option B — Build a skill for YOUR workflow:
Think about a repetitive multi-step process you do regularly. Encode it as a skill.

Option C — Enhance /check-ui with arguments:

    Add $0 support to your /check-ui skill so you can run:
      /check-ui Electronics
    and it only checks products in that category.


Table 2 Discussion Prompts
  - What's in your CLAUDE.md that should be a skill instead?
  - What team conventions could you encode and share via git?
  - Auto-invoked vs manual — where do you draw the line?


————————————————————————————————————————


TABLE 3: WORKFLOWS & POWER-USER TIPS

Table sign: "Workflows — Level Up Your Daily Driver"
Best for: Daily users who want to optimize their setup, learn shortcuts, manage context better


Part 1: CLAUDE.md Mastery (5 min)

The repo already has a CLAUDE.md. Read it:

    Show me the CLAUDE.md file and explain what conventions it sets

Now customize it:

    Update CLAUDE.md to add:
    - Convention: never use print() for debugging, use logging module
    - Convention: all new endpoints must have at least 2 tests

Start a fresh session (/clear) and ask Claude to add a feature. Verify it follows your rules.

Power move: Create CLAUDE.local.md for personal preferences that don't go in git:

    Create CLAUDE.local.md with:
    "I prefer verbose explanations. Always show me the git diff after making changes."


Part 2: Hooks — See Auto-Formatting in Action (8 min)

The repo ships with a PostToolUse hook in .claude/settings.json that auto-formats Python files with ruff. See it work:

    Add a /api/products/low-stock endpoint that returns only products with
    stock between 1 and 10. Write it with messy formatting — no consistent
    spacing, weird line breaks.

Verify: The code gets auto-formatted by the hook after Claude writes it. Check .claude/settings.json to see how it's configured.

Bonus: Add a PreToolUse hook that blocks writes to pyproject.toml:

    Add a PreToolUse hook to .claude/settings.json that runs a script
    checking if the file being edited is pyproject.toml, and if so, exits
    with code 2 and the message "Protected file — edit pyproject.toml manually"


Part 3: Context Discipline (8 min)

This is the single most impactful power-user skill. Practice the context lifecycle:

Step 1 — Baseline:

    /context
    /cost

Step 2 — Do some work. Add a feature, run tests, ask questions. Use Claude normally for 5 minutes.

Step 3 — Check again:

    /context
    /cost

Step 4 — Compact with focus:

    /compact "Focus on the API endpoints and test coverage. Forget the setup steps."

Step 5 — Check the recovery:

    /context

Step 6 — Try the subagent approach. Delegate verbose work:

    Use a subagent to run all the tests and report only failures with their error messages

vs. directly:

    Run pytest with verbose output

Compare /context after each. The subagent approach keeps your main context clean.


Part 4: Session Management (4 min)

    /rename my-workshop-session

Close Claude (Ctrl+C). Resume:

    claude --resume my-workshop-session

Everything is preserved. Try asking about what you were working on — Claude remembers.


Part 5: Keyboard Shortcut Speed Run (5 min)

Practice these in rapid succession:

    1.  Shift+Tab — cycle to Auto-Accept Edits mode
    2.  Ask Claude to make a quick change — it edits without asking permission
    3.  Shift+Tab — cycle to Plan mode
    4.  Ask Claude to add a complex feature — watch it plan without modifying
    5.  Shift+Tab — back to Normal mode
    6.  Option+P / Alt+P — switch model to Haiku for a quick question
    7.  Option+P again — switch back to Sonnet
    8.  Option+T / Alt+T — toggle extended thinking on for a complex question
    9.  Ctrl+O — toggle verbose output to see Claude's thinking
    10. Start a long operation, then Ctrl+B — background it


Part 6: Build Your Workflow (5 min)

Challenge: Set up your ideal Claude Code configuration:

    1. A CLAUDE.md with your actual project's conventions
    2. One hook that automates something you do manually today
    3. One session management habit (naming convention, when to /clear)

If you brought your own repo, try applying these to it.


Table 3 Discussion Prompts
  - What's your biggest context management pain point?
  - What do you automate with hooks vs leave to Claude's judgment?
  - Plan mode vs Auto-Accept — what's your workflow?


————————————————————————————————————————


TABLE 4: MCP, BASH & EXTENDING YOUR AGENT

Table sign: "Extend Your Agent — MCP, Bash & Beyond"
Best for: People who want to connect Claude to external systems, build custom toolchains


Part 1: Bash — The Universal Tool Layer (8 min)

Claude can use ANY CLI tool. No setup needed. Try these with the inventory app:

Git analysis:

    Analyze the git history of this project. Show me the commit story,
    most-edited files, and how the project was built incrementally.

Live API exploration:

    Use curl to explore the inventory API at localhost:8000.
    Show me the stats, then find all out-of-stock products,
    then create a new product and verify it appears.

System info:

    What Python packages do I have installed? Show me the top 10 largest
    ones by disk size.

Discussion: No MCP server needed for any of this. Bash + installed CLIs cover an enormous range. Zero context overhead at startup.


Part 2: Build a Script Claude Can Use (7 min)

Create a utility that becomes part of Claude's toolkit:

    Create a scripts/project-health.sh that:
    1. Runs the test suite and captures pass/fail count
    2. Runs ruff check and counts issues
    3. Counts total lines of Python code (excluding .venv)
    4. Checks for any TODO or FIXME comments
    5. Outputs a formatted health report
    6. Exits 0 if healthy (tests pass, <5 lint issues), 1 if unhealthy

    Make it executable with chmod +x

Reference it in CLAUDE.md:

    Add to CLAUDE.md: "Run ./scripts/project-health.sh before committing
    to verify project health. Fix any issues it reports."

Test:

    /clear
    Make a small change and prepare to commit

Observe: Claude runs your script as part of its workflow. Your scripts = Claude's tools.


Part 3: MCP Server Setup (10 min)

Option A — If you have gh CLI installed and authed:

    # Outside of Claude, in your terminal:
    claude mcp add --transport http github https://api.githubcopilot.com/mcp/

Restart Claude and try:

    Use the GitHub MCP to show me my most recent open pull requests

Now compare with Bash:

    Use the gh CLI to show me my most recent open pull requests

Run /context after each. Discussion: Both work. Which consumed more context? Which gave richer data?

Option B — If no gh CLI, try a local MCP server:

    # Outside of Claude, in your terminal:
    claude mcp add --transport stdio filesystem -- npx -y @anthropic-ai/mcp-filesystem ~/dev-agent-workshop-starter

Then in Claude:

    Use the filesystem MCP to explore this project

Check tool search:

    /mcp
    /context

See how MCP tool definitions consume context. If you had 5+ servers, you'd want:

    export ENABLE_TOOL_SEARCH=auto:5


Part 4: Compose All Three (10 min)

Build a skill that orchestrates Bash and MCP together:

    Create .claude/skills/ship-it/SKILL.md with:
    - name: ship-it
    - description: "Pre-flight checks and ship"
    - disable-model-invocation: true
    - Dynamic context injection:
      - !`git status --short`
      - !`git log --oneline -5`
      - !`./scripts/project-health.sh 2>&1`
    - Instructions:
      1. Review the injected project health report
      2. If health check failed: list issues and stop
      3. If health check passed:
         a. Use git (via Bash) to stage and commit with a descriptive message
         b. Show the commit
         c. If gh CLI is available, create a draft PR
      4. Summarize what was shipped

Test:

    /ship-it

This is the composition pattern: Skill provides choreography. Bash provides CLI access. Dynamic injection provides live data. MCP provides external system connections where needed.


Table 4 Discussion Prompts
  - What CLI tools does Claude already have access to that you haven't tried?
  - What external systems would you connect via MCP?
  - Bash vs MCP — when does the structured approach win?


————————————————————————————————————————


REGROUP (10 min)

Each table shares one key takeaway or "aha moment" with the room.

Facilitator prompts:
  - Table 1: What's the most useful custom agent someone built?
  - Table 2: What workflow did someone encode as a skill?
  - Table 3: What shortcut or context trick surprised people?
  - Table 4: What creative Bash + MCP composition did someone build?



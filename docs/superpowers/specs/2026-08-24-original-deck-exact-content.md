# Original deck — exact content extraction (2026-08-24)

**Source:** `https://docs.google.com/presentation/d/1JY7CmnE33b9_R1IhHyv0M-WYw-kdTJFEqskoR_PRqBc/edit`
Presentation title (as stored): "Develop at Idea Velocity: AI coding stack + WorldAI: V0.1 (latest)"
14 slides. Slides 1-13 are full-bleed uploaded images (no native text — content
extracted by reading the rendered image). Slide 14 is native Google Slides
text/shapes.

Real image assets downloaded to
`~/roadmap/llm-wiki/original-deck-assets/orig-slide-01.png` through `-14.png`
(slides 1-13 at 2048x1152; slide 14's decorative asset at 540x540 — its real
content is native text, listed below).

**Status: this file is a pure [UNCHANGED] transcription of the real original.**
No wording has been touched. This is the baseline for the next step: deciding,
slide by slide, what stays [UNCHANGED], what gets a [WORDING EDIT], and what
[NEW] slides (if any) get added — per `.claude/skills/slides/SKILL.md`.

---

## Slide 1 — Title [UNCHANGED]

- Top-left: "JEFFREY LEE-CHAN · 2026"
- Top-right: "PRESENTATION · 15 SLIDES" *(note: says 15, deck actually has 14 — a
  pre-existing inconsistency in the original, not something I introduced)*
- Eyebrow: "● AI CODING · STACK & CASE STUDY"
- H1: "AI coding stack **+ *WorldAI***" (WorldAI in rust italic serif)
- Subtitle: *"Develop at **idea velocity** — a tour of the autonomous pipeline
  and the game I built with it."*
- Byline: "Jeffrey Lee-Chan" / "**Head of Vibe Coding** · Snapchat · ex-Google"
- Right: "linkedin.com/in/**jeffrey-lee-chan**" / "github.com/**jleechanorg**"
- Right: QR code image, caption "SCAN TO CONNECT"
- Asset: `orig-slide-01.png`

## Slide 2 — The Autonomous Pipeline [UNCHANGED]

- Eyebrow: "§ 02 · THE AUTONOMOUS PIPELINE"
- H1: "One Slack message, *all the way to green checks*"
- Header-right: "A single natural-language message triggers the entire flow." /
  "**Every stage is automated and evidence-backed.**"
- 5 cards (PH 01–05), connected by → arrows:
  1. **Natural language** — `A short request in Slack: "add a corruption
     tracker". No tickets, no specs.` — tag: `↳ slack · trigger`
  2. **Context + Memory** — `Hermes pulls the relevant repo, docs, prior
     threads, and what your past goals were.` — tag: `↳ docs · gmail · slack
     history`
  3. **Parallel agents** — `Orchestrator fans out to multiple worker agents in
     worktrees — Claude Code, Codex, Cursor CLI — running in parallel.` — tag:
     `↳ 10-20 agents · max parallelism`
  4. **CI & Review** — `Tests, lint, type-check, regression suite — all green
     before a human sees the diff.` — tag: `↳ ci on PR · auto-label`
  5. **Proof-First** — `PR lands with evidence bundle attached: logs,
     screenshots, git diff. No vibes, only receipts.` — tag: `↳ evidence on
     every claim`
- Bridge line: *"No manual re-entry of context, no babysitting CI, no chasing
  reviewers."* **Every stage is automated and evidence-backed.**
- Footer: "02 / 15" · "→ idea → PR, hands-off"
- Asset: `orig-slide-02.png`

## Slide 3 — What is Hermes / Openclaw [UNCHANGED]

- Eyebrow: "§ 03 · WHAT IS HERMES / OPENCLAW"
- H1: "One AI *that talks to everything you do*"
- Header-right: "The concept matters more than any particular code or repo." /
  "Three pillars: **frictionless I/O, central data, memory.**"
- 3 cards (P·01–03):
  1. **Frictionless comms** — *"Talk to your AI the way you talk to a
     teammate."* — `Triggered the same way you message a person. No special
     CLI, no IDE plugin, no remembering which tool does what.` — pills: Slack,
     WhatsApp, Telegram, SMS
  2. **Central data access** — *"The more access, the more powerful."* —
     `Hermes reads from everything you can read. The breadth of context is the
     multiplier — code is just one input.` — pills: Google Docs, Gmail, Slack
     history, Calendar, Drive
  3. **Memory** — *"Replace more and more of your decisions over time."* — `It
     remembers your goals, your patterns, your past calls. Each request
     reasons against your history, not a cold start.` — pills: goals, past
     actions, preferences, style
- Footer: "03 / 15" · "→ concept, not codebase"
- Asset: `orig-slide-03.png`

## Slide 4 — The Agent Pyramid [UNCHANGED]

- Eyebrow: "§ 04 · MY STACK"
- H1: "The agent pyramid, *top to bottom*"
- Header-right: "A central AI hands work down through orchestrators,
  terminals, worker agents, and sub-agents." / "**Each layer multiplies the
  one below.**"
- **Left: a real AI-generated 3D graphic** — a glowing blue pyramid on a dark
  circuit-board background, four tiers labeled top to bottom: "OpenClaw"
  (apex, glowing diamond) → "Cmux Terminals + Orchestrator Agents" (laptop
  icons) → "Agents" (Claude Code / Codex / Antigravity IDE logos, worktree
  icons) → "Sub-agents & Self-Managing Agents" (robot icons at base).
  **This is the literal "exact original pyramid image" referenced throughout
  this session — a real illustration, not a CSS card grid.**
- Right: 4 stacked cards matching the pyramid tiers:
  1. **★ Openclaw** (highlighted, tag "CENTRAL AI") — `The brain that turns a
     Slack message into a plan and routes work everywhere below.`
  2. **CMUX terminals + orchestrator agents** (tag "AGENT MANAGERS") — `Tiled
     terminals where workers actually run. Orchestrator decides who gets
     what.`
  3. **Agents** (tag "NAMED WORKERS") — `Claude Code, Codex, Cursor CLI,
     Antigravity IDE. Each in its own worktree.`
  4. **Sub-agents & self-managing agents** (tag "DEPTH N+1") — `Specialized
     scoped agents — testing, review, refactor — spawned by the layer above.`
- Footer: "04 / 15" · "⚡ Openclaw is the multiplier at the top"
- Asset: `orig-slide-04.png`

## Slide 5 — Evolution of AI in Coding [UNCHANGED]

- Eyebrow: "§ 05 · THE EVOLUTION OF AI IN CODING"
- H1: "From tools *to self-evolution*"
- Header-right: "Four stages, less human at each." / "Most teams sit at
  **B**. The frontier is moving to **C**."
- Embedded full-width infographic (dark background, 4 colored panels):
  "THE EVOLUTION OF AI IN CODING: FROM TOOLS TO SELF-EVOLUTION"
  - **Stage A — Foundations & IDE Augmentation** (blue): No AI · Auto complete
    (copilot in IDE) · Cursor (code assist in IDE)
  - **Stage B — Agentic Shift & Autonomy** (green): Claude (terminal and
    review code, no more IDE) · Coding parallel (usually worktrees and
    multi-agent) · Openclaw (sort of orthogonal but big multiplier) · Looping
    agents (have them run for 3hr+ of planned work)
  - **Stage C — Advanced Orchestration & Self-Evolution** (orange): Harness
    engineering (maximize agent autonomy and minimize human interaction, "MAX
    AUTONOMY") · Orchestrators (manage 10-20 agents, max parallelize)
  - **Stage D — Self-Evolution (no one yet)** (purple): Self-evolving systems
    that automatically improve their code · "AUTO-IMPROVE" · "NO ONE YET"
  - Top-right label on infographic: "STAGE A → B → C → D"
- Footer: "05 / 15" · "→ less human, more autonomy, every step"
- Asset: `orig-slide-05.png` (this is the exact "appendix A6" slide referenced
  earlier this session — it already exists as a real, finished slide in the
  original deck; it does not need to be built from scratch)

## Slide 6 — Slack Workflow Example [UNCHANGED]

- Eyebrow: "§ 06 · SLACK WORKFLOW"
- H1: "\"Let's test this technique *out.*\""
- Header-right: "One thread → research → 99 replies of agent work." / "Reply
  with the deliverable, no project tracking, no handoff."
- **Left panel: real Slack screenshot** — Jeffrey Lee-Chan message: "Let's
  test this technique out. I want sprites for this campaign" + a linked X/
  Twitter post from @chongdashu about AI-generated game sprites ("Alexiel V2")
  + "99 replies" thread + Hermes app reply: "Let me read the campaign doc and
  check out the technique from that X post. Let me research the technique
  properly. ⏳ Still working... (3 min elapsed — iteration 5/60, running:
  delegate_task)"
- **Right panel: real result screenshot** — Hermes app message "45 minutes
  ago in #worldai - alexiel_v3_comparison.png", a 3x3 grid of actual generated
  anime-style character sprite art ("ALEXIEL V3 — Tall/Lean Proportions")
- Footer: "06 / 15" · "→ one message in, asset out"
- Asset: `orig-slide-06.png`

## Slide 7 — CMUX Terminal Workflow [UNCHANGED]

- Eyebrow: "§ 07 · CMUX TERMINAL WORKFLOW"
- H1: "Hands on the keyboard, *Hermes on standby*"
- Header-right: "I'm still **manually typing** in CMUX terminals most of the
  time." / "Hermes *can* drive them — and one pane sometimes runs multiple
  agents."
- Left: "What you're seeing *terminal multiplexer for agents*" — `The default
  is me — I sit in CMUX, type, navigate, paste, watch. The terminals are how I
  drive.` / `When the work is well-scoped, I let **Hermes** take the wheel: it
  sends keystrokes into a pane on my behalf, watches the output, and reports
  back.` / `A single pane isn't always one agent. Sometimes a pane is a
  manager that *spawns sub-agents inside itself* — one terminal, many minds.`
  — pills: manual by default, hermes-driven on demand, 1 pane → N agents,
  per-pane git worktree, evidence capture
- Right: embedded YouTube video player (thumbnail), title "CMUX terminal
  workflow — live demo", label "CMUX DEMO · YOUTUBE", url
  `youtube.com/qGJZ31t4wj4`, "CLICK TO PLAY"
- Footer: "07 / 15" · "→ I drive, Hermes assists"
- Asset: `orig-slide-07.png`

## Slide 8 — What I'm Building: WorldAI [UNCHANGED]

- Eyebrow: "§ 08 · WHAT I'M BUILDING — WORLDAI"
- H1: "An AI Game Master, *playing live*"
- Header-right: "A production AI tabletop RPG platform." / "Built with the
  stack you just saw — **at idea velocity.**"
- Left: "WorldAI *a digital D&D 5e Game Master*" — `You start a campaign in a
  sentence. The system generates the setting, your character, the rules in
  play, and the opening scene.` / `The world reacts to what you do —
  autonomous factions, dice you cannot fabricate, narrative that remembers a
  thousand turns.` — pills: D&D 5e SRD, 12 specialized agents, 30+ prompt
  files, BYOK, live at worldarchitect.ai
- Right: real WorldAI app screenshot — "WorldAI" header, user
  `jleechan@gmail.com`, campaign "My Epic Adventure" with Debug Mode
  Active / BYOK Active badges, a full campaign-summary chat message
  ("**CAMPAIGN SUMMARY** Title: The Knight of Two Suns / Character: Ser Arion
  val Valerion / Setting: Assiah (The Celestial Imperium)..."), 3 numbered
  choice buttons, character portrait avatar, message input box with "Send"
  button, mode selector (Character / Think-Plan / God)
- Footer: "08 / 15" · "→ worldarchitect.ai"
- Asset: `orig-slide-08.png`

## Slide 9 — Game Summary [UNCHANGED]

- Eyebrow: "§ 09 · GAME SUMMARY"
- H1: "Epic adventure, *or open a bakery*"
- Header-right: "A simulated world that follows D&D rules." / "**Endless
  possibilities** — and you don't always win."
- Left: "Live in a *simulated* world" — `Go on an epic adventure, or relax and
  run a bakery. The world reacts to **you** and changes depending on what you
  do — and generates events just like real life.` — highlighted callout: "★
  I've spent hundreds of hours playing my own game."
- Right: 3 cards (G·01–03):
  1. **D&D ruleset is essential** — `So you don't always win. The roll can
     betray you — and that's the point. Stakes only matter if outcomes are
     uncertain.`
  2. **The world reacts and remembers** — `Factions act on their own goals
     between your sessions. NPCs remember what you did three weeks ago. Time
     keeps passing whether you log in or not.`
  3. **God Mode — change anything** — `Prompt the LLM in plain English to
     rewrite your character, the world, or the rules. The system parses your
     directive and persists it across every future request.`
- Footer: "09 / 15" · "→ hundreds of hours · same engine, still surprising"
- Asset: `orig-slide-09.png`

## Slide 10 — Technical Highlights [UNCHANGED]

- Eyebrow: "§ 10 · TECHNICAL HIGHLIGHTS"
- H1: "Three pieces *that make it work*"
- Header-right: "Context · routing · integrity." / "The next four slides go
  deeper on the whole system."
- 3 cards (T·01–03):
  1. **Context management** — *"so the world never forgets"* — `Up to
     **300k tokens** of context given to the LLM. **BYOK** — you can plug in
     your own model key.` / `The budget is allocated by a **Min-first /
     Fill-to-max** algorithm.` — code block: `40% story · 20% system · 5%
     memories · 3% npcs` / `Then spread the rest evenly; remainder spills into
     story as needed.` — tags: 300k tokens, 5 components, BYOK
  2. **Two-layer inference** — *"cheap fast routing → expensive smart model"*
     — `Layer 1. in-memory FastEmbed classifier decides which agent —
     StoryMode, LevelUp, Combat.` / `Layer 2. primary big frontier model =
     Gemini 3 Flash — best quality/speed/cost tradeoff today.` / `Routing is
     local and free; only the right agent's prompt hits the paid model.` —
     tags: <50ms local L1, 12 agents, Gemini 3 Flash
  3. **Dice rolls** — *"casino-grade fairness"* — `The dice are essential —
     they're what makes the world feel real. Hit a sword strike, convince a
     guard, persuade a king.` / `The LLM *requests* rolls; the server resolves
     them with random.randint() via **code execution**, then verifies with
     cryptographic hashing.` / `Same model as casino software: "I told the LLM
     I'm going to double-check its work."` — tags: 0 fabrication, 4 audit
     signals, verifiable
- Footer: "10 / 15" · "→ next: the full architecture"
- Asset: `orig-slide-10.png`

## Slide 11 — High-Level Architecture [UNCHANGED]

- Eyebrow: "§ 11 · HIGH-LEVEL ARCHITECTURE"
- H1: "Two engines, *one gateway*"
- Header-right: "Client → Gateway → Orchestrator → AI Engine → Gemini →
  audit → Firestore." / "Living World feeds sideways. **Firestore is read in,
  written back.**"
- Full architecture flow diagram (boxes + arrows), layers L1-L5:
  - **Client** (L1) — `frontend_v1/ · Vanilla JS · SSE renderer · planning UI`
  - ↓ HTTP/JSON → **API Gateway · Flask 3.0** (L2, MAIN.PY) — `HTTP + auth ·
    Firebase token · Flask-Limiter 100/hr`
  - ↓ JSON-RPC 2.0 → **Orchestration · MCP Server** (L3) — `world_logic.py ·
    7,273 lines · Validates, sanitizes, applies state delta · SSE producer`
  - ↓ continue_story() → boxed group "★ PROPRIETARY AI ENGINE · NOVEL" (L4):
    **Classifier** (`intent_classifier.py · FastEmbed · <50ms`) → **Multi-
    Agent Router** (`agents.py · 12 agents · 8-level priority chain`) →
    **Prompt Library** (`agent_prompts.py · 30+ files · essentials mode`) →
    **Token Budget** (`context_compaction.py · Min-first · story ≥ 30%`) →
    assembled prompt → **Gemini API** (external, `Flash · code-exec sandbox`)
  - **★ Dice Anti-Fabrication Guard** (L4, NOVEL) — `dice_integrity.py · LLM
    requests rolls; server resolves.` → audited → feeds Gemini box
  - Sideways: **★ Living World** group — Faction System (`faction/ · 12
    factions · battle_sim · ai · resources`) + Social HP + Planning, connected
    via tick events / player actions to the orchestrator, and via a dashed SSE
    stream arrow back to Client
  - ↓ validated state delta → **Firestore** (L5, "Source of truth") →
    atomic write → `firestore_service.py` (`Atomic, whitelist-sanitized
    writes`)
  - Legend (top right): orange = proprietary/novel, peach = living-world
    simulation, gray = persistence, white = standard service
- Footer: "11 / 15" · "⭐ proprietary — AI Engine · Living World"
- Asset: `orig-slide-11.png`

## Slide 12 — Anatomy of One Request [UNCHANGED]

- Eyebrow: "§ 12 · PLAYER ACTION → STREAMING RESPONSE"
- H1: "Anatomy *of one request*"
- Header-right: "A flame chart of the unique work, generic glue elided." /
  "The four ★ orange bars are the parts that don't exist anywhere else."
- Flame-chart / gantt diagram, 5 phases (PH 01-05) across the top (Route
  ~50ms local, Assemble ~100ms, Reason 2-15s dominant, Audit+persist ~30ms,
  Stream continuous), with horizontal bars beneath a left-hand component list:
  - `world_logic.py` (orchestrator, 7,273 lines) — dark gray bar "owns the
    request" spanning the full width
  - ★ `FastEmbed classifier` (intent_classifier.py, 384-dim) — orange bar
    "classify intent" in Route phase
  - ★ `Agent priority chain` (agents.py, 8 levels) — orange bar "pick agent"
    in Route phase
  - ★ `Prompt builder` (agent_prompts.py, 30+ files) — orange bar "build
    prompt" in Assemble phase
  - ★ `Token budget engine` (context_compaction.py) — orange bar "fit budget"
    in Assemble phase
  - `Gemini API` (+ code execution sandbox) — tan bar "reason · roll" in
    Reason phase
  - ★ `Dice integrity audit` (dice_integrity.py, 1,549 lines) — orange bar
    "verify" in Audit+persist phase
  - `Sanitize → Firestore` (whitelist-filtered atomic write) — blue bar
    "persist" in Audit+persist phase
  - `Browser` (SSE client) — dark striped bar "stream" in Stream phase
  - Legend: gray=orchestrator, orange★=WorldAI-unique work, tan=LLM (the
    wall-clock), blue=persistence, black=SSE stream back
- Footer: "12 / 15" · "≈ 80% of wall-clock is the LLM · the ★ work is what
  makes it WorldAI"
- Asset: `orig-slide-12.png`

## Slide 13 — Four Things Nobody Else Does [UNCHANGED]

- Eyebrow: "§ 13 · TRULY NOVEL CAPABILITIES"
- H1: "Four things *nobody else does*"
- Header-right: "No direct equivalent in the public AI TTRPG landscape." /
  "Each tied to specific code refs that can be independently verified."
- 4 cards (N·01–04), 2x2 grid:
  1. **Player-invented persistent laws** — *"God Mode directives"* — `Players
     type natural-language behavioral rules. The server validates,
     timestamps, and injects every directive into *every* subsequent agent
     prompt — newest first. AI Dungeon world info is static facts; this is
     versioned runtime mandates.` — refs: `game_state.py:2755`,
     `agent_prompts.py:1799`, `world_logic.py:5292`
  2. **Zero fabrication** — *"structural prevention of dice cheating"` —
     `LLM must emit tool_requests or trigger code execution; the server runs
     random.randint(). A 1,549-line audit pass scans narrative prose, verifies
     the code-exec path, and tags RNG provenance.` — refs: `dice.py`,
     `dice_integrity.py:54`, `dice_strategy.py`
  3. **Campaign tier system** — *"scoped runtime rule extension"* —
     `Campaigns upgrade to Divine or Sovereign. The matching rule doc is
     appended to every agent's prompt for that request — two simultaneous
     campaigns can run under completely different rule sets with no server
     config change.` — refs: `campaign_divine.py`, `agent_prompts.py:2236`
  4. **Dynamic ruleset ingestion** — *"schemas inferred from pasted docs"* —
     `User pastes a homebrew mechanic in plain English. The LLM acts as a
     schema parser: extracts field, type, range; state_updates initializes
     it; directives.add enforces it. Works because CustomCampaignState is
     declared open.` — refs: `god_mode_instruction.md`,
     `game_state.schema.json:2338`
- Footer: "13 / 15" · "→ verifiable code refs · no fabrication"
- Asset: `orig-slide-13.png`

## Slide 14 — Find Me, Play the Game [UNCHANGED] (native text, not an image)

- Eyebrow: "§ 14 · LINKS & FURTHER READING"
- H1: "Find me, play the game"
- Left panel: "★ CONNECT" — "LinkedIn" *(say hello)* — `DMs open. Especially
  if you're building at the frontier of stages C and D — or if any of this
  sparked an idea you want to riff on.` — `linkedin.com/in/jeffrey-lee-chan`
- Right, 3 stacked cards:
  1. "01 · PLAY" — `worldarchitect.ai` — **WorldAI** *(D&D simulation)* — `The
     live game. Start a campaign in one sentence; BYOK.`
  2. "02 · RESEARCH" — `consensus-ml.ai` — **Consensus ML** *(multi-AI
     research)* — `Cross-model agreement and verification — separate, related
     project.`
  3. "03 · CODE" — `github.com/jleechanorg` — **GitHub** *(everything else)*
     — `My open-source agentic experiments, including the harness that built
     this deck.`
- Closing line: "Thanks for watching. Now go ship something at idea
  velocity."
- Footer: "14 / 14" · "END · JEFFREY LEE-CHAN · 2026"
- No separate image asset — this slide is native text/shapes in the original.

---

## What this means for the live deck (1Zb6sc0HUKOIR...)

Everything currently on the live deck — verification-gap stats, left-shift/
right-shift, craftsmanship-vs-velocity, the 6-step loop diagram, the 4-tier
CSS pyramid, tokenmaxxing, cache-stability, harness-decay, "8 bets," the
postmortem slide — **has no equivalent in this real original**. It was
invented/expanded during this session's work, not reused from the source
deck. That includes the CSS "pyramid" I built and rebuilt multiple times:
the real original pyramid (slide 4 above) is a completely different, real
illustrated graphic that was never actually inserted into the live deck at
any point this session.

**Next step per the /slides skill:** confirm with you which slides from this
real 14-slide original should become the live deck (likely: all of them,
largely as-is), which specific wording updates you want, and which of this
session's invented additions (if any) should be kept as genuinely new slides
— before touching Google Slides again.

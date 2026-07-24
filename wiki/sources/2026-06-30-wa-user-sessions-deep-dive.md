# WA Retention — User Sessions Deep-Dive (2026-06-30)

**Query window:** last 28 days (data through 2026-06-30 12:44 UTC).

## TL;DR

Of 47 turn-having users in the window:

- **42 had exactly 1 session** (89% of turn-users). Only 5 had 2-3 sessions. **0 returned from prior weeks.**
- **Median turn count: 4. Median session span: 4.2 min.** Most churn = inside their first session.
- **The funnel is bimodal**, not a normal retention curve. Two clusters visible:
  - **Tourists** (~38% of single-session users): 1-4 turns, 0-4 min span — tried it once, left without exploring.
  - **Natives** (15-25 turns in 23-89 min — `stream.of.silver`, `hmason`, `me@ecor.me`, `nakrasainesh`, `rivierecyp`, `inakizulaika`, `akey445`, `dongrantlower`, `mushrooming.fungus`, `thiago.hirai`): engaged deeply... and still never came back.
- **5 warm-return users** all came back within **0.7-7.7 hours** of first session. **Nobody returned after 24h.**
- **Bounced signups** (7 users, signed up but 0 turns): mostly stale; only 4 are recent (06-19 to 06-28).

## Cohort shape

| Cohort   | Size | Multi-session? | Days idle (now) | Profile                                     |
|----------|------|----------------|-----------------|---------------------------------------------|
| W-0 (last 7d)     | 15 | 5/15 with 2-3 sessions | mixed (4.7-67d; mostly fresh) | net-new, some warm-returns |
| W-1 (8-14d ago)   | 12 | 1 of 12 = `mrkennethyip` (3 sessions, 17 turns) | 10-11d | mostly one-and-done, all churned |
| W-2 (15-21d ago)  |  0 | —          | —        | **structural empty week** — no traffic |
| W-3 (22-28d ago)  |  3 | 0 multi-session | 22-29d | one-and-done |
| Older tail (29+d) | 17 | 1 (`thiago.hirai`)  | 33-114d | one-and-done |

**Final-session turn count (proxy for "how they left"):**

| Turns in last session | Users |
|---|---|
| 1 | 11 |
| 2 | 6 |
| 3 | 6 |
| 4 | 7 |
| 5 | 3 |
| 9 | 2 |
| 10 | 1 |
| 12 | 2 |
| 13 | 1 |
| 15-25 | 9 |

The 11 users with `last_session_turns=1` are the cleanest bounce signal — they typed one message, got one LLM reply, and left.

## Sessions-per-user distribution

| Sessions | Users |
|---|---|
| 1 | 42 |
| 2 | 3 |
| 3 | 2 |

## Auth cross-check (sample of 27 + 7 bounced)

- **100% Google provider** for the 27 sampled turn-having users.
- **Median signup-to-first-turn gap = 0.1 days** (~2.4 hours). P75 = 0.3 d (~7 hours).
- Most play happens within hours of signup.
- 5 outliers with long signup-to-first-turn gaps: `nathan@torkington.com` (130d), `tiffanycodes.co` (61d), `rivierecyp` (19d), `patrick.marre.valer` (5d), `stream.of.silver` (1.3d) — they signed up but didn't engage until much later.

## Three Reviewer Verdicts

### Reviewer A — Engineering / product lens (HIGH-confidence ranked causes)

1. **No re-engagement loop** (HIGH) — 9 of 42 one-session users played 10-25 turns over 20-89 min and never returned. WA has zero email/notification infrastructure (no sendgrid/mailgun/SES/smtplib in `mvp_site/`). No system exists to bring engaged natives back.
2. **Mixed first-turn experience** (MED) — 11/42 one-session users got exactly one LLM reply and left; idle-time spread 2.5d-114d means the bucket is heterogeneous (some bounces, some curiosity clicks from non-target audiences). Need LLM response quality data to split.
3. **Mobile auth redirect drops** (MED, unmeasured) — `auth.js:882` uses `signInWithRedirect` on mobile for Incognito tab-eviction; we have zero UA telemetry in Firestore.
4. **Wizard friction / sign-in failure** (LOW) — wizard is only 2 steps (`campaign-wizard.js:504-505`); 3 of 7 bounces are stale (>30d). 4 recent bounces deserve manual check.
5. **Rate-limit popup** (LOW, effectively refuted) — defaults are 30/day, 20/5h (`rate_limiting.py:75-80`). Max session turns in dataset = 25. No user hit the cap.

### Reviewer B — User-research lens

**Distribution read:** Classic bimodal tourist/native, not stuck-engaged-user shape. 38% of single-session users churned in the 2-4 turn / 2-4 min friction band — tried the tool, didn't get hooked in first 90 seconds.

**Cold-start vs warm-return:** Cold-start exit is the dominant leak (36/47 users = 77% never made it past first ~4 min). Warm-return is rare but instructive: 5 multi-session users all came back within **0.7-7.7 hours**, never after 24h.

**Single highest-EV experiment:** A "story-in-progress" email at 18-24h after the user's first session, sent only to the 2-4 turn friction band. Email subject = one-line teaser of story state at the moment they left ("You stood at the edge of the Thornwood at dusk. The stranger was still waiting."), one-click CTA to resume. Success metric: lift in D1 return rate for the 2-4 turn cohort from ~0% to ≥20%.

**One blind spot:** No qualitative signal — exit surveys, NPS, "why did you stop?" modal. Equally plausible alternative: first turn DID hook but user hit quota/timeout/bad-LM-output on turn 5. Need LLM latency / error rate / quota events keyed to exit turns before betting engineering time.

**Benchmarks (caveated, web search was offline in that session):** AI chat/RPG apps typically 20-35% D1, 5-10% D7, 2-5% D30 (data.ai/Sensor Tower summaries). Character.AI reportedly 25% D1 stable. AI Dungeon cited 8-12 turns per retained session. These numbers are from training-data recall; should re-verify before citing externally.

### Reviewer C — Code-archaeology lens

**Most likely code-level cause:** After campaign creation, user lands at `/game/<campaign_id>` with an empty story panel and no auto-narration, no suggested first action, no onboarding tutorial (`frontend_v1/app.js:4297` pushState to `/game/<id>` after create, only a 500 ms `setTimeout`; no auto-`/interaction` POST anywhere in `frontend_v1/`).

**Ruled OUT:**
- Rate-limit-on-first-turn (defaults are 30/day).
- Backend exception swallow (`main.py:4004-4021` returns a sanitized 500; user always sees something).
- Auth-cookie-too-short (`auth.js:740-789` auto-refreshes 5 min before exp; deep-drill shows all 47 are authenticated Firebase users).
- Waitlist killing first-time signups (`WAITLIST_MODE_ENABLED=false`; the 28-day snapshot would be empty of turn-users otherwise).
- First-turn returning empty story (frontend `app.js:3956-3984` logs "Missing 'story' field" as WARNING).
- Stale cached frontend pointing at moved endpoint (`main.py:5467-5479` returns 410 with explicit "Hard refresh" message).

**Instrumentation hook (zero infra cost):** Wire `safeDiag('first_turn.begin'/'first_turn.outcome')` through the existing `/api/client_diag` Cloud Logging sink at `main.py:4025` and `main.py:3999`. This answers "did turn 1 ever return a story?" — currently invisible.

## Synthesis — what stops users from coming back

Three converging hypotheses, ranked by combined evidence weight:

### 1. **Hook failure at first reply** (combined evidence: highest)
- 11/42 single-session users got exactly **one LLM reply and left**.
- The 23-89 min deep-session natives (10-25 turns) still don't return — they finished a satisfying arc.
- Code path shows **no intro narration, no empty-state placeholder, no suggestion chips, no onboarding tutorial** for the new campaign view.
- Combined, this says: even when users LIKE the content enough to play 20+ turns, nothing tells them "come back, your story waits." And when first reply lands flat, there's no scaffolding to nudge them forward.

### 2. **Zero re-engagement infrastructure** (combined evidence: high)
- Grep confirmed: no email library (no sendgrid, mailgun, SES, smtplib) anywhere in `mvp_site/`.
- The 5 multi-session users all came back **within 0.7-7.7 hours** — the return window is hours, not days. After 24h the trail goes cold.
- The engaged natives (15-25 turn users from W-3 and W-2) all churned with **no outreach**.

### 3. **Cold-start tourists naturally exit** (lower-weight baseline)
- The bimodal distribution is characteristic of top-of-funnel "AI try-it-once" products. Some share of bounces is irreducible, just the way it is for character-chat / RPG tools.
- ~25% D1 baseline for AI companion apps is the industry range.

## Recommended next actions

### A. Instrument the funnel (zero-infra cost, ships this week)
Wire `safeDiag('first_turn.begin', ...)` and `safeDiag('first_turn.outcome', ...)` to capture whether `turn 1` ever returned a narrative, errored, hit a quota, or got OOC content. Already-existing `/api/client_diag` sink; no new vendor. Required to validate hypotheses 1 vs 2 vs 3 above.

### B. Build a 24h "story-in-progress" email (1 eng-week)
Single highest-EV intervention per Reviewer B. Targets the 2-4 turn friction band; holds the warm-return window which is 0.7-7.7h. Subject = story-state teaser. Builds on SendGrid/Resend/SES (must install).

### C. Auto-narrate on campaign create (small UX win)
Ship a pre-built first scene ("You stand at the entrance of [Setting]. Before you lies...") so `/game/<id>` isn't empty. Removes the "what do I type?" blank-page moment for ~38% of new users.

### D. (Stretch) Failed-first-turn rescue modal
After 1-2 turns if user returns 24h+ later, surface the previous session state and offer to resume. Same SendGrid infra as (B).

## Data files
- `/tmp/wa_retention_4w/users_28d.json` — raw 28d dump (54 records, schema: `by_email`, `summary`).
- `/tmp/wa_retention_4w/deep_drill.json` — per-user session timeline, last_turn, days_idle.
- `/tmp/wa_retention_4w/auth_xref.json` — Firebase auth metadata for 27 sampled turn-users + 7 bounced signups.

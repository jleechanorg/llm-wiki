---
title: "Command Usage — Last 30 Days (2026-02-21 to 2026-03-23)"
type: source
tags: [claude-code, commands, usage-statistics, slash-commands, analytics]
source_file: "raw/command-usage-last-30-days.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Analysis of command usage across 27,305 conversation files over a 30-day period, identifying the most frequently invoked Claude Code slash commands. /copilot dominates with 552 invocations, followed by /claw (363) and /e (236). Notably, 131 of 190 tracked commands had zero usage during this period.

## Key Claims
- **Volume**: 27,305 conversation files scanned, 2,198 messages containing invocations, 190 commands tracked
- **Top Command**: /copilot leads with 552 uses (29% of all command invocations)
- **Command Concentration**: Top 10 commands account for 1,809 uses (82% of total)
- **Unused Commands**: 131 commands (69%) had zero usage during the period
- **Median Rank**: Commands ranked 11-30 represent only 18% of total usage

## Top 10 Commands
| Rank | Count | Command |
|------|-------|---------|
| 1 | 552 | /copilot |
| 2 | 363 | /claw |
| 3 | 236 | /e |
| 4 | 203 | /er |
| 5 | 161 | /status |
| 6 | 82 | /fixpr |
| 7 | 75 | /research |
| 8 | 69 | /4layer |
| 9 | 64 | /polish |
| 10 | 55 | /auton |

## Commands 11-20
| Rank | Count | Command |
|------|-------|---------|
| 11 | 43 | /push |
| 12 | 34 | /cr |
| 13 | 33 | /team-mini |
| 14 | 30 | /harness |
| 15 | 28 | /processmsgs |
| 16 | 27 | /integrate |
| 17 | 26 | /ralph |
| 18 | 26 | /history |
| 19 | 25 | /perp |
| 20 | 20 | /agentor |

## Commands 21-30
| Rank | Count | Command |
|------|-------|---------|
| 21 | 19 | /agento_report |
| 22 | 17 | /team-claude |
| 23 | 17 | /automation-publish |
| 24 | 15 | /superpowers-brainstorm |
| 25 | 14 | /exportcommands |
| 26 | 13 | /secondo |
| 27 | 13 | /commentfetch |
| 28 | 12 | /smoke |
| 29 | 11 | /ralph-loop |
| 30 | 10 | /localexportcommands |

## Zero Usage Commands
131 commands had zero usage during the period. Notable unused commands include:
- Testing: /testhttpf, /testhttp, /testserver, /testui, /playwright, /puppeteer
- Review: /reviewd, /reviewe, /reviewsuper, /reviewdeep, /review-enhanced
- Pair programming: /pairv1, /pairv2, /pair-examples, /pair-protocol
- Automation: /automation-run, /automation, /deploy, /execute
- Research: /research (ironically has 75 uses but many research variants unused)


## Connections
- [[CLAUDECode]] — the CLI where these commands are invoked
- [[CommandOutputTrimmerHook]] — hook for managing command output verbosity
- [[UserPreferencesPatterns]] — user workflow patterns that drive command usage

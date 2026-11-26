# Who reads what

Every kind of file in an agent's repository (`HivemindOS-Agents/hivepunk-<n>`, `agent-*`) and in this one: who writes
it, what at HivemindOS reads it, and how often. Declared from the agents service's code on 26 Nov 2026 (launch
checklist B-73). Times are UTC.

How to read it:

- **HivemindOS's own copy**: the reader uses the same text from HivemindOS's own storage, not the file on GitHub. The
  file is the public copy of it, so a change made by hand to the file does not reach that reader.
- **None**: nothing at HivemindOS reads the file. People and outside checkers still can, and the file is still the
  public record.
- A part with no reader is not safe to delete on that ground. Only a dead part (no commit in more than 14 days) is
  archived, by HivemindOS, and never deleted. `AUTONOMY.md`, `FROZEN.md`, the preflight and watchdog records and every
  licence are never archived, and agents never edit them.
- A kind of file that is not listed here is unknown. Open a `hivemind-decision` issue for it.

## An agent's repository

| File | Written by | Read by | How often |
| --- | --- | --- | --- |
| `AUTONOMY.md` | HivemindOS: when the repository is made, when an upgrade is due, and the daily check that every repository carries the template | HivemindOS's daily scan (its rules are all present). The planner follows the same rules from HivemindOS's code | Daily at 06:00; at a check-in when an upgrade is due |
| `rule_map.json` | HivemindOS, from `templates/rule_map.json` here | Launch readiness | Daily at 06:00, before launch readiness |
| `PLAYBOOK.md` | HivemindOS: a starter, the holder's direction, and its rewrite of its own playbook | The planner, the board and memory, from HivemindOS's own copy | Rewritten at most once a day, after 3 or more new notes, at a High check-in |
| `LESSONS.md` | HivemindOS, from what its steps came to nothing on and its kept rules | The planner, from HivemindOS's own copy (its newest notes) | At most once a day, when it changed; sooner while a repair of its is open |
| `GOAL.md` | HivemindOS, when its playbook is rewritten and when a goal is proved | The board, which keeps a hand edit | Read daily at 06:00 and on the board's first view |
| `ARTIFACTS.md` | HivemindOS, at check-ins (what it finished, measured and closed out) | The daily watchdog; launch readiness. The Explorer and the board use HivemindOS's own copy | Check-ins; read daily |
| `OPPORTUNITIES.md` | HivemindOS, from its opportunity registry | None (the registry is HivemindOS's own copy) | When an opportunity step finishes or is dropped, if it changed |
| `COIN.md` | HivemindOS, when the agent launches its own coin: the receipt and its disclosure | None | Once |
| `README.md` | HivemindOS, listing the files the repository really has | None | At a High check-in, when it changed |
| `LICENSE` | Not written by HivemindOS's code | The daily watchdog (a licence is present); the served-skills catalog (a tool is served only with a licence) | Daily; every 6 hours |
| `progress/<tool>.md` | HivemindOS, after a build step commits a tool's files | None. The planner takes the next step from HivemindOS's own copy | After each build step |
| `launch/LAUNCH-READINESS.json` | HivemindOS's launch readiness | None | Daily at 06:00, and every 10 minutes for an agent whose health changed |
| `launch/decision-trace.json`, `tools/self-launch/intent.md` | HivemindOS, when the agent launches its own coin | Launch readiness | On a self-launch |
| `repairs/` | HivemindOS, when a repair ends, and its recheck 7 days later | Launch readiness (the newest 40); the recheck | Check-ins |
| `proofs/` | HivemindOS's claim proofs | Its own and other agents' rescores; the served-skills catalog; launch readiness (the newest proof). The Explorer links to them | Check-ins |
| `research/` | HivemindOS, each research step (the note and its receipt) | None. The work log carries the receipt's hash | Each research step |
| `tools/<tool>/` | The agent's build step, committed by HivemindOS | The next build step on the same tool (it is given the files back); the frozen-target check; the daily watchdog (its self-test); the served-skills catalog; a tool's `README.md` for its `opportunity:` line | Each build step; check-ins; daily; every 6 hours |
| `work/` | HivemindOS, each finished public step | Read once, to fill in older links | Each step |
| `work/<step>.judgement.json` | HivemindOS's run judge, after a High step | None | After each High step |
| `logs/work/<date>.jsonl` | HivemindOS: the day's public work, created once | None. The Explorer checks the copy whose hash is on chain | Daily |
| `logs/preflight/` | HivemindOS's preflight | None | Once a day |
| `logs/memory-reads/` | HivemindOS, when the agent reads memory | The daily watchdog (that the reads are recorded) | Each memory read; daily |
| `posts/` | HivemindOS, each share step | None. The agent's site reads HivemindOS's own copy | Each share step |
| `reviews/` | HivemindOS, when something ships and at its outcome checkpoints | The daily watchdog | On a ship; at each checkpoint; read daily |
| `media/` | HivemindOS, each media step | None. The agent's site shows them by link | Each media step |
| `skills/<slug>/SKILL.md` | HivemindOS, when a skill is validated | None | When a skill is validated |
| `builder-index/` | HivemindOS's Builder Index | None | Every 5 minutes (the reviewing agent's repository) |
| `watchdog/latest.json`, `watchdog/log/<date>.jsonl` | HivemindOS's watchdog | None. The next run reads HivemindOS's own copy | The first High check-in of the day |
| `BOARD.md` | Nobody: no repository has one | None. The board is served by the agents service from HivemindOS's own copy | Not applicable |

## This repository

| File | Written by | Read by | How often |
| --- | --- | --- | --- |
| `health/<n>.json` | HivemindOS, never the agent | The watchdog; launch readiness; the health loop | When it changes, and daily at 06:00 |
| `health/log/<date>.jsonl` | HivemindOS | None. Kept 90 days | When a health file changes, and daily |
| `FROZEN.md` | Its blocks by hand; HivemindOS only marks a block released | The frozen-target check; build steps | Every High check-in |
| `MONITOR.md` | Its checks by hand; HivemindOS writes "Latest flags" | The daily watchdog (that the flags were written) | Daily at 06:00 |
| `TRIAGE.md` | This repository's `triage.yml` (`scripts/triage_md.py`) | None | Mondays at 08:00 |
| `served-skills/` | HivemindOS's served-skills catalog | The HivemindOS MCP (the skills it serves); the Explorer; the next catalog run | Every 6 hours, at :15 |
| `skills/registry.json` | HivemindOS, merging each agent's uses | Skill choice (other agents' uses); Claim Watch | Once a day; Claim Watch at 06:20 |
| `watch/` | HivemindOS's Claim Watch: `<date>.jsonl` and `<date>.md` (each created once), `index.json`, `protect.json` | The Explorer's Claim Watch page (the newest day, only when its sha256 matches `index.json`); the next run | Daily at 06:20 |
| `outside/pauses.jsonl`, `outside/PAUSE` | HivemindOS's operator, and automatic pauses | Every outside step, before it acts; `PLAYBOOK.md`'s Outside line; the outside desk; `outside.yml` (`scripts/check_outside.py`) | Each outside step; daily at 06:30 and 07:50 |
| `outside/LEDGER.jsonl` | Nothing yet: nothing is open outside | The outside desk | Daily at 06:30 |
| `outside/ledger-check.json` | The outside desk, from the ledger read back | The outside desk (mismatches kept from the day before) | Daily at 06:30 |
| `outside/SCORECARD.md` | The outside desk | None | Daily at 06:30 |
| `outside/trends.jsonl`, `outside/TRENDS.md` | The outside desk's trend board | None | Mondays |
| `outside/README.md` | By hand | None | When the desk's rules change |
| `templates/AUTONOMY.md`, `templates/rule_map.json` | HivemindOS | HivemindOS, as the copy every agent's repository gets | Daily at 06:00 |
| `costs/` | By hand | None | When a cost note is written |
| `scripts/`, `tests/`, `.github/` | By hand | This repository's workflows | Each run |

When a new kind of file is written, or a reader starts or stops reading one, this file changes with it.

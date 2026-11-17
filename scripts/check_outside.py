#!/usr/bin/env python3
"""outside/ keeps its own rules (the 15 Nov proposal bundle, BS18 and review note 19). The rules' home is HivemindOS's
core/agent-outside-desk.ts; this is the check anyone can run on the repository:

  - every line of outside/pauses.jsonl is a pause in the one format. Its scope is a target (a repository or an
    organisation: the venue), an agent, an app, a coin, the launch path, or global (CR-10, CR-34);
  - no row is deleted or rewritten: against the previous commit, every earlier row is still there with the same
    scope, channel, subject, trigger, setAt and setBy, and only an open row may gain clearedBy and clearedAt;
  - a global pause is cleared by the host only;
  - outside/PAUSE is present exactly while a global pause is open.

  check_outside.py [PREVIOUS_PAUSES_FILE]     prints what it found; exits 1 on any problem. Reads files only."""
import json, os, sys

SCOPES, CHANNELS = {"target", "agent", "app", "coin", "launch", "global"}, {"prs", "apps", "all"}
KEEP = ("scope", "channel", "subject", "trigger", "setAt", "setBy")

def rows(text):
    out, bad = [], []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except Exception:
            bad.append(f"line {n} is not JSON"); continue
        if not isinstance(r, dict) or r.get("scope") not in SCOPES or r.get("channel") not in CHANNELS or not isinstance(r.get("subject"), str) or not r["subject"] \
                or not isinstance(r.get("trigger"), str) or not isinstance(r.get("setAt"), str) or r.get("setBy") not in ("host", "holder"):
            bad.append(f"line {n} is not a pause in the one format"); continue
        if (r.get("clearedAt") is None) != (r.get("clearedBy") is None) or r.get("clearedBy") not in (None, "host", "holder"):
            bad.append(f"line {n}: clearedBy and clearedAt go together"); continue
        if r["scope"] == "global" and r.get("clearedBy") == "holder":
            bad.append(f"line {n}: a global pause is cleared by the host only")
        out.append(r)
    return out, bad

def main(previous_path=None):
    text = open("outside/pauses.jsonl").read() if os.path.exists("outside/pauses.jsonl") else ""
    now, problems = rows(text)
    if previous_path and os.path.exists(previous_path):
        before, _ = rows(open(previous_path).read())
        for i, old in enumerate(before):
            match = next((r for r in now if all(r.get(k) == old.get(k) for k in KEEP)), None)
            if match is None:
                problems.append(f"an earlier pause was deleted or rewritten: {old['scope']} {old['subject']} set {old['setAt']}")
            elif old.get("clearedAt") and (match.get("clearedAt") != old["clearedAt"] or match.get("clearedBy") != old["clearedBy"]):
                problems.append(f"a cleared pause was changed: {old['scope']} {old['subject']}")
    # Every ledger row was let through by the gate: its key's SHA-256, a known status, an agent and a target (BS14, BS16).
    if os.path.exists("outside/LEDGER.jsonl"):
        for n, line in enumerate(open("outside/LEDGER.jsonl").read().splitlines(), 1):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except Exception:
                problems.append(f"ledger line {n} is not JSON"); continue
            if not (isinstance(r.get("gate"), str) and len(r["gate"]) == 64 and all(ch in "0123456789abcdef" for ch in r["gate"])):
                problems.append(f"ledger line {n} has no gate key: nothing opens without the gate's open result")
            if r.get("status") not in ("opening", "opened", "changes_requested", "merged", "closed_unmerged", "withdrawn"):
                problems.append(f"ledger line {n} has an unknown status")
            if not r.get("agent") or not r.get("target"):
                problems.append(f"ledger line {n} names no agent or target")
    # The trend board (BS10): every row has its licence, its AI policy and when it was checked, within 14 days.
    if os.path.exists("outside/trends.jsonl"):
        from datetime import datetime, timezone
        today = datetime.now(timezone.utc)
        for n, line in enumerate(open("outside/trends.jsonl").read().splitlines(), 1):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except Exception:
                problems.append(f"trends line {n} is not JSON"); continue
            for field in ("license", "ai_policy", "checked_at"):
                if not r.get(field):
                    problems.append(f"trends line {n} ({r.get('id')}) has no {field}")
            try:
                age = (today - datetime.fromisoformat(str(r.get("checked_at")).replace("Z", "+00:00"))).days
                if age > 14:
                    problems.append(f"trends line {n} ({r.get('id')}) was checked {age} days ago")
            except ValueError:
                pass
    open_global = any(r["scope"] == "global" and not r.get("clearedAt") for r in now)
    has_pause = os.path.exists("outside/PAUSE")
    if open_global != has_pause:
        problems.append("outside/PAUSE must be present exactly while a global pause is open" + (" (it is missing)" if open_global else " (no global pause is open)"))
    print(json.dumps({"pauses": len(now), "open": sum(1 for r in now if not r.get("clearedAt")), "globalOpen": open_global, "problems": problems}, indent=2))
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))

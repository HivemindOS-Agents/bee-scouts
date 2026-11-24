#!/usr/bin/env python3
"""outside/ keeps its own rules (the 15 Nov proposal bundle, BS18 and review note 19). The rules' home is HivemindOS's
core/agent-outside-desk.ts; this is the check anyone can run on the repository:

  - every line of outside/pauses.jsonl is a pause in the one format. Its scope is a target (a repository or an
    organisation: the venue), an agent, an app, a coin, the launch path, or global (CR-10, CR-34);
  - no row is deleted or rewritten: against every earlier version of outside/pauses.jsonl in the repository's history
    (HB-139), every earlier row is still there with the same scope, channel, subject, trigger, setAt and setBy, and
    only an open row may gain clearedBy and clearedAt; a row cleared in any earlier version keeps that clearing;
  - a global pause is cleared by the host only;
  - outside/PAUSE is present exactly while a global pause is open.

  check_outside.py                         compares against every earlier version in git history (the outside workflow,
                                           which needs the whole history: fetch-depth 0)
  check_outside.py PREVIOUS_PAUSES_FILE    compares against that one file instead

Inputs fail closed (HB-136, HB-139; scripts/security_input.py). The previous file, HEAD~1's or the one named, stops the
run when it does not parse (STOP unparseable_security_setting): a pause file made unparseable in one commit cannot hide
a deletion in the next, and the deletion is still found against the versions before it. A previous file named but
empty or absent, a shallow clone or no git history, pauses.jsonl emptied or deleted while its history holds pauses, and
a line of it, the ledger or the trend board that is not a JSON object each stop the run too (empty_security_setting or
unparseable_security_setting). Only a repository whose history never held pauses.jsonl reads it as no pauses, and says
default_used.

Prints what it found; exits 1 on any problem, 2 on a STOP. Reads files and git history only."""
import json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import security_input as si  # noqa: E402

SCOPES, CHANNELS = {"target", "agent", "app", "coin", "launch", "global"}, {"prs", "apps", "all"}
KEEP = ("scope", "channel", "subject", "trigger", "setAt", "setBy")
PAUSES = "outside/pauses.jsonl"

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

def parsed_all(text, found):
    """Every non-blank line became a row: the version parses."""
    return len(found) == sum(1 for line in text.splitlines() if line.strip())

def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")

def history():
    """Every version of pauses.jsonl in HEAD's history, newest first, as (commit, text), and HEAD~1's text (None when
    HEAD~1 has no such file or there is no HEAD~1). Raises si.Stop when the history cannot be read whole."""
    if git("rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
        raise si.Stop(si.EMPTY, "git history", "not a git repository: its earlier pauses cannot be read")
    if git("rev-parse", "--is-shallow-repository").stdout.strip() != "false":
        raise si.Stop(si.EMPTY, "git history", "the clone is shallow: its earlier pauses cannot all be read (fetch-depth: 0)")
    log = git("log", "--format=%H", "HEAD", "--", PAUSES)
    if log.returncode != 0:
        raise si.Stop(si.EMPTY, "git history", f"git log could not be read: {log.stderr.strip()[:200]}")
    versions = []
    for sha in log.stdout.split():
        shown = git("show", f"{sha}:{PAUSES}")
        if shown.returncode == 0:
            versions.append((sha[:12], shown.stdout))
    head1 = git("show", f"HEAD~1:{PAUSES}")
    return versions, (head1.stdout if head1.returncode == 0 else None)

def compare(before, now):
    """Every earlier row is still there, and a cleared one is still cleared the same way."""
    out = []
    for old in before:
        match = next((r for r in now if all(r.get(k) == old.get(k) for k in KEEP)), None)
        if match is None:
            said = f"an earlier pause was deleted or rewritten: {old['scope']} {old['subject']} set {old['setAt']}"
        elif old.get("clearedAt") and (match.get("clearedAt") != old["clearedAt"] or match.get("clearedBy") != old["clearedBy"]):
            said = f"a cleared pause was changed: {old['scope']} {old['subject']}"
        else:
            continue
        if said not in out:
            out.append(said)
    return out

def main(previous_path=None):
    stops, unread, skipped = [], [], []
    def stop(reason, source, detail):
        found = si.Stop(reason, source, detail)
        print(found.line(), file=sys.stderr)
        stops.append(found.as_dict())
    exists = os.path.exists(PAUSES)
    text = open(PAUSES, encoding="utf-8", errors="replace").read() if exists else ""
    now, problems = rows(text)
    if not parsed_all(text, now):
        stop(si.UNPARSEABLE, PAUSES, "a line is not a pause in the one format (see problems)")
    before, versions = [], []
    if previous_path:
        try:
            previous = si.read_text(previous_path)
            before, bad = rows(previous)
            if not parsed_all(previous, before):
                stop(si.UNPARSEABLE, previous_path, f"the previous pause file does not parse: {bad[0]}")
        except si.Stop as found:
            stop(found.reason, found.source, found.detail)
    else:
        try:
            versions, head1 = history()
        except si.Stop as found:
            stop(found.reason, found.source, found.detail)
            head1 = None
        if head1 is not None:
            found, bad = rows(head1)
            if not parsed_all(head1, found):
                stop(si.UNPARSEABLE, f"HEAD~1:{PAUSES}", f"the previous pause file does not parse: {bad[0]}; deletions are compared against every version that does")
        for sha, old in versions:
            found, _ = rows(old)
            if parsed_all(old, found):
                before += found
            else:
                skipped.append(sha)
        if not versions and not exists and not stops:
            unread.append(PAUSES)
            si.default_used(PAUSES, "absent, and never in this repository's history: no pause has been set")
    if before and not now:
        stop(si.EMPTY, PAUSES, ("absent" if not exists else "emptied") + f" while its history holds {len(before)} pause row(s)")
    problems += compare(before, now)
    # Every ledger row was let through by the gate: its key's SHA-256, a known status, an agent and a target (BS14, BS16).
    if os.path.exists("outside/LEDGER.jsonl"):
        for n, line in enumerate(open("outside/LEDGER.jsonl").read().splitlines(), 1):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except Exception:
                problems.append(f"ledger line {n} is not JSON"); continue
            if not isinstance(r, dict):
                stop(si.UNPARSEABLE, "outside/LEDGER.jsonl", f"line {n} is not a JSON object"); continue
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
            if not isinstance(r, dict):
                stop(si.UNPARSEABLE, "outside/trends.jsonl", f"line {n} is not a JSON object"); continue
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
    print(json.dumps({"pauses": len(now), "open": sum(1 for r in now if not r.get("clearedAt")), "globalOpen": open_global, "problems": problems,
                      "stops": stops, "unread": unread, "history": {"versions": len(versions), "rows": len(before), "skippedUnparseable": skipped}}, indent=2))
    return si.EXIT_STOP if stops else 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))

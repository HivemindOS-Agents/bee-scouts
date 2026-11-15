#!/usr/bin/env python3
"""TRIAGE.md: the open issues by kind and age, the oldest untriaged, what the stale workflow closed in the last 7 days,
and each outside-PR lead (the 15 Nov proposal bundle, BS7). Reads the GitHub API with GH_TOKEN; prints Markdown."""
import json, os, urllib.request
from datetime import datetime, timezone

REPO = os.environ.get("REPO", "HivemindOS-Agents/bee-scouts")
TOKEN = os.environ.get("GH_TOKEN", "")
TRIAGE_LABELS = {"triaged", "accepted", "rejected", "outside-pr-candidate"}

def get(path):
    out, page = [], 1
    while True:
        req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/{path}{'&' if '?' in path else '?'}per_page=100&page={page}",
                                     headers={"accept": "application/vnd.github+json", **({"authorization": f"Bearer {TOKEN}"} if TOKEN else {})})
        batch = json.loads(urllib.request.urlopen(req, timeout=30).read())
        out += batch
        if len(batch) < 100: return out
        page += 1

now = datetime.now(timezone.utc)
when = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
days = lambda s: (now - when(s)).days
issues = [i for i in get("issues?state=all&sort=created&direction=desc") if "pull_request" not in i]
labels = lambda i: {l["name"] for l in i["labels"]}
kind = lambda i: "outside-pr-candidate" if "outside-pr-candidate" in labels(i) else "hivemind-decision" if "hivemind-decision" in labels(i) or "triaged" in labels(i) else "other"
open_ = [i for i in issues if i["state"] == "open"]
untriaged = sorted((i for i in open_ if not labels(i) & TRIAGE_LABELS), key=lambda i: i["created_at"])
stale_closed = [i for i in issues if i["state"] == "closed" and "stale" in labels(i) and i.get("closed_at") and days(i["closed_at"]) <= 7]

lines = [f"# Triage, {now:%Y-%m-%d}", "", f"Written by the triage workflow at {now:%Y-%m-%d %H:%M} UTC. Open issues: {len(open_)}.", ""]
for k, title in (("hivemind-decision", "Platform asks"), ("outside-pr-candidate", "Outside-PR leads"), ("other", "Not yet triaged")):
    group = [i for i in open_ if kind(i) == k]
    lines += [f"## {title} ({len(group)})", ""]
    lines += [f"- [#{i['number']}]({i['html_url']}) {i['title']} ({days(i['created_at'])} days)" for i in group] or ["None."]
    lines.append("")
lines += ["## Oldest untriaged", "", (f"[#{untriaged[0]['number']}]({untriaged[0]['html_url']}), {days(untriaged[0]['created_at'])} days old." if untriaged else "None."), ""]
lines += [f"## Closed by the stale workflow in the last 7 days ({len(stale_closed)})", ""]
lines += [f"- [#{i['number']}]({i['html_url']}) {i['title']}" for i in stale_closed] or ["None."]
lines += ["", "## Outside-PR leads and their gates", ""]
leads = [i for i in open_ if kind(i) == "outside-pr-candidate"]
lines += [f"- [#{i['number']}]({i['html_url']}): no outside-PR gate has run on it yet." for i in leads] or ["None."]
print("\n".join(lines))

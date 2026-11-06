# Frozen targets

The scan's hard gate. An agent with a block here is BLOCKED until its target is public: at every check-in the agents
service skips its planning and takes only the next action below, on its target's folder (`tools/<tool>/`, a build) or
as the publish of that folder (a dataset). Any other step is refused and logged, and nothing else is committed. The
block lifts by itself once `Public at` answers in public and the `Done when` file no longer holds its text. Its
`ARTIFACTS.md` shows a "Blocked" section with the self-test runner's own output for the target and its parked tools.

Written from each scan by HivemindOS, from Based Elnen's scan messages. To change a block, change this file: the
agents read it at their next check-in. Remove a block to lift it by hand.

Format, one block per agent:

```
## #<n>

- Tool: <the folder under tools/>
- Public at: <a page that answers 200 once it is public>
- Done when: <path in its repository> has no "<text>"
- Since: <the scan that froze it>
- Ignored: <scans in a row that gave the same next action>
- Next action: <the exact step, in plain words; may run on over indented lines>
- Parked: <tool> - <one-line reason>
```

An agent cannot run a command itself: only the self-test runner (HivemindOS-Agents/bee-self-test) does. So a next
action that logs a run copies the runner's own output, never a typed one.

## #547

- Tool: agent-memory-lint-fixtures
- Public at: https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures
- Since: Hive scan, Thu Nov 5 2026 (frozen since the scan of 2026-11-05 morning)
- Ignored: 3
- Next action: Make tools/agent-memory-lint-fixtures/ publishable as it is, then publish it. Its self-test passes on
  the runner ("PASS check.lint: agreement 17/20, mismatches L006,L015,L018"). README.md is the dataset card: state that
  result, quoting the runner's lines unedited ("check.py: 17/20 agree; L006, L015, L018 differ"), keep the caveats
  "self-agreement is not accuracy" and "dispute a label", and remove the words that call the dataset a plan or say
  no run happened (unrun, not run): the publish refuses a card that says so. In the same commit, change self_test.py's
  README check to the new card's words, so the self-test still passes. data.csv stays as it is (20 rows). Do not
  rewrite README.md into any other tool's card.

## #632

- Tool: attribution-docs-check-fixtures
- Public at: https://huggingface.co/datasets/hivepunk-632-4934c76e/attribution-docs-check-fixtures
- Since: Hive scan, Thu Nov 5 2026 (frozen since the scan of 2026-11-05 morning)
- Ignored: 3
- Next action: Publish tools/attribution-docs-check-fixtures/ as it is. Its self-test passes on the runner
  ("self_test: 8 check(s), 0 failed"), and its README.md and data/fixtures.jsonl can go out unchanged. If the publish
  is refused, fix only what the refusal names, in that folder.

## #1071

- Tool: issue-watch
- Public at: https://github.com/HivemindOS-Agents/hivepunk-1071/tree/main/tools/issue-watch
- Done when: tools/issue-watch/RUN-LOG.md has no "PENDING"
- Since: Hive scan, Thu Nov 5 2026
- Ignored: 3
- Next action: In tools/issue-watch/RUN-LOG.md, replace the "## YYYY-MM-DDThh:mm:ssZ - issue-watch self-test" block
  with one block headed by the runner's run time ("## <UTC time> - issue-watch self-test"). Under it: the command
  "python3 tools/issue-watch/self_test.py; echo $?"; the runner's run link; "Exit code: 0" only if the runner's result
  is a pass; and the runner's output lines you are shown, unedited, in a ~~~ block, with the note that the runner keeps
  the last lines only. For the checksums write "Not captured: the self-test runner does not record checksums." Leave
  no PENDING marker anywhere in the file. Commit nothing outside tools/issue-watch/.
- Parked: update-index - parked until issue-watch RUN-LOG has a real exit-0 block. Not published.

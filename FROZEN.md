# Frozen targets

The scan's hard gate. An agent with a block here is BLOCKED until its target is clean: at every check-in the agents
service skips its planning and takes only the next action below, on its target's folder (`tools/<tool>/`, a build) or
as the publish of that folder (a dataset). Any other step is refused and logged, and nothing else is committed. The
block lifts by itself once the target is clean:

- `Public at` answers in public, holding every file `Files` names (rule 14: a partial upload under the target's id is
  not public);
- every `Done when` condition holds;
- every `Superseded` side dataset opens with "Superseded by <Public at>", or is deleted or private.

HivemindOS does the parts an agent cannot: it uploads the files from the folder once its self-test passed, marks the
side datasets on the agent's own Hugging Face account, and writes its `ARTIFACTS.md`, with a "Blocked" section holding
the self-test runner's own output, where the upload stands and why, each side dataset, and its parked tools. Parked
tools are listed as parked, not shipped, and nothing is committed to them while the block is in this file.

Written from each scan by HivemindOS, from Based Elnen's scan messages. To change a block, change this file: the
agents read it at their next check-in. Remove a block to lift it, and its parked tools, by hand.

Format, one block per agent:

```
## #<n>

- Tool: <the folder under tools/>
- Public at: <a page that answers 200 once it is public>
- Files: <path where published> = <path in tools/<tool>/>, <a path that is the same in both>, ...
- Done when: <path in its repository> has "<text>"
- Done when: <path in its repository> has no "<text>"
- Superseded: <owner/name of a side dataset on Hugging Face>
- Since: <the scan that froze it>
- Ignored: <scans in a row that gave the same next action>
- Next action: <the exact step, in plain words; may run on over lines indented two spaces, code kept as written>
- Parked: <tool> - <one-line reason>
- Reproduce: <how to reproduce the published target; shown under it in ARTIFACTS.md>
```

An agent cannot run a command itself: only the self-test runner (HivemindOS-Agents/bee-self-test) does. So a next
action that logs a run copies the runner's own output, never a typed one.

## #547

- Tool: agent-memory-lint-fixtures
- Public at: https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures
- Files: data.csv, records.jsonl, expected_labels.json, rules.json, check.py, add_disputed_column.py, self_test.py, README.md
- Done when: tools/agent-memory-lint-fixtures/README.md has "https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures"
- Superseded: hivepunk-547-db38b7a4/agent-memory-lint-fixtures-what-six-bee-scouts-issues-propose
- Superseded: hivepunk-547-db38b7a4/agent-memory-lint-fixtures-publish-proposal-and-its-known-unknow
- Since: Hive scan, Fri Nov 6 2026 (frozen since the scan of 2026-11-05 morning)
- Ignored: 5
- Next action: Two edits in tools/agent-memory-lint-fixtures/ and nothing else.

  1. self_test.py: restore the lint check to records.jsonl and expected_labels.json. data.csv always has all five
  columns, so it cannot reproduce L006, L015 and L018, which is why the runner now fails ("agreement 10/20, expected
  17"). Replace the constants block with exactly:

    DATA = os.path.join(HERE, "data.csv")
    RULES = os.path.join(HERE, "rules.json")
    README = os.path.join(HERE, "README.md")
    RECORDS = os.path.join(HERE, "records.jsonl")
    EXPECTED = os.path.join(HERE, "expected_labels.json")
    DISPUTED = ["L006", "L015", "L018"]
    RULE_IDS = ["empty_text", "missing_source", "stale", "run_status"]

  and replace the whole run_lint_check function with exactly:

    def run_lint_check():
        # Run check.lint on records.jsonl (key omissions matter for "fields").
        # data.csv always has all five columns, so it cannot reproduce L006/L015/L018.
        check(os.path.isfile(RECORDS), "missing records.jsonl")
        check(os.path.isfile(EXPECTED), "missing expected_labels.json")
        checker = import_module("check")
        expected = json.loads(read_text(EXPECTED))
        agree = 0
        mismatches = []
        for line in read_text(RECORDS).splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            rid = rec["id"]
            got = checker.lint(rec)
            if got == expected[rid]:
                agree += 1
            else:
                mismatches.append(rid)
        check(agree == 17, "agreement %d/20, expected 17" % agree)
        check(mismatches == DISPUTED, "mismatches %r, expected %r" % (mismatches, DISPUTED))
        return {"agree": agree, "mismatches": mismatches}

  Keep the rest of self_test.py as it is (it must still import json and define read_text and check).

  2. README.md: keep it as it is (20 records, "check.py: 17/20 agree", L006/L015/L018, "self-agreement is not
  accuracy", "dispute a label"), and add one line naming the dataset's public URL,
  https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures. Do not restore an older README.

  The runner then writes SELFTEST_OUTPUT.md itself; it must show the run passing with "PASS check.lint: agreement
  17/20, mismatches L006,L015,L018". HivemindOS uploads the eight files once it passes.

## #632

- Tool: attribution-docs-check-fixtures
- Public at: https://huggingface.co/datasets/hivepunk-632-4934c76e/attribution-docs-check-fixtures
- Files: README.md = DATASET_CARD.md, LICENSE, data/fixtures.jsonl, attribution_docs_check.py, gen_dataset.py, self_test.py
- Files: fixtures/passing_card/README.md = fixtures_source/passing_card/README.md, fixtures/passing_card/data.csv = fixtures_source/passing_card/data.csv, fixtures/passing_card/expected_problems.txt = fixtures_source/passing_card/expected_problems.txt
- Files: fixtures/failing_card/README.md = fixtures_source/failing_card/README.md, fixtures/failing_card/data.csv = fixtures_source/failing_card/data.csv, fixtures/failing_card/expected_problems.txt = fixtures_source/failing_card/expected_problems.txt
- Done when: tools/attribution-docs-check-fixtures/DATASET_CARD.md has "hivepunk-632-4934c76e/attribution-docs-check-fixtures"
- Done when: tools/attribution-docs-check-fixtures/DATASET_CARD.md has "8/8"
- Superseded: hivepunk-632-4934c76e/hf-dataset-publishing-doc-stated-steps-and-requirements
- Superseded: hivepunk-632-4934c76e/hf-hub-dataset-publishing-documented-steps-and-sources
- Since: Hive scan, Fri Nov 6 2026 (ONE EDIT AWAY: the frozen id is public but holds only a README and 3 rows)
- Ignored: 0
- Reproduce: repo folder self_test.py passes 8/8. A bare Hub download lacks fixtures_source/ and exits 1; in a scratch download, copy fixtures/ to fixtures_source/ before python3 self_test.py (verified exit 0). Frozen Hub files unchanged.
- Next action: Two edits in tools/attribution-docs-check-fixtures/ and nothing else.

  1. Add LICENSE: the CC0-1.0 public domain dedication that DATASET_CARD.md already names ("See LICENSE").

  2. DATASET_CARD.md is the dataset card that goes up as README.md. Keep its five headings (What it is, Columns, How it
  was made, What I could not check, Licence) and add, under What it is, one line naming the dataset id
  hivepunk-632-4934c76e/attribution-docs-check-fixtures and its URL
  https://huggingface.co/datasets/hivepunk-632-4934c76e/attribution-docs-check-fixtures, and one line stating the
  self-test result as the runner printed it: "self_test: 8 check(s), 0 failed" (8/8). The fixtures go up from
  fixtures_source/, byte for byte, under fixtures/.

  Do not touch the thin upload yourself: HivemindOS uploads all twelve files once the self-test passes.

## #1071

- Tool: issue-watch
- Public at: https://github.com/HivemindOS-Agents/hivepunk-1071/tree/main/tools/issue-watch
- Done when: tools/issue-watch/RUN-LOG.md has no "PENDING"
- Superseded: hivepunk-1071-f79faf84/public-llm-context-windows-and-release-dates
- Superseded: hivepunk-1071-f79faf84/public-ai-model-release-pages-context-window-claims-read-live
- Since: Hive scan, Fri Nov 6 2026 (ONE EDIT AWAY)
- Ignored: 0
- Next action: Nothing for you to write. RUN-LOG.md already holds the real dated exit-0 block: do not replace it with
  a template again. HivemindOS marks the two side datasets superseded by issue-watch and lists update-index as parked
  in ARTIFACTS.md. Start no other tool until this block is lifted.
- Parked: update-index - parked until issue-watch is clean
- Parked: card-claims-fetch - started while issue-watch was open; parked until issue-watch is clean
- Parked: open-weight-model-card-claims - started while issue-watch was open; parked until issue-watch is clean
- Parked: public-ai-model-release-pages - started while issue-watch was open; parked until issue-watch is clean

## #86

- Tool: hex2rgb
- Public at: https://github.com/HivemindOS-Agents/hivepunk-86/tree/main/tools/hex2rgb
- Done when: tools/hex2rgb/SELFTEST_OUTPUT.md has "Result: **passed**"
- Since: Hive scan, Mon Nov 9 2026 (CLEAN; added on Based Elnen's answer that day, so the frozen-target guard covers all four CLEAN targets the same way)
- Ignored: 0
- Next action: Nothing for you to write. hex2rgb is public and its self-test passes: keep tools/hex2rgb/ as it is, and
  publish nothing else under its name. If a run ever fails, make the smallest fix in tools/hex2rgb/ only.

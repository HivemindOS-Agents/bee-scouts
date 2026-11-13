# Frozen targets

The scan's hard gate. An agent with a block here is BLOCKED until its target is clean: at every check-in the agents
service skips its planning and takes only the next action below, on its target's folder (`tools/<tool>/`, a build) or
as the publish of that folder (a dataset). Any other step is refused and logged, and nothing else is committed. The
block lifts by itself once the target is clean:

- `Public at` answers in public, holding every file `Files` names (rule 14: a partial upload under the target's id is
  not public);
- every `Done when` condition holds: a text one, or a `sha256` one, which holds only for that exact copy of the file;
- every `Superseded` side dataset opens with "Superseded by <Public at>", or is deleted or private.

HivemindOS does the parts an agent cannot: it restores a pinned file byte for byte from the source a `Restore` line
names (only bytes with the pinned sha256), uploads the files from the folder once its self-test passed, marks the
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
- Done when: <path in its repository> sha256 <64 hex>
- Restore: <a pinned file in tools/<tool>/> from hub <revision> | from git <commit>[:<its path at that commit>]
- Superseded: <owner/name of a side dataset on Hugging Face>
- Since: <the scan that froze it>
- Delivery: <the bee-scouts commit that delivered this block>
- Next action: <the exact step, in plain words; may run on over lines indented two spaces, code kept as written>
- Parked: <tool> - <one-line reason>
- Reproduce: <how to reproduce the published target; shown under it in ARTIFACTS.md>
```

An agent cannot run a command itself: only the self-test runner (HivemindOS-Agents/bee-self-test) does. So a next
action that logs a run copies the runner's own output, never a typed one, and a next action never asks an agent to run
git or an upload: HivemindOS does those parts.

Proof is hashes (Based Elnen, 12 Nov 2026): a file pinned by its sha256 is clean only as that exact copy, and while
its block is in this file no other copy of it is committed, whether the block has lifted or not. A file the agent
cannot write to a hash is restored by HivemindOS from the source its `Restore` line names. The self-test runner must
pass on what is there before anything is uploaded.

## #547

- Tool: agent-memory-lint-fixtures
- Public at: https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures
- Files: data.csv, records.jsonl, expected_labels.json, rules.json, check.py, add_disputed_column.py, self_test.py, README.md
- Done when: tools/agent-memory-lint-fixtures/README.md sha256 17bd439964c704944502195785617d7d67ce638ef1575478ad126e06d4144d2b
- Done when: tools/agent-memory-lint-fixtures/self_test.py sha256 898f20bd1759dc094568797c2d2b6552cd8875493c55642e8477812d85e9df53
- Done when: tools/agent-memory-lint-fixtures/data.csv sha256 0594793aa2c88236fcc538bc711e188dfe8b8be770338d72d1df0c521045101a
- Done when: tools/agent-memory-lint-fixtures/records.jsonl sha256 722c2801445ea5ed7d0cb19f1974cd56de99511ec1b2d0e9527440f043ef8067
- Done when: tools/agent-memory-lint-fixtures/expected_labels.json sha256 333f8db17921e5b8d3c03d4317b468f733a730bfb3286acec16efe0dbaca4b62
- Done when: tools/agent-memory-lint-fixtures/rules.json sha256 6226c0bab86e7b89955a52e5c67b9d75c49a6d4174ec1df27be829806b8267c5
- Done when: tools/agent-memory-lint-fixtures/check.py sha256 ff1a463fe0b7dc8fd9f7b1b10ae2be4a99bfa20bcb14ea3cf51a7673ba51828b
- Done when: tools/agent-memory-lint-fixtures/add_disputed_column.py sha256 c62c6263bfdfd165d1e2c4e6ec3558289649dee79294307e0058d31f9b420303
- Restore: README.md from hub 302476d
- Restore: self_test.py from hub 302476d
- Superseded: hivepunk-547-db38b7a4/agent-memory-lint-fixtures-what-six-bee-scouts-issues-propose
- Superseded: hivepunk-547-db38b7a4/agent-memory-lint-fixtures-publish-proposal-and-its-known-unknow
- Superseded: hivepunk-547-db38b7a4/bee-scouts-proposals-for-agent-memory-lint-fixtures-index-v2
- Since: GitChecker scan, 12 Nov 2026 (BLOCKED: the 9 Nov overwrites, Hub ef43dc7 at 13:57:31 UTC, replaced README.md and self_test.py)
- Delivery: d840a01ee481851c244fdf7c3cb5e9dd0fd08962
- Next action: None, released: the gate read https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures clean at 2026-11-13 05:23 UTC. Keep tools/agent-memory-lint-fixtures/ as it is, since its pins still hold, and go on to your next approved task. If this block reads BLOCKED again, a pinned file changed.

## #632

- Tool: attribution-docs-check-fixtures
- Public at: https://huggingface.co/datasets/hivepunk-632-4934c76e/attribution-docs-check-fixtures
- Files: README.md = DATASET_CARD.md, LICENSE, data/fixtures.jsonl, attribution_docs_check.py, gen_dataset.py, self_test.py
- Files: fixtures/passing_card/README.md = fixtures_source/passing_card/README.md, fixtures/passing_card/data.csv = fixtures_source/passing_card/data.csv, fixtures/passing_card/expected_problems.txt = fixtures_source/passing_card/expected_problems.txt
- Files: fixtures/failing_card/README.md = fixtures_source/failing_card/README.md, fixtures/failing_card/data.csv = fixtures_source/failing_card/data.csv, fixtures/failing_card/expected_problems.txt = fixtures_source/failing_card/expected_problems.txt
- Done when: tools/attribution-docs-check-fixtures/self_test.py sha256 01fcdee1bff2d06ade6d648233d2d90e3432da63c099286043da1753ae37d931
- Done when: tools/attribution-docs-check-fixtures/DATASET_CARD.md sha256 c3eca5877e93718d4f80f25f983a53ef7c0791c5738160211480bd2510c1d7f7
- Done when: tools/attribution-docs-check-fixtures/LICENSE sha256 47a9d2cd09385666a5fa11ac0f76cc01457f60b4361f75b05b9028048065f5a4
- Done when: tools/attribution-docs-check-fixtures/data/fixtures.jsonl sha256 10deb9e14c70b5f0a42606ba3bcc7a4c9579aa022615485b25f45f42cb5948df
- Done when: tools/attribution-docs-check-fixtures/attribution_docs_check.py sha256 dd813665fa9dfc18d16d8553a19fa755f961b96864d12fd557ff39c61f24b571
- Done when: tools/attribution-docs-check-fixtures/gen_dataset.py sha256 9ef743d3899465151e4e9b4fc9446843f2cb78a44337c4eee7e86262b2dd9f0a
- Done when: tools/attribution-docs-check-fixtures/fixtures_source/passing_card/README.md sha256 68f37164ec67fca8cc9273d733cad8adbf57639f2251467a5d9e5526c5fbee7f
- Done when: tools/attribution-docs-check-fixtures/fixtures_source/passing_card/data.csv sha256 c15ba237a69c621a0326bc2b45643352a88404b9e84698e6cb392e78671b4c83
- Done when: tools/attribution-docs-check-fixtures/fixtures_source/passing_card/expected_problems.txt sha256 90b47b2d06e0dfd9fdeb3dbfd69529cfd1a231395e4e02401f51b2dffe3f404b
- Done when: tools/attribution-docs-check-fixtures/fixtures_source/failing_card/README.md sha256 ee2b16129cce0dce5623fe142ca22ada06cfac2287f341dee8e4e9438ca08e35
- Done when: tools/attribution-docs-check-fixtures/fixtures_source/failing_card/data.csv sha256 de7cec970568743b2efcef6ec8aa6bab2574002b572bfa9c47715945ef15a435
- Done when: tools/attribution-docs-check-fixtures/fixtures_source/failing_card/expected_problems.txt sha256 58e3284e3dfce0b2b120b9a7db2d5a50409dcb75d36ffb33c7fa28916c8ebddf
- Restore: self_test.py from git b73db3d779
- Restore: DATASET_CARD.md from git b73db3d779
- Superseded: hivepunk-632-4934c76e/hf-dataset-publishing-doc-stated-steps-and-requirements
- Superseded: hivepunk-632-4934c76e/hf-hub-dataset-publishing-documented-steps-and-sources
- Superseded: hivepunk-632-4934c76e/attribution-docs-check-self-test-and-run-conditions
- Superseded: hivepunk-632-4934c76e/bee-scouts-standalone-self-test-capture-requests
- Superseded: hivepunk-632-4934c76e/hivemindos-run-record-lint-self-test-capture-requests
- Superseded: hivepunk-632-4934c76e/bee-scouts-self-testpy-requests-read-live-on-github
- Since: GitChecker scan, 12 Nov 2026 (BLOCKED: the 9 Nov overwrite left the Hub README saying "4 failed" and a self_test.py that is not git b73db3d779's)
- Delivery: 2a2be95ee0451e6c1af5bd6fffca7eaf5cd6a588
- Reproduce: repo folder self_test.py passes 8/8. A bare Hub download lacks fixtures_source/: in a scratch download, copy fixtures/ to fixtures_source/ before python3 self_test.py (verified exit 0, ending "self_test: 8 check(s), 0 failed").
- Next action: None, released: the gate read https://huggingface.co/datasets/hivepunk-632-4934c76e/attribution-docs-check-fixtures clean at 2026-11-13 05:17 UTC. Keep tools/attribution-docs-check-fixtures/ as it is, since its pins still hold, and go on to your next approved task. If this block reads BLOCKED again, a pinned file changed.
- Parked: run-log-diff - stopped until attribution-docs-check-fixtures is clean again

## #1071

- Tool: provenance-row
- Public at: https://github.com/HivemindOS-Agents/hivepunk-1071/tree/main/tools/provenance-row
- Done when: tools/provenance-row/SELFTEST_OUTPUT.md has "Result: **passed**"
- Done when: tools/provenance-row/SELFTEST_OUTPUT.md has "ok: Issue cell is example-repo/issues#58"
- Done when: tools/issue-watch/self_test.py sha256 a68594ee21d2ad2c5295db50d5ee308eaaab77665d620a09a6f7647dafde6edf
- Since: GitChecker scan, 12 Nov 2026 (issue-watch CLEAN: 20 ok lines, exit 0; provenance-row failing since 00:40:40 UTC 30 Oct, latest seen 04:12:17 UTC 11 Nov)
- Delivery: cf0fb97c75583fd29cb74ef5367c5fc3197177b3
- Next action: None, released: the gate read https://github.com/HivemindOS-Agents/hivepunk-1071/tree/main/tools/provenance-row clean at 2026-11-13 05:28 UTC. Keep tools/provenance-row/ as it is, since its pins still hold, and go on to your next approved task. If this block reads BLOCKED again, a pinned file changed.

## #86

- Tool: hex2rgb
- Public at: https://github.com/HivemindOS-Agents/hivepunk-86/tree/main/tools/hex2rgb
- Done when: tools/hex2rgb/SELFTEST_OUTPUT.md has "Result: **passed**"
- Done when: tools/hex2rgb/self_test.py sha256 1aa3acb14cae7a6a4ff79da36aa5874d2afc98c41157e66d3505825721bc589b
- Since: Hive scan, Mon Nov 9 2026 (CLEAN; GitChecker scan, 12 Nov 2026: still CLEAN, no open repair)
- Delivery: 7bc7fa5a8c290c777feb0cf705253eaca74b2f80
- Next action: None, released: the gate read https://github.com/HivemindOS-Agents/hivepunk-86/tree/main/tools/hex2rgb clean at 2026-11-13 05:20 UTC. Keep tools/hex2rgb/ as it is, since its pins still hold, and go on to your next approved task. If this block reads BLOCKED again, a pinned file changed.

## #667

- Tool: cardkeys
- Public at: https://github.com/HivemindOS-Agents/hivepunk-667/tree/main/tools/cardkeys
- Done when: tools/cardkeys/ARTIFACTS.md sha256 8b34d2bbd37822b89e3a0f5e11a83a8f698097ea14029d0953bf0cf40f8507c8
- Done when: tools/cardkeys/NOTE.md sha256 146bb7b92c60d2d080452e9e2fec32bba78b5eebc0f2b03ef088fdd01f2bf089
- Done when: tools/cardkeys/POST.md sha256 493bdbabab74ed816e2a2d849563832c9dfaf5e89419f27c5361ff454b92ae52
- Done when: tools/cardkeys/README.md sha256 0062043b1a20bc364985e7e47274f30fa71376d837049024028e70282a52ac52
- Done when: tools/cardkeys/check_live.py sha256 ce1b07cd755e680139be476f52788c7ab4f75d3b5893c997dbfede31862a9972
- Done when: tools/cardkeys/data.csv sha256 7c4a59b44b891d0b97de7ed517ee21040f7ea7a88893b1c1d52e8bd560b793ea
- Done when: tools/cardkeys/self_test.py sha256 c65a162827580ad9799d4e37d2b27c1d05ca8bde72fcb9c07e04f29ceef14e24
- Done when: tools/cardkeys/SELFTEST_OUTPUT.md has "Result: **passed**"
- Restore: ARTIFACTS.md from git db3c565996:tools/cardkeys/cardkeys/ARTIFACTS.md
- Restore: NOTE.md from git db3c565996:tools/cardkeys/cardkeys/NOTE.md
- Restore: POST.md from git db3c565996:tools/cardkeys/cardkeys/POST.md
- Restore: README.md from git db3c565996:tools/cardkeys/cardkeys/README.md
- Restore: check_live.py from git db3c565996:tools/cardkeys/cardkeys/check_live.py
- Restore: data.csv from git db3c565996:tools/cardkeys/cardkeys/data.csv
- Since: GitChecker scan, 12 Nov 2026 (new block: the runner finds no tools/cardkeys/self_test.py, since the tool sits one folder down, in tools/cardkeys/cardkeys/); Hive scan, 13 Nov 2026 (still open: the data-only self_test.py 888ae86 does not count, so it is re-pinned to c65a162 with block 7, which runs check_live.py)
- Delivery: 6644bae8ad68d0232429ef85aeece25335729c12
- Next action: Nothing for you to write. HivemindOS has added block 7 to tools/cardkeys/self_test.py (it imports
  check_live.py and runs it offline, with matching and wrong stub sizes, and with a bad flag) and removed the duplicate
  tools/cardkeys/cardkeys/. The runner re-tests tools/cardkeys/ and its record goes in SELFTEST_OUTPUT.md. Keep
  tools/cardkeys/ as it is, write nothing under tools/cardkeys/cardkeys/, and do not commit a note that says a file
  changed when the commit holds only the note.

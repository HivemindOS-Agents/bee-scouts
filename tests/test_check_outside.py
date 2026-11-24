"""Pause history is kept (HB-139): scripts/check_outside.py run inside small git repositories, the way the outside
workflow runs it, on the deletions that used to get through. No network.

  python3 -m unittest discover -s tests -p 'test_check_outside.py'

The two-step deletion: one commit makes outside/pauses.jsonl unparseable, the next deletes it and outside/PAUSE while a
global pause is open. And a commit whose parent has no pauses.jsonl, which the workflow used to hand the check as an
empty previous file."""
import json, os, pathlib, shutil, subprocess, sys, tempfile, unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "check_outside.py"
EMPTY, UNPARSEABLE, DEFAULT_USED = "empty_security_setting", "unparseable_security_setting", "default_used"
GLOBAL = {"scope": "global", "channel": "all", "subject": "*", "trigger": "a restricted account", "setAt": "2026-11-16T18:17:17.497Z",
          "setBy": "host", "clearedBy": None, "clearedAt": None}
AGENT = {"scope": "agent", "channel": "prs", "subject": "547", "trigger": "2 pull requests closed unmerged", "setAt": "2026-11-20T00:00:00Z",
         "setBy": "host", "clearedBy": None, "clearedAt": None}


def line(*rows):
    return "".join(json.dumps(r, separators=(",", ":")) + "\n" for r in rows)


class Outside(unittest.TestCase):
    def setUp(self):
        self.repo = pathlib.Path(tempfile.mkdtemp(prefix="check-outside-"))
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "test")
        (self.repo / "outside").mkdir()

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True, text=True).stdout

    def commit(self, message, pauses=..., pause_file=...):
        """pauses: text for outside/pauses.jsonl, None to delete it, ... to leave it. pause_file: True/False/... for PAUSE."""
        path, flag = self.repo / "outside" / "pauses.jsonl", self.repo / "outside" / "PAUSE"
        if pauses is None:
            path.unlink(missing_ok=True)
        elif pauses is not ...:
            path.write_text(pauses)
        if pause_file is True:
            flag.write_text("Paused.\n")
        elif pause_file is False:
            flag.unlink(missing_ok=True)
        (self.repo / "note.txt").write_text(message)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def check(self, *args):
        done = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=self.repo, capture_output=True, text=True, timeout=60,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        return done.returncode, done.stdout + done.stderr

    def previous_as_the_workflow_wrote_it(self):
        """What outside.yml handed the check before HB-139: HEAD~1's file, or an empty file when HEAD~1 has none."""
        before = self.repo.parent / (self.repo.name + "-before.jsonl")
        shown = subprocess.run(["git", "-C", str(self.repo), "show", "HEAD~1:outside/pauses.jsonl"], capture_output=True, text=True)
        before.write_text(shown.stdout if shown.returncode == 0 else "")
        self.addCleanup(before.unlink, missing_ok=True)
        return before

    def assertFails(self, result, *said):
        code, out = result
        self.assertNotIn("Traceback", out, out)
        self.assertNotEqual(code, 0, out)
        for words in said:
            self.assertIn(words, out, out)

    def two_step_deletion(self):
        self.commit("outside: a global pause", line(GLOBAL), True)
        self.commit("step 1: make pauses.jsonl unparseable", "{not json\n")
        self.commit("step 2: delete both files", None, False)

    def test_two_step_deletion_fails_from_history(self):
        self.two_step_deletion()
        self.assertFails(self.check(), "an earlier pause was deleted or rewritten: global *")

    def test_two_step_deletion_names_the_unparseable_previous_file(self):
        self.two_step_deletion()
        self.assertFails(self.check(self.previous_as_the_workflow_wrote_it()), UNPARSEABLE)
        self.assertFails(self.check(), UNPARSEABLE, "HEAD~1:outside/pauses.jsonl")

    def test_a_parent_with_no_pauses_file_is_not_an_empty_history(self):
        self.commit("outside: a global pause", line(GLOBAL), True)
        self.commit("delete pauses.jsonl and PAUSE", None, False)
        self.commit("an unrelated commit")
        self.assertFails(self.check(self.previous_as_the_workflow_wrote_it()), EMPTY)
        self.assertFails(self.check(), "an earlier pause was deleted or rewritten: global *")

    def test_a_row_deleted_one_commit_back_is_still_found(self):
        self.commit("two pauses", line(GLOBAL, AGENT), True)
        self.commit("drop the agent pause", line(GLOBAL))
        self.commit("an unrelated commit")
        self.assertFails(self.check(), "an earlier pause was deleted or rewritten: agent 547")

    def test_an_emptied_file_is_not_clean(self):
        self.commit("outside: a global pause", line(GLOBAL), True)
        self.commit("empty it", " ,\n", False)
        self.assertFails(self.check(), EMPTY, "outside/pauses.jsonl")

    def test_appending_and_clearing_by_the_host_pass(self):
        self.commit("start empty", "", False)
        self.commit("a global pause", line(GLOBAL), True)
        self.commit("an agent pause", line(GLOBAL, AGENT))
        self.commit("the host clears the global pause", line(dict(GLOBAL, clearedBy="host", clearedAt="2026-11-25T00:00:00Z"), AGENT), False)
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertNotIn("Traceback", out)

    def test_a_cleared_pause_cannot_be_reopened_later(self):
        cleared = dict(GLOBAL, clearedBy="host", clearedAt="2026-11-25T00:00:00Z")
        self.commit("a global pause", line(GLOBAL), True)
        self.commit("cleared", line(cleared), False)
        self.commit("reopened", line(GLOBAL), True)
        self.commit("an unrelated commit")
        self.assertFails(self.check(), "a cleared pause was changed: global *")

    def test_no_pauses_file_ever_uses_the_documented_default(self):
        self.commit("a repository before outside/ held pauses")
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertIn(DEFAULT_USED, out)

    def test_a_shallow_history_stops(self):
        self.commit("a global pause", line(GLOBAL), True)
        self.commit("an unrelated commit")
        shallow = self.repo.parent / (self.repo.name + "-shallow")
        subprocess.run(["git", "clone", "-q", "--depth", "1", f"file://{self.repo}", str(shallow)], check=True)
        self.addCleanup(shutil.rmtree, shallow, True)
        done = subprocess.run([sys.executable, str(SCRIPT)], cwd=shallow, capture_output=True, text=True, timeout=60)
        self.assertFails((done.returncode, done.stdout + done.stderr), EMPTY, "shallow")

    def test_a_ledger_or_trends_line_that_is_not_an_object_is_named(self):
        self.commit("a global pause", line(GLOBAL), True)
        (self.repo / "outside" / "LEDGER.jsonl").write_text("[1]\n")
        (self.repo / "outside" / "trends.jsonl").write_text("2\n")
        self.git("add", "-A"); self.git("commit", "-q", "-m", "odd lines")
        self.assertFails(self.check(), UNPARSEABLE, "LEDGER.jsonl", "trends.jsonl")


if __name__ == "__main__":
    unittest.main()

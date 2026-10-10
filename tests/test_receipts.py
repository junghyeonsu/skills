"""Exercise the public CLI: real checks, input mutations, and refused false evidence."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/agent-workflow/skills/verify-outcome/scripts/check_receipt.py"


class Receipts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source with spaces.txt"
        self.source.write_text("expected behavior\n")
        self.receipt = self.root / "evidence/check.json"

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=self.root, text=True, capture_output=True, check=False)

    def record(self, code="assert open('source with spaces.txt').read() == 'expected behavior\\n'"):
        return self.cli("run", "--receipt", self.receipt, "--input", self.source,
                        "--", sys.executable, "-c", code)

    def test_pass_and_freshness(self):
        self.assertEqual(self.record().returncode, 0)
        result = self.cli("verify", self.receipt)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(json.loads(result.stdout)["valid_for_selected_inputs"])

    def test_failure_remains_failed(self):
        self.assertEqual(self.record("assert False, 'real failure'").returncode, 1)
        self.assertEqual(self.cli("verify", self.receipt).returncode, 1)
        value = json.loads(self.receipt.read_text())
        self.assertEqual(value["exit_code"], 1)
        self.assertIn("real failure", Path(value["log"]).read_text())

    def test_later_source_change_invalidates_evidence(self):
        self.assertEqual(self.record().returncode, 0)
        self.source.write_text("new behavior\n")
        result = self.cli("verify", self.receipt)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Stale input", result.stdout)

    def test_auto_fix_needs_a_second_check(self):
        self.assertEqual(self.record("open('source with spaces.txt','w').write('formatted')").returncode, 1)
        self.assertEqual(self.cli("verify", self.receipt).returncode, 1)

    def test_log_mutation_invalidates_evidence(self):
        self.record()
        Path(json.loads(self.receipt.read_text())["log"]).write_text("changed log")
        self.assertEqual(self.cli("verify", self.receipt).returncode, 1)

    def test_missing_input_is_not_evidence(self):
        self.source.unlink()
        self.assertEqual(self.record().returncode, 2)
        self.assertFalse(self.receipt.exists())

    def test_deleted_input_fails_verification(self):
        self.record()
        self.source.unlink()
        self.assertNotEqual(self.cli("verify", self.receipt).returncode, 0)

    def test_no_overwrite_of_prior_evidence(self):
        self.record()
        original = self.receipt.read_bytes()
        self.assertEqual(self.record("print('different run')").returncode, 2)
        self.assertEqual(self.receipt.read_bytes(), original)

    def test_missing_executable_is_not_pass(self):
        result = self.cli("run", "--receipt", self.receipt, "--input", self.source,
                          "--", "this-command-does-not-exist-goal-loop")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(self.receipt.read_text())["exit_code"], 127)
        self.assertEqual(self.cli("verify", self.receipt).returncode, 1)

    def test_no_shell_interpretation(self):
        marker = self.root / "unwanted"
        result = self.cli("run", "--receipt", self.receipt, "--input", self.source,
                          "--", sys.executable, "-c", "import sys; print(sys.argv[1])",
                          "$(touch unwanted)")
        self.assertEqual(result.returncode, 0)
        self.assertFalse(marker.exists())

    def test_symlink_input_is_rejected(self):
        link = self.root / "link.txt"
        link.symlink_to(self.source)
        result = self.cli("run", "--receipt", self.receipt, "--input", link,
                          "--", sys.executable, "-c", "print('ok')")
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.receipt.exists())


if __name__ == "__main__":
    unittest.main()

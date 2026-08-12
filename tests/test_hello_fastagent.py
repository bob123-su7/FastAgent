import subprocess
import sys
import unittest
from pathlib import Path

from examples.hello_fastagent import greet


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples" / "hello_fastagent.py"


class HelloFastAgentTests(unittest.TestCase):
    def test_greet_uses_default_name(self):
        self.assertEqual(greet(), "Hello, FastAgent! Welcome to FastAgent.")

    def test_greet_uses_custom_name(self):
        self.assertEqual(greet("Ada"), "Hello, Ada! Welcome to FastAgent.")

    def test_cli_uses_default_name(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.stdout.strip(), "Hello, FastAgent! Welcome to FastAgent.")

    def test_cli_accepts_custom_name(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "Ada"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.stdout.strip(), "Hello, Ada! Welcome to FastAgent.")

    def test_cli_rejects_extra_arguments(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "Ada", "Extra"],
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("usage:", result.stderr)


if __name__ == "__main__":
    unittest.main()

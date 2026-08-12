"""Tests for the FastAgent greeting example."""

import unittest

from examples.hello_fastagent import greet


class GreetTests(unittest.TestCase):
    def test_uses_fastagent_as_default_name(self):
        self.assertEqual(greet(), "Hello, FastAgent! Welcome to FastAgent.")

    def test_uses_custom_name(self):
        self.assertEqual(greet("Codex"), "Hello, Codex! Welcome to FastAgent.")


if __name__ == "__main__":
    unittest.main()

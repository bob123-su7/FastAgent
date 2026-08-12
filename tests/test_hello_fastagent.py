import unittest

from examples.hello_fastagent import greet


class GreetTest(unittest.TestCase):
    def test_uses_default_name(self) -> None:
        self.assertEqual(greet(), "Hello, FastAgent! Welcome to FastAgent.")

    def test_uses_custom_name(self) -> None:
        self.assertEqual(greet("Contributor"), "Hello, Contributor! Welcome to FastAgent.")


if __name__ == "__main__":
    unittest.main()

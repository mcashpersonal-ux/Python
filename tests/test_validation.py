import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_code  # noqa: E402


class DocumentationValidationTests(unittest.TestCase):
    def test_python_examples_are_valid(self):
        self.assertEqual(validate_code.validate_python_examples(), [])

    def test_navigation_targets_exist(self):
        self.assertEqual(validate_code.validate_navigation(), [])

    def test_internal_links_exist(self):
        self.assertEqual(validate_code.validate_internal_links(), [])


if __name__ == "__main__":
    unittest.main()

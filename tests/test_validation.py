import sys
import unittest
import re
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

    def test_markdown_structure_has_valid_headings(self):
        malformed = []
        for path in validate_code.DOCS.rglob("*.md"):
            in_fence = False
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if not in_fence and re.match(r"^#{1,6}[^ #]", line):
                    malformed.append(f"{path}:{line_number}")
        self.assertEqual(malformed, [])

    def test_known_corruption_artifacts_are_absent(self):
        artifacts = ("uai", "uapt", "uä", "u།", "uams")
        found = []
        for path in validate_code.DOCS.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for artifact in artifacts:
                if artifact in text:
                    found.append(f"{path}:{artifact}")
        self.assertEqual(found, [])

    def test_documentation_filenames_are_globally_numbered(self):
        files = list(validate_code.DOCS.rglob("*.md"))
        invalid = [str(path) for path in files if not re.match(r"^\d{3}-[^/]+\.md$", path.name)]
        numbers = sorted(int(path.name[:3]) for path in files)
        self.assertEqual(invalid, [])
        self.assertEqual(numbers, list(range(len(files))))


if __name__ == "__main__":
    unittest.main()

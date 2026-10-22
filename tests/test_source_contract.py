"""Source-level smoke checks; live Groq, Tavily and weather APIs are not called."""
import ast
from pathlib import Path
import unittest

APP = Path(__file__).resolve().parents[1] / "multi-modal-travel-agent"

class SourceChecks(unittest.TestCase):
    def test_entrypoint_and_agent_modules_parse(self):
        for path in [APP / "app.py", *sorted((APP / "travel_agent").glob("*.py"))]:
            with self.subTest(file=path.name):
                ast.parse(path.read_text(encoding="utf-8"))

    def test_dependency_manifest_exists(self):
        self.assertTrue((APP / "requirements.txt").is_file())

    def test_workflow_diagram_exists(self):
        self.assertTrue((APP / "graph.png").is_file())

if __name__ == "__main__":
    unittest.main()

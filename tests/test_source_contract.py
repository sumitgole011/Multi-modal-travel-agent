"""Source-level smoke checks; live Groq, Tavily and weather APIs are not called."""
import ast
from pathlib import Path
from unittest.mock import Mock
import unittest

APP = Path(__file__).resolve().parents[1] / "multi-modal-travel-agent"

class SourceChecks(unittest.TestCase):
    def test_entrypoint_and_agent_modules_parse(self):
        for path in [APP / "app.py", *sorted((APP / "travel_agent").glob("*.py"))]:
            with self.subTest(file=path.name):
                ast.parse(path.read_text(encoding="utf-8"))

    def test_weather_provider_failure_returns_no_forecast(self):
        graph_path = APP / "travel_agent" / "graph.py"
        tree = ast.parse(graph_path.read_text(encoding="utf-8"))
        node = next(node for node in tree.body
                    if isinstance(node, ast.FunctionDef) and node.name == "fetch_weather")
        provider = Mock(side_effect=TimeoutError)
        scope = {"get_weather": provider, "TravelState": dict}
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(graph_path), "exec"), scope)
        self.assertEqual(scope["fetch_weather"]({"city": "Gwalior"}), {
            "weather_forecast": [],
            "errors": ["Weather forecast is currently unavailable."],
        })
        provider.assert_called_once_with("Gwalior")

    def test_dependency_manifest_exists(self):
        self.assertTrue((APP / "requirements.txt").is_file())

    def test_workflow_diagram_exists(self):
        self.assertTrue((APP / "graph.png").is_file())

if __name__ == "__main__":
    unittest.main()

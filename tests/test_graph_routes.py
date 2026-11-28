"""Run real LangGraph routes with an in-memory index and offline providers."""

from copy import deepcopy
from importlib import import_module
import os
import unittest
from unittest.mock import Mock, patch

from travel_agent.data import INITIAL_CITY_RECORDS, LocalCityStore


class TravelGraphTests(unittest.TestCase):
    def setUp(self):
        self.store = LocalCityStore(memory_records=deepcopy(INITIAL_CITY_RECORDS))
        self.enterContext(patch.dict(os.environ, {
            "GROQ_API_KEY": "",
            "LANGCHAIN_TRACING_V2": "false",
            "LANGSMITH_TRACING": "false",
        }))
        with patch.object(LocalCityStore, "build", return_value=self.store):
            graph = import_module("travel_agent.graph")
        self.enterContext(patch.object(graph, "STORE", self.store))
        self.enterContext(patch.object(graph, "get_llm", side_effect=RuntimeError("Offline test")))
        self.search = Mock()
        self.enterContext(patch.dict(graph.TOOLS, {"web_search": self.search}))
        self.weather = self.enterContext(patch.object(graph, "get_weather"))
        self.workflow = graph.build_graph()

    def ask(self, question):
        return self.workflow.invoke(
            {"query": question},
            config={"configurable": {"thread_id": self._testMethodName}},
        )

    def test_known_city_uses_local_index_and_skips_web_search(self):
        forecast = [{
            "date": "2026-11-23",
            "temperature_c": 12.5,
            "condition": "Clear sky",
            "humidity": 60,
            "precipitation_probability": 0,
        }]
        self.weather.return_value = forecast

        state = self.ask("Tell me about Paris")

        self.assertEqual(state["city"], "Paris")
        self.assertEqual(state["route"], "internal")
        self.search.invoke.assert_not_called()
        self.weather.assert_called_once_with("Paris")
        response = state["final_response"]
        self.assertTrue(response["city_summary"].startswith(self.store.get("Paris")["summary"]))
        self.assertIn("Suggested day plan:", response["city_summary"])
        self.assertEqual(response["image_urls"], self.store.get("Paris")["image_urls"])
        self.assertEqual(response["weather_forecast"], forecast)

    def test_missing_city_uses_web_search_and_keeps_plan_on_weather_timeout(self):
        self.assertIsNone(self.store.get("Lisbon"))
        snippet = "Lisbon is known for Alfama, its hilltop viewpoints, and the waterfront in Belem."
        image_url = "https://example.com/lisbon.jpg"
        self.search.invoke.return_value = {
            "matched_city": "Lisbon",
            "source": "test",
            "sources": [{"snippet": snippet}],
            "image_urls": [image_url],
        }
        self.weather.side_effect = TimeoutError("Simulated provider timeout")

        state = self.ask("Tell me about Lisbon")

        self.assertEqual(state["city"], "Lisbon")
        self.assertEqual(state["route"], "web")
        self.search.invoke.assert_called_once_with({"city": "Lisbon"})
        self.weather.assert_called_once_with("Lisbon")
        self.assertEqual(state["errors"], ["Weather forecast is currently unavailable."])
        response = state["final_response"]
        self.assertIn(snippet, response["city_summary"])
        self.assertIn("Suggested day plan:", response["city_summary"])
        self.assertEqual(response["image_urls"], [image_url])
        self.assertEqual(response["weather_forecast"], [])

    def test_weather_question_can_switch_to_a_city_outside_local_index(self):
        self.weather.return_value = []
        self.ask("Tell me about Paris")
        self.weather.reset_mock()
        self.search.invoke.return_value = {}

        state = self.ask("What's the weather in Lisbon?")

        self.assertEqual(state["city"], "Lisbon")
        self.assertFalse(state["refresh_weather_only"])
        self.weather.assert_called_once_with("Lisbon")

    def test_weather_followup_without_destination_reuses_current_city(self):
        self.weather.return_value = []
        self.ask("Tell me about Paris")
        self.weather.reset_mock()

        state = self.ask("What about the weather next week?")

        self.assertEqual(state["city"], "Paris")
        self.assertTrue(state["refresh_weather_only"])
        self.weather.assert_called_once_with("Paris")

    def test_successful_weather_followup_clears_previous_warning(self):
        forecast = [{
            "date": "2026-11-26",
            "temperature_c": 14.0,
            "condition": "Clear sky",
            "humidity": 60,
            "precipitation_probability": 0,
        }]
        self.weather.side_effect = [TimeoutError("Provider timeout"), forecast]

        failed = self.ask("Tell me about Paris")
        self.assertEqual(failed["errors"], ["Weather forecast is currently unavailable."])

        recovered = self.ask("What about the weather next week?")
        self.assertEqual(recovered["errors"], [])
        self.assertEqual(recovered["final_response"]["weather_forecast"], forecast)

    def test_unverified_search_results_do_not_supply_images_or_create_a_city_record(self):
        self.weather.return_value = []
        for match in ("", "Madrid"):
            with self.subTest(match=match):
                self.search.invoke.return_value = {
                    "matched_city": match,
                    "source": "test",
                    "sources": [{"snippet": "Madrid has the Prado Museum."}],
                    "image_urls": ["https://example.com/madrid.jpg"],
                }

                state = self.ask("Tell me about Lisbon")

                self.assertIn("could not verify", state["final_response"]["city_summary"])
                self.assertEqual(state["final_response"]["image_urls"], [])
                self.assertIsNone(self.store.get("Lisbon"))

    def test_verified_search_snippet_is_used_when_summary_model_is_unavailable(self):
        snippet = "Lisbon is known for Alfama and the waterfront in Belem."
        self.search.invoke.return_value = {
            "matched_city": "Lisbon",
            "source": "test",
            "sources": [{"snippet": snippet}],
            "image_urls": [],
        }
        self.weather.return_value = []

        with patch.dict(os.environ, {"GROQ_API_KEY": "offline-test-key"}):
            state = self.ask("Tell me about Lisbon")

        self.assertEqual(state["final_response"]["city_summary"], snippet)
        self.assertEqual(self.store.get("Lisbon")["summary"], snippet)
        self.weather.assert_called_once_with("Lisbon")

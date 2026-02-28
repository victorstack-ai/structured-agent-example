# tests/test_agent.py

import unittest
from unittest.mock import patch
from structured_agent_example.agent import SentimentAgent

class TestSentimentAgent(unittest.TestCase):

    def setUp(self):
        """Set up a basic config for each test."""
        self.config = {"model_name": "test-model-v1"}

    def test_agent_initialization(self):
        """Tests that the agent initializes correctly with valid config."""
        agent = SentimentAgent(self.config)
        self.assertEqual(agent.config["model_name"], "test-model-v1")

    def test_agent_init_fails_without_model(self):
        """Tests that initialization fails if config is missing the model name."""
        with self.assertRaises(ValueError):
            SentimentAgent({})

    def test_run_handles_empty_input(self):
        """Tests the agent returns an error for empty or invalid input."""
        agent = SentimentAgent(self.config)
        result = agent.run("")
        self.assertEqual(result["status"], "error")
        self.assertIn("Invalid text input", result["message"])

    @patch('structured_agent_example.llm_service.get_sentiment')
    def test_run_positive_sentiment(self, mock_get_sentiment):
        """Tests the agent's run method with a mock for a positive sentiment."""
        # Configure the mock to return a specific value
        mock_get_sentiment.return_value = "positive"
        
        agent = SentimentAgent(self.config)
        text = "This is a great product, I love it!"
        result = agent.run(text)
        
        # Assert that our mock was called correctly
        mock_get_sentiment.assert_called_once_with(text, model="test-model-v1")
        
        # Assert that the agent processed the result correctly
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["sentiment"], "positive")
        self.assertEqual(result["input"], text)

    @patch('structured_agent_example.llm_service.get_sentiment')
    def test_run_negative_sentiment(self, mock_get_sentiment):
        """Tests the agent's run method with a mock for a negative sentiment."""
        mock_get_sentiment.return_value = "negative"
        
        agent = SentimentAgent(self.config)
        text = "This is a terrible experience."
        result = agent.run(text)
        
        mock_get_sentiment.assert_called_once_with(text, model="test-model-v1")
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["sentiment"], "negative")

    @patch('structured_agent_example.llm_service.get_sentiment')
    def test_run_handles_llm_exception(self, mock_get_sentiment):
        """Tests that the agent handles exceptions from the LLM service gracefully."""
        # Configure the mock to raise an exception
        mock_get_sentiment.side_effect = Exception("API connection failed")

        agent = SentimentAgent(self.config)
        text = "Some input."
        result = agent.run(text)

        self.assertEqual(result["status"], "error")
        self.assertIn("An unexpected error occurred", result["message"])

    # --- Additional edge-case tests ---

    @patch('structured_agent_example.llm_service.get_sentiment')
    def test_run_neutral_sentiment(self, mock_get_sentiment):
        """Tests the agent correctly returns neutral sentiment."""
        mock_get_sentiment.return_value = "neutral"

        agent = SentimentAgent(self.config)
        text = "The meeting is scheduled for 3pm."
        result = agent.run(text)

        mock_get_sentiment.assert_called_once_with(text, model="test-model-v1")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["sentiment"], "neutral")
        self.assertEqual(result["input"], text)

    def test_run_none_input(self):
        """Tests that the agent returns an error when input is None."""
        agent = SentimentAgent(self.config)
        result = agent.run(None)

        self.assertEqual(result["status"], "error")
        self.assertIn("Invalid text input", result["message"])
        self.assertIsNone(result["sentiment"])

    def test_run_non_string_input(self):
        """Tests that the agent returns an error when input is not a string (e.g., int)."""
        agent = SentimentAgent(self.config)
        result = agent.run(12345)

        self.assertEqual(result["status"], "error")
        self.assertIn("Invalid text input", result["message"])
        self.assertIsNone(result["sentiment"])

    @patch('structured_agent_example.llm_service.get_sentiment')
    def test_run_preserves_original_input(self, mock_get_sentiment):
        """Tests that the response includes the exact original input text."""
        mock_get_sentiment.return_value = "positive"

        agent = SentimentAgent(self.config)
        text = "  Whitespace around great text  "
        result = agent.run(text)

        # The agent should preserve the original input exactly as provided
        self.assertEqual(result["input"], text)
        self.assertEqual(result["input"], "  Whitespace around great text  ")

if __name__ == '__main__':
    unittest.main()

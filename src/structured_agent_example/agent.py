# src/structured_agent_example/agent.py

from typing import Dict, Any
from . import llm_service

class SentimentAgent:
    def __init__(self, config: Dict[str, Any]):
        if "model_name" not in config:
            raise ValueError("Configuration must include 'model_name'")
        self.config = config

    def run(self, text_input: str) -> Dict[str, Any]:
        """
        Runs the sentiment analysis agent.
        """
        if not text_input or not isinstance(text_input, str):
            return {
                "status": "error",
                "message": "Invalid text input.",
                "sentiment": None
            }

        model_name = self.config["model_name"]
        
        try:
            sentiment = llm_service.get_sentiment(text_input, model=model_name)
            return {
                "status": "success",
                "input": text_input,
                "sentiment": sentiment
            }
        except Exception as e:
            # In a real app, log the error
            return {
                "status": "error",
                "message": f"An unexpected error occurred: {e}",
                "sentiment": None
            }

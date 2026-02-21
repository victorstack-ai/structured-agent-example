# src/structured_agent_example/llm_service.py

import time

def get_sentiment(text: str, model: str) -> str:
    """
    Simulates calling a Large Language Model (LLM) to get sentiment.
    In a real application, this would make an API call to a service like
    Gemini, OpenAI, or a local model.
    """
    print(f"Analyzing sentiment for: '{text}' using model: {model}")
    # Simulate network latency
    time.sleep(0.1)

    # Simple rule-based mock for predictable testing
    text_lower = text.lower()
    if "great" in text_lower or "love" in text_lower or "excellent" in text_lower:
        return "positive"
    if "bad" in text_lower or "terrible" in text_lower or "hate" in text_lower:
        return "negative"
    
    return "neutral"

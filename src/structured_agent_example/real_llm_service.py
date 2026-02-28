# src/structured_agent_example/real_llm_service.py

"""
Real LLM Service using the Anthropic Claude API.

This module provides a drop-in replacement for llm_service.py that calls
the actual Claude API instead of using rule-based mocking. To use it,
set the ANTHROPIC_API_KEY environment variable and swap the import in agent.py.

Usage:
    export ANTHROPIC_API_KEY="your-api-key-here"

    from structured_agent_example.real_llm_service import get_sentiment
    sentiment = get_sentiment("I love this product!", model="claude-sonnet-4-20250514")
"""

import os
from anthropic import Anthropic


def get_sentiment(text: str, model: str = "claude-sonnet-4-20250514") -> str:
    """
    Calls the Anthropic Claude API to classify the sentiment of the given text.

    Args:
        text: The text to analyze for sentiment.
        model: The Claude model to use (e.g., "claude-sonnet-4-20250514",
               "claude-haiku-4-20250414").

    Returns:
        A string: "positive", "negative", or "neutral".

    Raises:
        RuntimeError: If the ANTHROPIC_API_KEY environment variable is not set.
        anthropic.APIError: If the API call fails.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY environment variable is not set. "
            "Get your API key at https://console.anthropic.com/"
        )

    client = Anthropic(api_key=api_key)

    system_prompt = (
        "You are a sentiment classifier. Your job is to classify the sentiment "
        "of user-provided text. You must respond with exactly one word: "
        '"positive", "negative", or "neutral". Do not include any other text, '
        "punctuation, or explanation in your response."
    )

    message = client.messages.create(
        model=model,
        max_tokens=10,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"Classify the sentiment of the following text:\n\n{text}",
            }
        ],
    )

    # Extract the text response and normalize it
    raw_response = message.content[0].text.strip().lower()

    # Validate the response is one of the expected sentiments
    valid_sentiments = {"positive", "negative", "neutral"}
    if raw_response not in valid_sentiments:
        # If the model returns something unexpected, default to neutral
        # and log a warning in production
        print(
            f"Warning: Unexpected sentiment response '{raw_response}', "
            f"defaulting to 'neutral'"
        )
        return "neutral"

    return raw_response

# Structured Agent Example

This project is a companion to the article "Beyond the Vibe: A Practical Guide to Engineering Agentic AI Systems". It demonstrates a structured, test-driven approach to developing a simple AI agent.

The agent's task is to receive a text input, classify its sentiment (positive, negative, or neutral), and return a structured response.

## Key Principles Demonstrated

*   **Modular Design:** The agent's logic, the "LLM" call (mocked for this example), and the configuration are separated.
*   **Test-Driven Development:** Unit tests are provided for the agent's core logic.
*   **Configuration Management:** Key parameters (like the "model name") are stored in a separate configuration file.

# Structured Agent Example

Companion code for the article **"Beyond the Vibe: A Practical Guide to Engineering Agentic AI Systems"**.

This project demonstrates how to build a structured, test-driven AI agent using clean software engineering principles -- not just "vibes". It implements a **sentiment classification agent** that receives text input, classifies its sentiment (positive, negative, or neutral), and returns a structured response. The codebase is intentionally small and focused so you can study the architecture and apply it to more complex agentic systems.

---

## Table of Contents

- [Architecture](#architecture)
- [How the Agent Works](#how-the-agent-works)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Extending the Project](#extending-the-project)
- [Key Concepts](#key-concepts)
- [License](#license)

---

## Architecture

```
+---------------------+       +---------------------+       +---------------------+
|                     |       |                     |       |                     |
|   User / Caller     +------>+   SentimentAgent    +------>+   LLM Service       |
|                     |       |   (agent.py)        |       |   (llm_service.py)  |
|                     |       |                     |       |                     |
+---------------------+       +----------+----------+       +---------------------+
                                         |                           |
                                         |   config (model_name)     |   Swappable:
                                         |   input validation        |   - MockLLM (default)
                                         |   error handling          |   - RealLLM (Claude API)
                                         |   structured response     |
                                         v                           v
                              +---------------------+       +---------------------+
                              |  Structured Output   |       | real_llm_service.py |
                              |  {status, sentiment, |       | (Anthropic SDK)     |
                              |   input, message}    |       +---------------------+
                              +---------------------+
```

## How the Agent Works

The agent follows a disciplined **Receive -> Execute -> Respond** loop:

1. **Receive**: The agent receives a text input string and validates it. If the input is empty or not a string, it immediately returns a structured error response.

2. **Execute**: The agent delegates the actual sentiment analysis to the **LLM Service** layer. The service is decoupled from the agent, making it easy to swap between a mock (for testing) and a real LLM provider (for production).

3. **Respond**: The agent wraps the result in a structured dictionary containing the status (`success` or `error`), the original input, and the classified sentiment.

This separation ensures that:
- The agent's orchestration logic is testable independently of the LLM.
- The LLM can be swapped without changing the agent.
- Errors are caught and returned as structured responses, never as unhandled exceptions.

---

## Project Structure

```
structured-agent-example/
|-- src/
|   |-- structured_agent_example/
|       |-- __init__.py
|       |-- agent.py              # Core agent with validation and orchestration
|       |-- llm_service.py        # Mock LLM service (rule-based, for testing)
|       |-- real_llm_service.py   # Real LLM service (Anthropic Claude API)
|-- tests/
|   |-- __init__.py
|   |-- test_agent.py             # Unit tests for the agent
|-- pyproject.toml                # Project metadata and build config
|-- requirements.txt              # Python dependencies
|-- LICENSE                       # MIT License
|-- README.md                     # This file
```

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip

### Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/structured-agent-example.git
cd structured-agent-example

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the project in editable mode
pip install -e .

# Install dependencies (needed only for the real LLM service)
pip install -r requirements.txt
```

---

## Usage

### Basic Usage with the Mock LLM

```python
from structured_agent_example.agent import SentimentAgent

# Create the agent with a configuration
config = {"model_name": "mock-model-v1"}
agent = SentimentAgent(config)

# Analyze positive sentiment
result = agent.run("This product is great, I love it!")
print(result)
# Output: {'status': 'success', 'input': 'This product is great, I love it!', 'sentiment': 'positive'}

# Analyze negative sentiment
result = agent.run("This is a terrible experience.")
print(result)
# Output: {'status': 'success', 'input': 'This is a terrible experience.', 'sentiment': 'negative'}

# Analyze neutral sentiment
result = agent.run("The meeting is at 3pm.")
print(result)
# Output: {'status': 'success', 'input': 'The meeting is at 3pm.', 'sentiment': 'neutral'}

# Handle invalid input
result = agent.run("")
print(result)
# Output: {'status': 'error', 'message': 'Invalid text input.', 'sentiment': None}
```

### Using the Real LLM Service (Claude API)

To use the real LLM provider, see `src/structured_agent_example/real_llm_service.py`. You need to set the `ANTHROPIC_API_KEY` environment variable:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

```python
from structured_agent_example.real_llm_service import get_sentiment

sentiment = get_sentiment("I absolutely love this!", model="claude-sonnet-4-20250514")
print(sentiment)  # "positive"
```

---

## Testing

The project uses `unittest` with mocking to isolate the agent logic from the LLM service.

```bash
# Run all tests
python -m pytest tests/ -v

# Run tests with unittest directly
python -m unittest discover tests -v
```

### What the Tests Cover

| Test Case                          | Description                                           |
|------------------------------------|-------------------------------------------------------|
| `test_agent_initialization`        | Agent initializes correctly with valid config          |
| `test_agent_init_fails_without_model` | Raises `ValueError` when `model_name` is missing   |
| `test_run_handles_empty_input`     | Returns structured error for empty string input        |
| `test_run_positive_sentiment`      | Correctly classifies positive text via mocked LLM      |
| `test_run_negative_sentiment`      | Correctly classifies negative text via mocked LLM      |
| `test_run_handles_llm_exception`   | Gracefully handles LLM service exceptions              |
| `test_run_neutral_sentiment`       | Correctly classifies neutral text via mocked LLM       |
| `test_run_none_input`              | Returns structured error when input is `None`          |
| `test_run_non_string_input`        | Returns structured error when input is not a string    |
| `test_run_preserves_original_input`| The response includes the exact original input text    |

---

## Extending the Project

### Adding a New Tool

To add a new capability (e.g., named entity recognition), create a new service module:

```python
# src/structured_agent_example/ner_service.py

def get_entities(text: str, model: str) -> list:
    """Extract named entities from text using an LLM."""
    # Your implementation here
    pass
```

Then update the agent to call it:

```python
# In agent.py, add a new method:
def extract_entities(self, text_input: str) -> Dict[str, Any]:
    entities = ner_service.get_entities(text_input, model=self.config["model_name"])
    return {"status": "success", "entities": entities}
```

### Swapping the LLM Provider

The LLM service is fully decoupled from the agent. To swap providers:

1. Create a new module (e.g., `openai_llm_service.py`) that exposes the same `get_sentiment(text, model)` interface.
2. Update the import in `agent.py`:

```python
# Change this:
from . import llm_service

# To this:
from . import openai_llm_service as llm_service
```

The agent code itself requires no changes because it depends on the interface, not the implementation.

---

## Key Concepts

### Separation of Concerns

The agent (`agent.py`) handles orchestration: input validation, calling the LLM, and formatting the response. The LLM service (`llm_service.py`) handles the actual model interaction. This makes each piece independently testable and replaceable.

### Dependency Injection via Configuration

The agent receives its configuration (including `model_name`) through a dictionary at initialization time. This avoids hardcoded values and makes the agent configurable for different environments (development, testing, production).

### Structured Error Handling

Instead of raising exceptions to the caller, the agent catches errors internally and returns them as structured dictionaries with `"status": "error"`. This is critical for agentic systems where upstream orchestrators need to programmatically handle failures.

### Test Isolation with Mocking

Tests use `unittest.mock.patch` to replace the LLM service with a mock. This means tests run instantly (no API calls), are deterministic (no flaky network behavior), and verify the agent's logic independently of the LLM's behavior.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

# Part 1: Techniques to Prevent Unexpected Behaviour

This document explains the different techniques used to ensure the Twenty Questions game doesn’t have any unexpected behaviour.

## Response Validation and Normalisation

LLMs can produce different output formats even when they are asked for simple responses.

The `validators.py` module implements normalisation functions that:
- Strip whitespace and convert to lowercase for yes/no answers
- Detect variations ("yes", "y", "no", "n") and normalise to "yes" or "no"
- Extract object names from guesses by removing prefixes such as "I think it's" or "My guess is"

This ensures that the game logic receives consistent input regardless of how the LLM phrases its response.

## Error Handling

LLM API calls can fail because of network issues, rate limiting, timeouts, or service unavailability. Without proper handling, these failures may crash the game or leave it in an inconsistent state.

The `llm_client.py` module implements:
- **Retry logic with exponential backoff:** Failed requests are retried up to 3 times with increasing delays (1s, 2s, 4s)
- **Specific handling for rate limits (429):** Uses exponential backoff to respect API rate limits
- **Timeout protection:** 30-second timeout prevents indefinite hanging
- **Custom exception types:** `LLMError` provides clear error messages for debugging


## Input Validation

Human players might enter invalid input (answering "maybe" to a yes/no question, or submitting empty strings).

The frontend and backend both validate input:
- **Client-side validation:** The React frontend checks yes/no answers before submission, giving immediate feedback
- **Server-side validation:** The API handlers (`handlers.py`) validate all inputs, returning clear error messages for invalid submissions
- **Empty input protection:** Both layers check for empty or whitespace-only input

This makes sure that invalid data does not reach the game logic.

## State Management

Game state must stay consistent throughout the game. If the state becomes corrupted ( question count exceeding 20, objects being set multiple times), the game logic breaks.

The `GameState` class handles all state management:
- **Immutable constants:** `MAX_QUESTIONS` is defined and used consistently
- **Encapsulated state changes:** Methods like `increment_question()` and `win()` ensure state transitions are valid
- **Status checking:** `is_playing()` provides game status and ensures the game progresses

## Prompt Engineering

Poorly structured prompts cause LLMs to produce unexpected output, ask invalid questions, or make bad strategic decisions.

The `prompts.py` module uses structured prompts that:
- **Explicitly specify format requirements:** "Respond with ONLY 'yes' or 'no'" prevents verbose answers
- **Provide examples:** Shows the LLM what good questions look like
- **Include context:** Conversation history is included so that the LLM can make informed decisions
- **Set clear constraints:** "Choose a RANDOM and VARIED object" encourages diversity in object selection

Well worded prompts reduce the need for post-processing and improve LLM interactions.

## Conversation History Management

LLMs need context to make good decisions. Without tracking previous questions and answers, the LLM cannot build upon previous information.

The `LLMPlayer` class maintains a `conversation_history` list that:
- Records each question-answer pair
- Passes the full history to prompts when asking questions or making guesses
- Allows the LLM to reason about what it has learned so far

This ensures the LLM's questions become more targeted over time and its guesses are based on accumulated information.

## Defensive Programming

Even with validation, unexpected scenarios can occur (API returns malformed JSON, LLM returns empty string).

The code includes defensive checks:
- **Null/empty checks:** All LLM responses are checked before use
- **Fallback values:** If validation fails, sensible defaults are used (e.g., "no" for invalid yes/no answers)
- **Type checking:** The code assumes LLM responses might be in unexpected formats and handles them gracefully

These checks ensure the game keeps working even when the LLM behaves unexpectedly.

## Separation of Concerns

Mixing game logic, API calls, and validation makes the code harder to test and debug. When unexpected behaviour occurs, it's difficult to isolate the cause.

The codebase is organised into distinct modules:
- **Core logic** (`core/`): Game state and player abstractions
- **Player implementations** (`players/`): Human and LLM-specific logic
- **API layer** (`api.py`, `handlers.py`): Request handling separate from game logic
- **Utilities** (`validators.py`, `llm_client.py`): Reusable functions

This modular structure makes it easier to identify and fix issues when unexpected behaviour occurs.


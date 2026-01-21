# Part 2: LLM vs LLM Implementation

This document explains how the implementation from Part 1 was extended to support two LLMs playing against each other.

## Architecture Extension

The design used an abstract `Player` base class, which made adding LLM vs LLM mode straightforward. The game logic does not depend on the player types (Human and LLM), so no modifications are required to support different player combinations.

The `GameManager.create_game()` method accepts `player1_type` and `player2_type` as parameters. When they are both set to "llm", two `LLMPlayer` instances are created. The existing game loop handles LLM players identically to human players, with the only difference being that LLM actions are generated programmatically rather than through user input.

## Auto-Advance Mechanism

When both players are LLMs, the game progresses automatically without user intervention. The frontend includes a `useEffect` hook that monitors game state and automatically calls `GET /api/game/next` when Player 2 is an LLM. The backend `/api/game/next` endpoint handles LLM decision-making:

- Player 2 decides whether to ask a question or make a guess using `decide_action()`
- If asking: Player 2 generates a question, Player 1 answers truthfully
- If guessing: Player 2 makes a guess, game checks correctness
- The endpoint returns the result, and the frontend auto-advances again after a 1-second delay

## Conversation Management

Each `LLMPlayer` instance maintains its own `conversation_history`. Player 2's history tracks all previous questions and their corresponding answers to make better decisions. Player 1 only needs to know the object it chose. When Player 2 asks a question, Player 1 answers truthfully based on its chosen object, and Player 2 records the interaction. This history is included in all following prompts to help Player 2 make better decisions.

## Strategic Decision Making

Player 2's `decide_action()` method uses a prompt that includes the number of remaining questions and conversation history. The LLM evaluates whether it has enough information to guess confidently. A rule forces a guess when only 1 question remains to prevent running out of questions. This allows the LLM to make strategic decisions about when it's confident enough to guess versus when it needs more information.


# Part 3: LLM Performance Evaluation Scheme

This document outlines how to implement automatic evaluation of LLM performance as both Player 1 and Player 2, potential emergent behaviour and proposes methods to prevent or encourage specific behaviours.

## Evaluation Scheme

### Metrics for Player 2 (Asking Questions and Guessing the Object)

Player 2's performance depends on how efficiently they narrow down object possibilities and how accurately they guess the chosen object. Metrics must capture both strategic thinking and final outcomes.

**How to measure:**

1. **Ratio of Questions to correct guess:** Track how many questions Player 2 asks before guessing correctly. The lower the better, indicating a more efficient questioning strategy.

2. **Information gain per question:** Calculate how much each question narrows the search space. Questions that eliminate roughly half the remaining possibilities are optimal. This can be approximated by:
   - Maintaining a set of possible objects
   - After each answer, calculating how many objects remain

3. **Guess accuracy:** Percentage of games where Player 2 guesses correctly within 20 questions. Higher indicates better performance.

4. **Question quality:** Analyse whether questions follow a good strategy (broad to narrow, binary splits). This could be done by:
   - Checking if early questions are categorical (e.g., "Is it an animal?")
   - Verifying that later questions are more specific
   - Measuring how diverse questions are (avoiding repetitive questions)

5. **Win rate:** Percentage of games won by Player 2. This shows overall performance.

### Metrics for Player 1 (Answering Questions)

Player 1's role is simpler but still important. They must answer truthfully and choose objects that are reasonable to guess.

**How to measure:**

1. **Object appropriateness:** Evaluate whether chosen objects are:
   - Common enough to guess
   - Not too specific or obscure
   - Varied across multiple games (not always choosing the same object)

2. **Answer consistency:** Verify that answers are truthful and consistent with the chosen object. This can be checked by:
   - Re-evaluating each question against the object
   - Flagging any inconsistencies
   - Measuring answer accuracy percentage

3. **Object diversity:** Track the variety of objects chosen across multiple games. Low diversity suggests the LLM is stuck in a pattern.

To get meaningful results, run multiple games (100-1000) with LLM as both players and record all game states, questions, answers, and outcomes. Compare performance against baselines like human players, random guessing, or optimal binary search strategies.

## Emergent Behaviour

When an LLM is trained or fine-tuned on its performance in this game, it may develop strategies and patterns that weren't explicitly programmed.

**What to expect:**

1. **Object selection patterns:**
   - LLM might learn to choose objects that are easier or harder to guess
   - Could develop preferences for certain categories (animals, objects, etc.)
   - Might learn to avoid obscure objects that lead to losses
   - May develop strong preferences for certain objects (currently favours toothbrush, umbrella) even without explicit training, suggesting API-level constraints or model bias

2. **Question strategies:**
   - Could develop optimal question sequences for common objects
   - Might learn to ask questions in a specific order (e.g., always starting with "Is it an animal?")
   - Could develop shortcuts for frequently chosen objects

3. **Timing of guesses:**
   - Might learn the optimal point to switch from asking to guessing
   - Could become overly cautious (always asking too many questions) or overly confident (guessing too early)

4. **Exploitation:**
   - If Player 1's object selection becomes predictable, Player 2 might exploit patterns

### Preventing Undesirable Behaviour

Some emergent behaviours could make the game less interesting or fair. We want to prevent the LLM from developing exploitative or repetitive patterns.

The LLM currently favours certain objects (toothbrush, umbrella) even with varied prompts. To address this, increase the temperature setting when calling the LLM for object selection, this encourages more randomness and variety. Add explicit instructions in prompts to choose varied objects and track object selection history to penalise repetition. If the LLM becomes too predictable, randomly sample from a diverse object pool. Limit how many times the same question type can be asked and encourage exploration of different questioning approaches. This prevents the LLM from memorising optimal question sequences. 

### Encouraging Desirable Behaviour

We want the LLM to develop good strategic thinking, efficient questioning, and appropriate object selection.

Provide explicit feedback in prompts about what constitutes good performance. Include examples of optimal question sequences and highlight efficient games where fewer questions led to correct guesses. Include examples of good vs. poor performance in prompts. Include statistics in prompts, for example "You typically guess correctly in 8 questions". This encourages self-reflection about what could be improved. Provide feedback loops that help the LLM learn from its mistakes. Explicitly teach binary search principles in prompts, provide examples of questions that efficiently narrow possibilities, and encourage the LLM to think about information gain.


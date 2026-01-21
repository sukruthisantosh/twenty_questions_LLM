"""LLM player implementation."""
from ..core.player import Player
from ..constants import PLAYER1, PLAYER2
from ..llm_client import call_llm, LLMError
from ..validators import validate_yes_no, validate_guess
from ..prompts import (
    get_set_object_prompt,
    get_ask_question_prompt,
    get_make_guess_prompt,
    get_decide_action_prompt,
    get_answer_question_prompt
)


class LLMPlayer(Player):
    """LLM player that uses the API to play."""
    
    def __init__(self, role, game_state):
        super().__init__(role, game_state)
        self.conversation_history = [] # Stores conversation history for LLM Player 2
        self.chosen_object = None # Stores object chosen by LLM Player 1
    
    def _call_llm(self, prompt, default=None):
        """Helper method to call LLM with a prompt and handle errors."""
        try:
            messages = [{"role": "user", "content": prompt}]
            result = call_llm(messages)
            return result.strip() if result else default
        except LLMError:
            return default
    
    def ask_question(self):
        """Player 2 asks a yes/no question using the LLM."""
        if self.role != PLAYER2:
            return None
        prompt = get_ask_question_prompt(self.conversation_history)
        return self._call_llm(prompt)
    
    def make_guess(self):
        """Player 2 makes a guess using the LLM."""
        if self.role != PLAYER2:
            return None
        prompt = get_make_guess_prompt(self.conversation_history)
        guess = self._call_llm(prompt)
        if not guess:
            return None
        validated = validate_guess(guess)
        return validated if validated else guess
    
    def decide_action(self):
        """Decide whether to ask a question or make a guess."""
        if self.role != PLAYER2:
            return None
        remaining = 20 - self.game_state.question_count
        if remaining < 2: # Force a guess when only 1 question remains
            return "guess"
        
        prompt = get_decide_action_prompt(remaining, self.conversation_history)
        decision = self._call_llm(prompt, default="question")
        if decision and (decision.startswith("guess") or decision == "g"):
            return "guess"
        return "question"
    
    def set_object(self):
        """Player 1 thinks of an object using the LLM."""
        if self.role != PLAYER1:
            return None
        prompt = get_set_object_prompt()
        obj = self._call_llm(prompt)
        if obj:
            self.chosen_object = obj
            self.game_state.set_object(obj)
            return obj
        return None
    
    def answer_question(self, question):
        """Player 1 answers a yes/no question truthfully."""
        if self.role != PLAYER1:
            return None
        if not self.chosen_object:
            self.chosen_object = self.game_state.object
        
        prompt = get_answer_question_prompt(self.chosen_object, question)
        answer = self._call_llm(prompt, default="no")
        if not answer:
            return "no"
        validated = validate_yes_no(answer)
        return validated if validated else "no"
    
    def record_interaction(self, question, answer):
        """Record a question-answer interaction."""
        if self.role == PLAYER2:
            self.conversation_history.append({
                "question": question,
                "answer": answer
            })


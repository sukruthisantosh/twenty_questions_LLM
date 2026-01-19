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
        self.conversation_history = []
        self.chosen_object = None
    
    def ask_question(self):
        """Player 2 asks a yes/no question using the LLM."""
        if self.role == PLAYER2:
            prompt = get_ask_question_prompt(self.conversation_history)
            
            try:
                messages = [{"role": "user", "content": prompt}]
                question = call_llm(messages)
                return question.strip() if question else None
            except LLMError as e:
                print(f"Error getting question: {e}")
                return None
        return None
    
    def make_guess(self):
        """Player 2 makes a guess using the LLM."""
        if self.role == PLAYER2:
            prompt = get_make_guess_prompt(self.conversation_history)
            
            try:
                messages = [{"role": "user", "content": prompt}]
                guess = call_llm(messages)
                validated = validate_guess(guess)
                if validated:
                    return validated
                return guess.strip() if guess else None
            except LLMError as e:
                print(f"Error making guess: {e}")
                return None
        return None
    
    def decide_action(self):
        """Decide whether to ask a question or make a guess."""
        if self.role == PLAYER2:
            remaining = 20 - self.game_state.question_count
            
            if remaining <= 2:
                return "guess"
            
            prompt = get_decide_action_prompt(remaining, self.conversation_history)
            
            try:
                messages = [{"role": "user", "content": prompt}]
                decision = call_llm(messages).strip().lower()
                
                if decision.startswith("guess") or decision == "g":
                    return "guess"
                return "question"
            except LLMError as e:
                print(f"Error deciding action: {e}")
                return "question"
        return None
    
    def set_object(self):
        """Player 1 thinks of an object using the LLM."""
        if self.role == PLAYER1:
            prompt = get_set_object_prompt()
            
            try:
                messages = [{"role": "user", "content": prompt}]
                obj = call_llm(messages).strip()
                if obj:
                    self.chosen_object = obj
                    self.game_state.set_object(obj)
                    return obj
            except LLMError as e:
                print(f"Error setting object: {e}")
            return None
        return None
    
    def answer_question(self, question):
        """Player 1 answers a yes/no question truthfully based on the chosen object."""
        if self.role == PLAYER1:
            if not self.chosen_object:
                self.chosen_object = self.game_state.object
            
            prompt = get_answer_question_prompt(self.chosen_object, question)
            
            try:
                messages = [{"role": "user", "content": prompt}]
                answer = call_llm(messages)
                validated = validate_yes_no(answer)
                if validated:
                    return validated
                answer_lower = answer.strip().lower()
                if answer_lower.startswith("yes") or answer_lower == "y":
                    return "yes"
                return "no"
            except LLMError as e:
                print(f"Error answering question: {e}")
                return "no"
        return None
    
    def record_interaction(self, question, answer):
        """Record a question-answer interaction for conversation history."""
        if self.role == PLAYER2:
            self.conversation_history.append({
                "question": question,
                "answer": answer
            })


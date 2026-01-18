"""Player implementations for Twenty Questions."""
from game_state import GameState
from llm_client import call_llm

PLAYER1 = "player1"
PLAYER2 = "player2"

class HumanPlayer:
    """Human player that gets input from user."""
    
    def __init__(self, role, game_state):
        self.role = role
        self.game_state = game_state
    
    def set_object(self):
        """Player 1 sets the object they're thinking of."""
        if self.role == PLAYER1:
            obj = input("What object are you thinking of? ").strip()
            self.game_state.set_object(obj)
            return obj
        return None
    
    def answer_question(self, question):
        """Player 1 answers a yes/no question."""
        if self.role == PLAYER1:
            while True:
                answer = input(f"Question: {question}\nYour answer (yes/no): ").strip().lower()
                if answer in ["yes", "no", "y", "n"]:
                    return "yes" if answer in ["yes", "y"] else "no"
                print("Please answer 'yes' or 'no'.")
        return None
    
    def ask_question(self):
        """Player 2 asks a yes/no question."""
        if self.role == PLAYER2:
            question = input("Ask a yes/no question: ").strip()
            return question
        return None
    
    def make_guess(self):
        """Player 2 makes a guess."""
        if self.role == PLAYER2:
            guess = input("Make your guess: ").strip()
            return guess
        return None


class LLMPlayer:
    """LLM player that uses the API to play."""
    
    def __init__(self, role, game_state):
        self.role = role
        self.game_state = game_state
        self.conversation_history = []
    
    def ask_question(self):
        """Player 2 asks a yes/no question using the LLM."""
        if self.role == PLAYER2:
            prompt = "You are playing Twenty Questions. Ask a strategic yes/no question to guess the object. Only ask the question, nothing else."
            
            if self.conversation_history:
                prompt += f"\n\nPrevious questions and answers:\n"
                for qa in self.conversation_history:
                    prompt += f"Q: {qa['question']}\nA: {qa['answer']}\n"
            
            messages = [{"role": "user", "content": prompt}]
            question = call_llm(messages)
            return question.strip()
        return None
    
    def make_guess(self):
        """Player 2 makes a guess using the LLM."""
        if self.role == PLAYER2:
            prompt = "You are playing Twenty Questions. Based on the questions and answers, make your guess for the object. Only state the object name, nothing else."
            
            if self.conversation_history:
                prompt += f"\n\nPrevious questions and answers:\n"
                for qa in self.conversation_history:
                    prompt += f"Q: {qa['question']}\nA: {qa['answer']}\n"
            
            messages = [{"role": "user", "content": prompt}]
            guess = call_llm(messages)
            return guess.strip()
        return None
    
    def decide_action(self):
        """Decide whether to ask a question or make a guess."""
        if self.role == PLAYER2:
            remaining = 20 - self.game_state.question_count
            
            if remaining <= 2:
                return "guess"
            
            prompt = f"""You are playing Twenty Questions. You have {remaining} questions remaining.

Based on the information you have gathered, decide:
- If you are confident about the answer, respond with: guess
- If you need more information, respond with: question

IMPORTANT: Respond with ONLY the single word "guess" or "question", nothing else."""

            if self.conversation_history:
                prompt += f"\n\nPrevious questions and answers:\n"
                for qa in self.conversation_history:
                    prompt += f"Q: {qa['question']}\nA: {qa['answer']}\n"
            
            messages = [{"role": "user", "content": prompt}]
            decision = call_llm(messages).strip().lower()
            
            if decision.startswith("guess") or decision == "g":
                return "guess"
            return "question"
        return None


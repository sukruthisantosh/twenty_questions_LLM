"""Human player implementation."""
from ..core.player import Player
from ..constants import PLAYER1, PLAYER2


class HumanPlayer(Player):
    """Human player that gets input from user."""
    
    def __init__(self, role, game_state):
        super().__init__(role, game_state)
    
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
    
    def decide_action(self):
        """Player 2 decides whether to ask a question or make a guess."""
        if self.role == PLAYER2:
            action = input("Ask a question (q) or make a guess (g)? ").strip().lower()
            if action == "g":
                return "guess"
            return "question"
        return None


"""Player implementations for Twenty Questions."""
from game_state import GameState

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


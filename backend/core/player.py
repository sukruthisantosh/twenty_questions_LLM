"""Base player class."""
from abc import ABC, abstractmethod


class Player(ABC):
    """Base class for all players."""
    
    def __init__(self, role, game_state):
        self.role = role
        self.game_state = game_state
    
    @abstractmethod
    def set_object(self):
        """Player 1 sets the object they're thinking of."""
        pass
    
    @abstractmethod
    def answer_question(self, question):
        """Player 1 answers a yes/no question."""
        pass
    
    @abstractmethod
    def ask_question(self):
        """Player 2 asks a yes/no question."""
        pass
    
    @abstractmethod
    def make_guess(self):
        """Player 2 makes a guess."""
        pass
    
    @abstractmethod
    def decide_action(self):
        """Player 2 decides whether to ask a question or make a guess."""
        pass
    
    def record_interaction(self, question, answer):
        """Record a question-answer interaction. Override if needed."""
        pass


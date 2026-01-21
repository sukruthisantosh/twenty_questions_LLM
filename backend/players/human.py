"""Human player implementation."""
from ..core.player import Player


class HumanPlayer(Player):
    """Placeholder for human players in web API.
    
    Note: In the web API, human input comes from HTTP requests via handlers.
    These methods are stubs to satisfy the Player interface but are never called.
    """
    
    def set_object(self):
        return None
    
    def answer_question(self, question):
        return None
    
    def ask_question(self):
        return None
    
    def make_guess(self):
        return None
    
    def decide_action(self):
        return None


"""Game session management."""
from typing import Dict, Optional
from .core import GameState
from .players import HumanPlayer, LLMPlayer
from .constants import PLAYER1, PLAYER2


class GameManager:
    """Manages a single game session."""
    
    def __init__(self):
        self.game: Optional[Dict] = None
    
    def create_game(self, player1_type: str, player2_type: str) -> None:
        """Create a new game session."""
        player_classes = {
            "human": HumanPlayer,
            "llm": LLMPlayer
        }
        
        p1_class = player_classes.get(player1_type.lower(), LLMPlayer)
        p2_class = player_classes.get(player2_type.lower(), HumanPlayer)
        
        game_state = GameState()
        player1 = p1_class(PLAYER1, game_state)
        player2 = p2_class(PLAYER2, game_state)
        
        self.game = {
            "game_state": game_state,
            "player1": player1,
            "player2": player2,
            "player1_type": player1_type,
            "player2_type": player2_type,
            "pending_question": None
        }
    
    def get_game(self) -> Optional[Dict]:
        """Get current game session."""
        return self.game


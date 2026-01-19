"""Game session management."""
from typing import Dict, Optional
from .core import GameState
from .players import HumanPlayer, LLMPlayer
from .constants import PLAYER1, PLAYER2


class GameManager:
    """Manages game sessions and player actions."""
    
    def __init__(self):
        """Initialize game manager."""
        self.games: Dict[str, Dict] = {}
    
    def create_game(self, player1_type: str, player2_type: str) -> str:
        """Create a new game session.
        
        Args:
            player1_type: "human" or "llm"
            player2_type: "human" or "llm"
        
        Returns:
            game_id: Unique game identifier
        """
        import uuid
        game_id = str(uuid.uuid4())
        
        player_classes = {
            "human": HumanPlayer,
            "llm": LLMPlayer
        }
        
        p1_class = player_classes.get(player1_type.lower(), LLMPlayer)
        p2_class = player_classes.get(player2_type.lower(), HumanPlayer)
        
        game_state = GameState()
        player1 = p1_class(PLAYER1, game_state)
        player2 = p2_class(PLAYER2, game_state)
        
        self.games[game_id] = {
            "game_state": game_state,
            "player1": player1,
            "player2": player2,
            "player1_type": player1_type,
            "player2_type": player2_type,
            "pending_question": None
        }
        
        return game_id
    
    def get_game(self, game_id: str) -> Optional[Dict]:
        """Get game session by ID.
        
        Args:
            game_id: Game identifier
        
        Returns:
            Game dict or None if not found
        """
        return self.games.get(game_id)
    
    def delete_game(self, game_id: str) -> bool:
        """Delete a game session.
        
        Args:
            game_id: Game identifier
        
        Returns:
            True if deleted, False if not found
        """
        if game_id in self.games:
            del self.games[game_id]
            return True
        return False


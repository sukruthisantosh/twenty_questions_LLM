"""Game state management for Twenty Questions."""
MAX_QUESTIONS = 20
PLAYING = "playing"
WON = "won"
LOST = "lost"


class GameState:
    """Tracks the state of a Twenty Questions game."""
    
    def __init__(self):
        self.question_count = 0
        self.status = PLAYING
        self.object = None
    
    def increment_question(self):
        """Increment question count and check win/loss conditions."""
        self.question_count += 1
        if self.question_count >= MAX_QUESTIONS:
            self.status = LOST
    
    def set_object(self, obj):
        """Set the object Player 1 is thinking of."""
        self.object = obj
    
    def win(self):
        """Mark the game as won."""
        self.status = WON
    
    def is_playing(self):
        """Check if game is still in progress."""
        return self.status == PLAYING


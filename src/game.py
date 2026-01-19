"""Game loop for Twenty Questions."""
from .core import GameState, MAX_QUESTIONS
from .players import HumanPlayer, LLMPlayer
from .constants import PLAYER1, PLAYER2


def play_game(player1_type=LLMPlayer, player2_type=HumanPlayer):
    """Run a game of Twenty Questions.
    
    Args:
        player1_type: Player class for Player 1 (default: LLMPlayer)
        player2_type: Player class for Player 2 (default: HumanPlayer)
    """
    game_state = GameState()
    player1 = player1_type(PLAYER1, game_state)
    player2 = player2_type(PLAYER2, game_state)
    
    print("=== Twenty Questions ===")
    print("Player 1 is thinking of an object...")
    obj = player1.set_object()
    if obj:
        print(f"Player 1 has chosen an object. Let's play!\n")
    
    while game_state.is_playing():
        print(f"Question {game_state.question_count + 1}/{MAX_QUESTIONS}")
        
        action = player2.decide_action()
        
        if action == "guess":
            guess = player2.make_guess()
            if guess:
                print(f"Player 2 guesses: {guess}")
            game_state.increment_question()
            
            if guess and guess.lower() == game_state.object.lower():
                game_state.win()
                print(f"\nCorrect! Player 2 wins! The object was {game_state.object}.")
            else:
                print("Wrong guess!")
                if not game_state.is_playing():
                    print(f"\nPlayer 1 wins! The object was {game_state.object}.")
        
        else:
            question = player2.ask_question()
            if question:
                print(f"Player 2 asks: {question}")
                answer = player1.answer_question(question)
                if answer:
                    game_state.increment_question()
                    
                    player2.record_interaction(question, answer)
                    
                    print(f"Player 1 answers: {answer}\n")
                    
                    if not game_state.is_playing():
                        print(f"\nPlayer 1 wins! The object was {game_state.object}.")
                else:
                    print("Error: Player 1 could not answer the question.")


if __name__ == "__main__":
    play_game(LLMPlayer, LLMPlayer)


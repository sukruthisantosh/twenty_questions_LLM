"""Game loop for Twenty Questions."""
from game_state import GameState, MAX_QUESTIONS
from players import HumanPlayer, PLAYER1, PLAYER2


def play_game():
    """Run a game of Twenty Questions."""
    game_state = GameState()
    player1 = HumanPlayer(PLAYER1, game_state)
    player2 = HumanPlayer(PLAYER2, game_state)
    
    print("=== Twenty Questions ===")
    print("Player 1, think of an object...")
    player1.set_object()
    print("\nPlayer 2, start asking questions!\n")
    
    while game_state.is_playing():
        print(f"Question {game_state.question_count + 1}/{MAX_QUESTIONS}")
        
        action = input("Ask a question (q) or make a guess (g)? ").strip().lower()
        
        if action == "g":
            guess = player2.make_guess()
            game_state.increment_question()
            
            if guess.lower() == game_state.object.lower():
                game_state.win()
                print(f"\nCorrect! Player 2 wins! The object was {game_state.object}.")
            else:
                print("Wrong guess!")
                if not game_state.is_playing():
                    print(f"\nPlayer 1 wins! The object was {game_state.object}.")
        
        elif action == "q":
            question = player2.ask_question()
            answer = player1.answer_question(question)
            game_state.increment_question()
            print(f"Answer: {answer}\n")
            
            if not game_state.is_playing():
                print(f"\nPlayer 1 wins! The object was {game_state.object}.")
        
        else:
            print("Please enter 'q' for question or 'g' for guess.")


if __name__ == "__main__":
    play_game()


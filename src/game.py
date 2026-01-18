"""Game loop for Twenty Questions."""
from game_state import GameState, MAX_QUESTIONS
from players import HumanPlayer, LLMPlayer, PLAYER1, PLAYER2


def play_game():
    """Run a game of Twenty Questions."""
    game_state = GameState()
    player1 = HumanPlayer(PLAYER1, game_state)
    player2 = LLMPlayer(PLAYER2, game_state)
    
    print("=== Twenty Questions ===")
    print("Player 1, think of an object...")
    player1.set_object()
    print("\nLLM Player 2 will ask questions!\n")
    
    while game_state.is_playing():
        print(f"Question {game_state.question_count + 1}/{MAX_QUESTIONS}")
        
        action = player2.decide_action()
        
        if action == "guess":
            guess = player2.make_guess()
            if guess:
                print(f"LLM guesses: {guess}")
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
                print(f"LLM asks: {question}")
                answer = player1.answer_question(question)
                game_state.increment_question()
                
                player2.conversation_history.append({
                    "question": question,
                    "answer": answer
                })
                
                print(f"Answer: {answer}\n")
                
                if not game_state.is_playing():
                    print(f"\nPlayer 1 wins! The object was {game_state.object}.")


if __name__ == "__main__":
    play_game()


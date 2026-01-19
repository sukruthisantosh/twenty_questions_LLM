"""Main entry point for Twenty Questions game."""
from src.game import play_game
from src.players import HumanPlayer, LLMPlayer

GAME_MODES = {
    "1": {
        "name": "Human vs LLM",
        "description": "You think of an object, LLM asks questions",
        "players": (HumanPlayer, LLMPlayer)
    },
    "2": {
        "name": "LLM vs Human",
        "description": "LLM thinks of an object, you ask questions",
        "players": (LLMPlayer, HumanPlayer)
    },
    "3": {
        "name": "LLM vs LLM",
        "description": "Watch two LLMs play against each other",
        "players": (LLMPlayer, LLMPlayer)
    }
}


def print_menu():
    """Display game mode selection menu."""
    print("\n" + "=" * 50)
    print("Twenty Questions - Game Mode Selection")
    print("=" * 50)
    for key, mode in GAME_MODES.items():
        print(f"{key}. {mode['name']} ({mode['description']})")
    print("0. Exit")
    print("=" * 50)


def get_choice(prompt, valid_choices):
    """Get validated user input."""
    while True:
        try:
            choice = input(f"\n{prompt}: ").strip()
            if choice in valid_choices:
                return choice
            print(f"Invalid choice. Please enter one of: {', '.join(valid_choices)}")
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting...")
            return "0"


def main():
    """Main entry point with mode selection."""
    while True:
        print_menu()
        choice = get_choice("Select a game mode", ["0"] + list(GAME_MODES.keys()))
        
        if choice == "0":
            print("Thanks for playing!")
            break
        
        mode = GAME_MODES[choice]
        print(f"\nStarting: {mode['name']}")
        print(f"{mode['description']}\n")
        play_game(*mode["players"])
        
        play_again = get_choice("Play again? (y/n)", ["y", "yes", "n", "no"])
        if play_again in ["n", "no"]:
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()


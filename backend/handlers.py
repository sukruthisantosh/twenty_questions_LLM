"""Request handlers for game actions."""
from typing import Dict
from fastapi import HTTPException
from .core import GameState, MAX_QUESTIONS


def handle_set_object(game: Dict, content: str) -> Dict:
    """Handle setting object when Player 1 is human."""
    if game["player1_type"] != "human":
        raise HTTPException(status_code=400, detail="Only human Player 1 can set object")
    
    game["game_state"].set_object(content)
    return {
        "status": "playing",
        "question_count": game["game_state"].question_count,
        "max_questions": MAX_QUESTIONS,
        "player1_type": game["player1_type"],
        "player2_type": game["player2_type"]
    }


def handle_answer_question(game: Dict, content: str) -> Dict:
    """Handle Player 1 answering a question."""
    if not game.get("pending_question"):
        raise HTTPException(status_code=400, detail="No pending question")
    
    answer = content.lower()
    if answer not in ["yes", "no", "y", "n"]:
        raise HTTPException(status_code=400, detail="Answer must be yes/no")
    
    answer = "yes" if answer in ["yes", "y"] else "no"
    question = game["pending_question"]
    game["pending_question"] = None
    
    gs = game["game_state"]
    gs.increment_question()
    game["player2"].record_interaction(question, answer)
    
    return {
        "status": "question_answered",
        "question": question,
        "answer": answer,
        "question_count": gs.question_count,
        "game_status": gs.status,
        "game_over": not gs.is_playing(),
        "object": gs.object if not gs.is_playing() else None,
        "winner": "Player 1" if not gs.is_playing() else None
    }


def handle_ask_question(game: Dict, content: str) -> Dict:
    """Handle Player 2 asking a question."""
    if game["player2_type"] != "human":
        raise HTTPException(status_code=400, detail="Only human Player 2 can ask questions")
    
    if not content:
        raise HTTPException(status_code=400, detail="Question required")
    
    question = content
    gs = game["game_state"]
    
    # Player 1 answers
    if game["player1_type"] == "llm":
        answer = game["player1"].answer_question(question)
        gs.increment_question()
        game["player2"].record_interaction(question, answer)
        
        return {
            "status": "question_answered",
            "question": question,
            "answer": answer,
            "question_count": gs.question_count,
            "game_status": gs.status,
            "game_over": not gs.is_playing(),
            "object": gs.object if not gs.is_playing() else None,
            "winner": "Player 1" if not gs.is_playing() else None
        }
    else:
        # Human Player 1 - wait for answer
        game["pending_question"] = question
        return {
            "status": "waiting_for_answer",
            "question": question,
            "question_count": gs.question_count
        }


def handle_make_guess(game: Dict, content: str) -> Dict:
    """Handle Player 2 making a guess."""
    if game["player2_type"] != "human":
        raise HTTPException(status_code=400, detail="Only human Player 2 can make guesses")
    
    if not content:
        raise HTTPException(status_code=400, detail="Guess required")
    
    guess = content
    gs = game["game_state"]
    gs.increment_question()
    
    if guess.lower() == gs.object.lower():
        gs.win()
        return {
            "status": "game_over",
            "guess": guess,
            "correct": True,
            "object": gs.object,
            "question_count": gs.question_count,
            "winner": "Player 2"
        }
    else:
        # Wrong guess - game continues if questions remain
        if gs.is_playing():
            return {
                "status": "waiting_for_question",
                "guess": guess,
                "correct": False,
                "question_count": gs.question_count,
                "message": "Wrong guess! You can ask another question or make another guess."
            }
        else:
            # Game over - no questions left
            return {
                "status": "game_over",
                "guess": guess,
                "correct": False,
                "object": gs.object,
                "question_count": gs.question_count,
                "winner": "Player 1"
            }


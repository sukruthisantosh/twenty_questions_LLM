"""REST API for Twenty Questions game."""
from typing import Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .core import GameState, MAX_QUESTIONS
from .game_manager import GameManager
from .handlers import handle_set_object, handle_answer_question, handle_ask_question, handle_make_guess

app = FastAPI(title="Twenty Questions Game API")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Game manager instance
game_manager = GameManager()


@app.post("/api/games")
async def create_game(data: Dict):
    """Create a new game."""
    player1_type = data.get("player1_type", "llm")
    player2_type = data.get("player2_type", "human")
    
    game_id = game_manager.create_game(player1_type, player2_type)
    game = game_manager.get_game(game_id)
    game_state = game["game_state"]
    player1 = game["player1"]
    
    # Player 1 sets object
    if player1_type == "llm":
        obj = player1.set_object()
        if obj:
            game_state.set_object(obj)
            status = "playing" if player2_type == "llm" else "waiting_for_question"
            return {
                "game_id": game_id,
                "status": status,
                "question_count": game_state.question_count
            }
        raise HTTPException(status_code=500, detail="Failed to set object")
    
    return {
        "game_id": game_id,
        "status": "waiting_for_object",
        "message": "Please set the object"
    }


@app.post("/api/games/{game_id}/object")
async def set_object(game_id: str, data: Dict):
    """Set object when Player 1 is human."""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    obj = data.get("object", "").strip()
    if not obj:
        raise HTTPException(status_code=400, detail="Object required")
    
    game["game_state"].set_object(obj)
    
    return {
        "status": "playing",
        "question_count": game["game_state"].question_count
    }


@app.get("/api/games/{game_id}/next")
async def get_next_action(game_id: str):
    """Get the next action."""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    gs = game["game_state"]
    
    if not gs.is_playing():
        return {
            "status": "game_over",
            "game_status": gs.status,
            "object": gs.object,
            "question_count": gs.question_count,
            "winner": "Player 2" if gs.status == "won" else "Player 1"
        }
    
    if game.get("pending_question"):
        return {
            "status": "waiting_for_answer",
            "question": game["pending_question"],
            "question_count": gs.question_count
        }
    
    if game["player2_type"] == "llm":
        action = game["player2"].decide_action()
    else:
        return {
            "status": "waiting_for_decision",
            "question_count": gs.question_count
        }
    
    if action == "guess":
        guess = game["player2"].make_guess()
        if guess:
            gs.increment_question()
            if guess.lower() == gs.object.lower():
                gs.win()
                return {
                    "status": "game_over",
                    "action": "guess",
                    "guess": guess,
                    "correct": True,
                    "object": gs.object,
                    "question_count": gs.question_count,
                    "winner": "Player 2"
                }
            else:
                # Wrong guess - game continues if questions remain
                if gs.is_playing():
                    # Game continues - LLM will decide next action
                    return {
                        "status": "guess_incorrect",
                        "action": "guess",
                        "guess": guess,
                        "correct": False,
                        "question_count": gs.question_count
                    }
                else:
                    # Game over - no questions left
                    return {
                        "status": "game_over",
                        "action": "guess",
                        "guess": guess,
                        "correct": False,
                        "object": gs.object,
                        "question_count": gs.question_count,
                        "winner": "Player 1"
                    }
    else:
        # Ask a question (only for LLM Player 2)
        if game["player2_type"] != "llm":
            return {
                "status": "waiting_for_question",
                "question_count": gs.question_count
            }
        
        question = game["player2"].ask_question()
        if question:
            # Player 1 answers
            if game["player1_type"] == "llm":
                answer = game["player1"].answer_question(question)
                gs.increment_question()
                game["player2"].record_interaction(question, answer)
                
                return {
                    "status": "question_answered",
                    "action": "question",
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
    
    return {"status": "error", "message": "Unable to determine next action"}


@app.post("/api/games/{game_id}/action")
async def submit_action(game_id: str, data: Dict):
    """Submit human player action."""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    gs = game["game_state"]
    
    if not gs.is_playing():
        raise HTTPException(status_code=400, detail="Game is not in progress")
    
    action_type = data.get("action_type")
    content = data.get("content", "").strip()
    
    handlers = {
        "set_object": handle_set_object,
        "answer_question": handle_answer_question,
        "ask_question": handle_ask_question,
        "make_guess": handle_make_guess
    }
    
    handler = handlers.get(action_type)
    if not handler:
        raise HTTPException(status_code=400, detail="Invalid action type")
    
    return handler(game, content)


@app.get("/api/games/{game_id}")
async def get_game_state(game_id: str):
    """Get current game state."""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    gs = game["game_state"]
    
    return {
        "status": "playing" if gs.is_playing() else "game_over",
        "game_status": gs.status,
        "question_count": gs.question_count,
        "max_questions": MAX_QUESTIONS,
        "object": gs.object if not gs.is_playing() else None,
        "player1_type": game["player1_type"],
        "player2_type": game["player2_type"],
        "pending_question": game.get("pending_question")
    }


@app.get("/")
async def root():
    """Health check."""
    return {"status": "ok", "message": "Twenty Questions Game API"}

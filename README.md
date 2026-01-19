# Twenty Questions Game

A simple implementation of the Twenty Questions game with LLM integration.

## Setup

### Backend

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API key:
```
CANDIDATE_API_KEY=your_api_key_here
```

3. Run the API server:
```bash
python run_api.py
```

The API will be available at `http://localhost:8000`

### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Game Modes

- **Human vs LLM**: You think of an object, LLM asks questions
- **LLM vs Human**: LLM thinks of an object, you ask questions
- **LLM vs LLM**: Watch two LLMs play against each other

## API Endpoints

- `POST /api/games` - Create a new game
- `GET /api/games/{game_id}` - Get game state
- `GET /api/games/{game_id}/next` - Get next action (for LLM players)
- `POST /api/games/{game_id}/action` - Submit human player action
- `POST /api/games/{game_id}/object` - Set object (when Player 1 is human)


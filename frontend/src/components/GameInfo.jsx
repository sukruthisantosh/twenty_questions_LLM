/** Game info component displaying game state. */
export default function GameInfo({ gameState, mode }) {
    return (
        <div className="game-info">
            <p><strong>Mode:</strong> {mode.player1} vs {mode.player2}</p>
            <p><strong>Questions:</strong> {gameState.question_count || 0} / {gameState.max_questions || 20}</p>
            {gameState.game_status && <p><strong>Status:</strong> {gameState.game_status}</p>}
            {gameState.winner && <p><strong>Winner:</strong> {gameState.winner}</p>}
            {gameState.object && <p><strong>Object:</strong> {gameState.object}</p>}
        </div>
    )
}


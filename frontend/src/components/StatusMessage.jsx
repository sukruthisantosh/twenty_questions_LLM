/** Status message component for displaying game state messages. */
export default function StatusMessage({ status, gameState, mode }) {
    if (status === 'waiting_for_object') {
        return (
            <div className="status-message">
                <p>What object are you thinking of?</p>
            </div>
        )
    }

    if (status === 'waiting_for_answer') {
        const question = gameState.pending_question || gameState.question
        if (question) {
            return (
                <div className="status-message">
                    <p><strong>Question:</strong> {question}</p>
                    <p>Answer yes or no:</p>
                </div>
            )
        }
    }

    if (status === 'waiting_for_question') {
        // Check if this is after an incorrect guess
        if (gameState.guess && gameState.correct === false) {
            return (
                <div className="status-message warning">
                    <p><strong>Incorrect guess: "{gameState.guess}"</strong></p>
                    <p>You can ask another question or make another guess.</p>
                    {gameState.max_questions && gameState.question_count && (
                        <p>Questions remaining: {gameState.max_questions - gameState.question_count}</p>
                    )}
                </div>
            )
        }
        return (
            <div className="status-message">
                <p>Ask a yes/no question:</p>
            </div>
        )
    }

    if (status === 'waiting_for_guess') {
        return (
            <div className="status-message">
                <p>Make your guess:</p>
            </div>
        )
    }


    if (status === 'question_answered' && gameState.question) {
        // If Player 2 is Human, show they can ask another question
        if (mode?.player2 === 'human' && !gameState.game_over) {
            return (
                <div className="status-message">
                    <p><strong>Q:</strong> {gameState.question}</p>
                    <p><strong>A:</strong> {gameState.answer}</p>
                    <p>Ask another question or make a guess:</p>
                </div>
            )
        }
        return (
            <div className="status-message">
                <p><strong>Q:</strong> {gameState.question}</p>
                <p><strong>A:</strong> {gameState.answer}</p>
            </div>
        )
    }

    if (status === 'guess_incorrect') {
        // Show clear message for human players
        if (mode?.player2 === 'human' && !gameState.game_over) {
            return (
                <div className="status-message warning">
                    <p><strong>Incorrect guess: "{gameState.guess}"</strong></p>
                    <p>You can ask another question or make another guess.</p>
                    <p>Questions remaining: {gameState.max_questions - gameState.question_count}</p>
                </div>
            )
        }
        // For LLM players or game over
        return (
            <div className="status-message warning">
                <p><strong>Wrong guess: {gameState.guess}</strong></p>
                {gameState.message && <p>{gameState.message}</p>}
            </div>
        )
    }

    if (status === 'game_over') {
        const humanWon = (gameState.winner === 'Player 1' && mode?.player1 === 'human') ||
            (gameState.winner === 'Player 2' && mode?.player2 === 'human')
        const bothLLMs = mode?.player1 === 'llm' && mode?.player2 === 'llm'

        return (
            <div className="status-message">
                {humanWon ? (
                    <p><strong>You win!</strong></p>
                ) : (
                    <p><strong>Game Finished!</strong></p>
                )}
                {gameState.winner && <p>Winner: {gameState.winner}</p>}
                {gameState.object && <p>The object was: {gameState.object}</p>}
            </div>
        )
    }

    return null
}


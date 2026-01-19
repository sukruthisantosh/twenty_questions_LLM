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

    if (status === 'waiting_for_decision') {
        return (
            <div className="status-message">
                <p>Ask a question or make a guess (type 'g' for guess, or type your question):</p>
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
        return (
            <div className="status-message warning">
                <p>Wrong guess: {gameState.guess}</p>
                {gameState.message && <p>{gameState.message}</p>}
            </div>
        )
    }

    if (status === 'game_over') {
        // Determine if human player won
        const humanWon =
            (gameState.winner === 'Player 1' && mode?.player1 === 'human') ||
            (gameState.winner === 'Player 2' && mode?.player2 === 'human')

        // If both players are LLMs, show "Game Finished!"
        const bothLLMs = mode?.player1 === 'llm' && mode?.player2 === 'llm'

        return (
            <div className="status-message">
                {humanWon ? (
                    <p><strong>You win!</strong></p>
                ) : bothLLMs ? (
                    <p><strong>Game Finished!</strong></p>
                ) : (
                    <p><strong>Game Over!</strong></p>
                )}
                {bothLLMs && gameState.winner && <p>Winner: {gameState.winner}</p>}
                {gameState.object && <p>The object was: {gameState.object}</p>}
            </div>
        )
    }

    return null
}


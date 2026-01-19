/** Mode selector component for choosing game mode. */
export default function ModeSelector({ onCreateGame }) {
    return (
        <div className="game-container">
            <h1>Twenty Questions</h1>
            <div className="mode-selector">
                <button className="mode-button" onClick={() => onCreateGame('human', 'llm')}>
                    Human vs LLM (You think, LLM asks)
                </button>
                <button className="mode-button" onClick={() => onCreateGame('llm', 'human')}>
                    LLM vs Human (LLM thinks, you ask)
                </button>
                <button className="mode-button" onClick={() => onCreateGame('llm', 'llm')}>
                    LLM vs LLM (Watch two LLMs play)
                </button>
            </div>
        </div>
    )
}


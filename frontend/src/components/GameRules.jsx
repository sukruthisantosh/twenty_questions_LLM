/** Game rules component displaying instructions for human players. */
export default function GameRules({ mode }) {
    if (!mode) return null

    const isPlayer1Human = mode.player1 === 'human'
    const isPlayer2Human = mode.player2 === 'human'

    if (!isPlayer1Human && !isPlayer2Human) {
        // Both LLMs, no rules needed
        return null
    }

    return (
        <div className="game-rules" style={{
            backgroundColor: '#f8f9fa',
            border: '1px solid #dee2e6',
            borderRadius: '8px',
            padding: '15px',
            marginBottom: '20px',
            fontSize: '0.9em'
        }}>
            <h3 style={{ marginTop: 0, marginBottom: '10px', fontSize: '1.1em' }}>Rules & Instructions</h3>

            {isPlayer2Human && (
                <div style={{ marginBottom: '10px' }}>
                    <p style={{ margin: '5px 0', fontWeight: 'bold' }}>As Player 2 (Asking Questions):</p>
                    <ul style={{ margin: '5px 0', paddingLeft: '20px' }}>
                        <li>You can only ask questions that can be answered with <strong>"yes"</strong> or <strong>"no"</strong></li>
                        <li>When making a guess, enter <strong>only the object name</strong> (1-2 words max, e.g., "apple" or "ice cream")</li>
                        <li>You have up to 20 questions/guesses to find the object</li>
                    </ul>
                </div>
            )}

            {isPlayer1Human && (
                <div>
                    <p style={{ margin: '5px 0', fontWeight: 'bold' }}>As Player 1 (Answering Questions):</p>
                    <ul style={{ margin: '5px 0', paddingLeft: '20px' }}>
                        <li>You must answer truthfully with only <strong>"yes"</strong> or <strong>"no"</strong></li>
                        <li>When setting the object, enter <strong>only the object name</strong> (1-2 words max)</li>
                    </ul>
                </div>
            )}
        </div>
    )
}

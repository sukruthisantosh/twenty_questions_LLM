/** Input form component for user actions. */
export default function InputForm({
    status,
    inputValue,
    setInputValue,
    onSubmit,
    loading,
    mode,
    gameState,
    actionMode,
    setActionMode
}) {
    const needsInput =
        status === 'waiting_for_object' ||
        status === 'waiting_for_answer' ||
        status === 'waiting_for_question' ||
        status === 'waiting_for_decision' ||
        status === 'waiting_for_guess' ||
        (status === 'question_answered' && !gameState?.game_over && mode?.player2 === 'human') ||
        // Allow input after wrong guess if Player 2 is Human and game continues
        (status === 'guess_incorrect' && !gameState?.game_over && mode?.player2 === 'human')

    if (!needsInput) return null

    const canChooseAction = (status === 'waiting_for_question' ||
        status === 'waiting_for_decision' ||
        (status === 'question_answered' && mode?.player2 === 'human' && !gameState?.game_over) ||
        (status === 'guess_incorrect' && mode?.player2 === 'human' && !gameState?.game_over))

    const getPlaceholder = () => {
        if (status === 'waiting_for_object') return 'Enter object...'
        if (status === 'waiting_for_answer') return 'yes/no'
        if (status === 'waiting_for_guess') return 'Enter guess...'
        if (canChooseAction) {
            return actionMode === 'guess' ? 'Enter your guess...' : 'Enter question...'
        }
        return 'Enter question...'
    }

    const handleChange = (e) => {
        const value = e.target.value
        setInputValue(value)
    }

    return (
        <form onSubmit={onSubmit}>
            {canChooseAction && (
                <div style={{ marginBottom: '10px', display: 'flex', gap: '10px' }}>
                    <button
                        type="button"
                        onClick={() => setActionMode('question')}
                        style={{
                            padding: '8px 16px',
                            backgroundColor: actionMode === 'question' ? '#007bff' : '#e9ecef',
                            color: actionMode === 'question' ? 'white' : '#333',
                            border: 'none',
                            borderRadius: '5px',
                            cursor: 'pointer'
                        }}
                    >
                        Ask Question
                    </button>
                    <button
                        type="button"
                        onClick={() => setActionMode('guess')}
                        style={{
                            padding: '8px 16px',
                            backgroundColor: actionMode === 'guess' ? '#007bff' : '#e9ecef',
                            color: actionMode === 'guess' ? 'white' : '#333',
                            border: 'none',
                            borderRadius: '5px',
                            cursor: 'pointer'
                        }}
                    >
                        Make Guess
                    </button>
                </div>
            )}
            <input
                type="text"
                value={inputValue}
                onChange={handleChange}
                placeholder={getPlaceholder()}
                disabled={loading}
            />
            <button type="submit" disabled={loading || !inputValue.trim()}>
                {loading ? 'Loading...' : 'Submit'}
            </button>
        </form>
    )
}


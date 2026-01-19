import { useState, useEffect } from 'react'
import './index.css'
import ModeSelector from './components/ModeSelector'
import GameInfo from './components/GameInfo'
import StatusMessage from './components/StatusMessage'
import QuestionHistory from './components/QuestionHistory'
import InputForm from './components/InputForm'

const API_BASE = '/api'

function App() {
    const [mode, setMode] = useState(null)
    const [gameId, setGameId] = useState(null)
    const [gameState, setGameState] = useState(null)
    const [questionHistory, setQuestionHistory] = useState([])
    const [inputValue, setInputValue] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [actionMode, setActionMode] = useState('question') // 'question' or 'guess'

    const createGame = async (player1Type, player2Type) => {
        setLoading(true)
        setError(null)
        try {
            const response = await fetch(`${API_BASE}/games`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player1_type: player1Type,
                    player2_type: player2Type
                })
            })
            const data = await response.json()
            setGameId(data.game_id)
            setGameState(data)
            setMode({ player1: player1Type, player2: player2Type })

            // If game is ready, get the next action
            if (data.status === 'playing' && player2Type === 'llm') {
                // For LLM Player 2, auto-advance
                setTimeout(getNextAction, 1000)
            }
            // For Human Player 2, status should already be "waiting_for_question" from API
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const getNextAction = async () => {
        if (!gameId) return

        setLoading(true)
        setError(null)
        try {
            const response = await fetch(`${API_BASE}/games/${gameId}/next`)
            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || 'Failed to get next action')
            }
            const data = await response.json()
            setGameState(data)

            // Update question history (only if both question and answer exist)
            if (data.question && data.answer) {
                setQuestionHistory(prev => [...prev, { question: data.question, answer: data.answer }])
            }

            // If guess was made, add to history
            if (data.guess) {
                setQuestionHistory(prev => [...prev, {
                    question: `Guess: ${data.guess}`,
                    answer: data.correct ? 'Correct!' : 'Wrong'
                }])
            }
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const submitAction = async (actionType, content) => {
        if (!gameId) return

        setLoading(true)
        setError(null)
        try {
            const response = await fetch(`${API_BASE}/games/${gameId}/action`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    action_type: actionType,
                    content: content
                })
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || 'Action failed')
            }

            const data = await response.json()
            setGameState(data)

            // Update question history
            if (data.question && data.answer) {
                setQuestionHistory(prev => [...prev, { question: data.question, answer: data.answer }])
            }

            // Add wrong guess to history
            if (data.guess && !data.correct) {
                setQuestionHistory(prev => [...prev, {
                    question: `Guess: ${data.guess}`,
                    answer: 'Wrong'
                }])
            }

            setInputValue('')

            // If game continues and LLM needs to act, get next action
            if (data.status === 'question_answered' && !data.game_over && mode?.player2 === 'llm') {
                setTimeout(getNextAction, 500)
            }
            // If object was just set and Player 2 is LLM, start the game
            else if (data.status === 'playing' && mode?.player2 === 'llm' && actionType === 'set_object') {
                setTimeout(getNextAction, 500)
            }
            // If question was answered and Player 2 is Human, keep status as 'question_answered' 
            // but allow them to ask another question (handled in needsInput check)
            // Reset action mode to question after each action
            if (actionType === 'ask_question' || actionType === 'make_guess') {
                setActionMode('question')
            }
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const validateAnswer = (answer) => {
        const normalized = answer.trim().toLowerCase()
        return ['yes', 'no', 'y', 'n'].includes(normalized)
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        if (!inputValue.trim()) return

        const status = gameState?.status
        const value = inputValue.trim()

        // Validate answer before submitting
        if (status === 'waiting_for_answer') {
            if (!validateAnswer(value)) {
                setError('Please answer with "yes" or "no"')
                return
            }
            submitAction('answer_question', value)
            return
        }

        if (status === 'waiting_for_object') {
            submitAction('set_object', value)
        } else if (status === 'waiting_for_question' ||
            (status === 'question_answered' && mode?.player2 === 'human' && !gameState.game_over) ||
            (status === 'guess_incorrect' && mode?.player2 === 'human' && !gameState.game_over)) {
            // Check if user typed "guess:" or "g:" prefix
            const lowerValue = value.toLowerCase().trim()
            if (lowerValue.startsWith('guess:') || lowerValue.startsWith('g:')) {
                const guess = value.split(':').slice(1).join(':').trim()
                if (guess) {
                    submitAction('make_guess', guess)
                } else {
                    setError('Please enter a guess after "guess:"')
                }
            } else if (actionMode === 'guess') {
                submitAction('make_guess', value)
            } else {
                submitAction('ask_question', value)
            }
        } else if (status === 'waiting_for_guess') {
            submitAction('make_guess', value)
        } else if (status === 'waiting_for_decision') {
            // If user types 'g' or 'guess', they want to guess
            const lowerValue = value.toLowerCase()
            if (lowerValue === 'g' || lowerValue === 'guess') {
                // Prompt for guess
                setGameState({ ...gameState, status: 'waiting_for_guess' })
                setInputValue('')
            } else {
                // Otherwise, treat as question
                submitAction('ask_question', value)
            }
        }
    }

    const resetGame = () => {
        setMode(null)
        setGameId(null)
        setGameState(null)
        setQuestionHistory([])
        setInputValue('')
        setError(null)
    }

    // Auto-advance for LLM players
    useEffect(() => {
        if (!gameId || !gameState || loading) return

        const status = gameState.status

        // Continue game if:
        // 1. Game is still playing (not over)
        // 2. Player 2 is LLM (needs to act)
        // 3. Status indicates we should continue (playing, question_answered, guess_incorrect)
        const shouldContinue =
            (status === 'playing' || status === 'question_answered' || status === 'guess_incorrect') &&
            status !== 'game_over' &&
            status !== 'waiting_for_object' &&
            status !== 'waiting_for_answer' &&
            status !== 'waiting_for_question' &&
            status !== 'waiting_for_guess' &&
            status !== 'waiting_for_decision' &&
            status !== 'error' &&
            !gameState.game_over &&
            mode?.player2 === 'llm'

        if (shouldContinue) {
            const timer = setTimeout(() => {
                getNextAction()
            }, 1500)
            return () => clearTimeout(timer)
        }
    }, [gameState, gameId, mode, loading])

    if (!mode) {
        return <ModeSelector onCreateGame={createGame} />
    }

    if (!gameState) {
        return <div className="game-container">Loading...</div>
    }

    const status = gameState.status
    const needsInput =
        status === 'waiting_for_object' ||
        status === 'waiting_for_answer' ||
        status === 'waiting_for_question' ||
        status === 'waiting_for_guess' ||
        status === 'waiting_for_decision' ||
        // Allow input if question was answered and Player 2 is Human (can ask another question)
        (status === 'question_answered' && !gameState.game_over && mode?.player2 === 'human') ||
        // Allow input after wrong guess if Player 2 is Human and game continues
        (status === 'guess_incorrect' && !gameState.game_over && mode?.player2 === 'human')

    return (
        <div className="game-container">
            <h1>Twenty Questions</h1>

            {error && <div className="status-message error">Error: {error}</div>}

            <GameInfo gameState={gameState} mode={mode} />
            <StatusMessage status={status} gameState={gameState} mode={mode} />

            <InputForm
                status={status}
                inputValue={inputValue}
                setInputValue={(value) => {
                    setInputValue(value)
                    // Clear error when user starts typing
                    if (error) setError(null)
                }}
                onSubmit={handleSubmit}
                loading={loading}
                mode={mode}
                gameState={gameState}
                actionMode={actionMode}
                setActionMode={setActionMode}
            />

            {status === 'game_over' && (
                <button onClick={resetGame}>New Game</button>
            )}

            {loading && status !== 'game_over' && !needsInput && (
                <div className="status-message">Processing...</div>
            )}

            <QuestionHistory questionHistory={questionHistory} />
        </div>
    )
}

export default App

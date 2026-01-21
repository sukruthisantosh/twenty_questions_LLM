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
    const [gameState, setGameState] = useState(null)
    const [questionHistory, setQuestionHistory] = useState([])
    const [inputValue, setInputValue] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [actionMode, setActionMode] = useState('question')

    const createGame = async (player1Type, player2Type) => {
        setLoading(true)
        setError(null)
        try {
            const response = await fetch(`${API_BASE}/game`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player1_type: player1Type,
                    player2_type: player2Type
                })
            })
            const data = await response.json()
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
        if (!gameState) return

        setLoading(true)
        setError(null)
        try {
            const response = await fetch(`${API_BASE}/game/next`)
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

            // If guess was made, add to history (for CLI-like output)
            if (data.guess) {
                setQuestionHistory(prev => [...prev, {
                    question: `Guess: ${data.guess}`,
                    answer: data.correct ? 'Correct!' : 'Incorrect'
                }])
            }
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const submitAction = async (actionType, content) => {
        if (!gameState) return

        setLoading(true)
        setError(null)
        try {
            const response = await fetch(`${API_BASE}/game/action`, {
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

            // Auto-advance for LLM Player 2 after actions
            if (mode?.player2 === 'llm' && !data.game_over) {
                if ((data.status === 'question_answered' || data.status === 'guess_incorrect') ||
                    (data.status === 'playing' && actionType === 'set_object')) {
                    setTimeout(getNextAction, 500)
                }
            }

            // Reset action mode after question/guess
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
        const normalised = answer.trim().toLowerCase()
        return ['yes', 'no', 'y', 'n'].includes(normalised)
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

        // Simple routing based on status and action mode
        if (status === 'waiting_for_object') {
            submitAction('set_object', value)
        } else if (status === 'waiting_for_guess') {
            submitAction('make_guess', value)
        } else if (status === 'waiting_for_question' ||
            status === 'waiting_for_decision' ||
            (status === 'question_answered' && mode?.player2 === 'human' && !gameState.game_over) ||
            (status === 'guess_incorrect' && mode?.player2 === 'human' && !gameState.game_over)) {
            if (actionMode === 'guess') {
                submitAction('make_guess', value)
            } else {
                submitAction('ask_question', value)
            }
        }
    }

    const resetGame = () => {
        setMode(null)
        setGameState(null)
        setQuestionHistory([])
        setInputValue('')
        setError(null)
    }

    // Auto-advance for LLM players - simplified logic
    useEffect(() => {
        if (!gameState || loading || mode?.player2 !== 'llm') return
        if (gameState.game_over) return

        const status = gameState.status
        // Auto-advance if LLM needs to act (not waiting for human input)
        const shouldAdvance =
            status === 'playing' ||
            status === 'question_answered' ||
            status === 'guess_incorrect'

        if (shouldAdvance) {
            const timer = setTimeout(() => {
                getNextAction()
            }, 1500)
            return () => clearTimeout(timer)
        }
    }, [gameState, mode, loading, getNextAction])

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
        status === 'waiting_for_decision' ||
        status === 'waiting_for_guess' ||
        (status === 'question_answered' && !gameState.game_over && mode?.player2 === 'human') ||
        (status === 'guess_incorrect' && !gameState.game_over && mode?.player2 === 'human')

    return (
        <div className="game-container">
            <div className="header-with-exit">
                <h1>Twenty Questions</h1>
                <button onClick={resetGame} className="exit-button">Exit Game</button>
            </div>

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

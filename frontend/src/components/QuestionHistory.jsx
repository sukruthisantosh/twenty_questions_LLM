/** Question history component. */
export default function QuestionHistory({ questionHistory }) {
    if (questionHistory.length === 0) return null

    // Reverse to show most recent at top
    const reversedHistory = [...questionHistory].reverse()

    return (
        <div className="question-history">
            <h3>Question History</h3>
            {reversedHistory.map((qa, idx) => (
                <div key={questionHistory.length - 1 - idx} className="question-item">
                    <p><strong>Q:</strong> {qa.question}</p>
                    <p><strong>A:</strong> {qa.answer}</p>
                </div>
            ))}
        </div>
    )
}


/** Question history component. */
export default function QuestionHistory({ questionHistory }) {
    if (questionHistory.length === 0) return null

    return (
        <div className="question-history">
            <h3>Question History</h3>
            {questionHistory.map((qa, idx) => (
                <div key={idx} className="question-item">
                    <p><strong>Q:</strong> {qa.question}</p>
                    <p><strong>A:</strong> {qa.answer}</p>
                </div>
            ))}
        </div>
    )
}


export default function FeedbackCard({ result }) {
  return (
    <div className="feedback-card">
      {result.feedback && (
        <div className="feedback-section">
          <h4>Feedback</h4>
          <p>{result.feedback}</p>
        </div>
      )}
      {result.strengths && (
        <div className="feedback-section">
          <h4>Strengths</h4>
          <p>{result.strengths}</p>
        </div>
      )}
      {result.improvements && (
        <div className="feedback-section">
          <h4>To Improve</h4>
          <p>{result.improvements}</p>
        </div>
      )}
      {result.transcript && (
        <div className="feedback-section">
          <h4>Your Answer (transcript)</h4>
          <p className="transcript">{result.transcript}</p>
        </div>
      )}
    </div>
  );
}

export default function QuestionCard({ question, index, total }) {
  return (
    <div className="question-card">
      {typeof index === "number" && (
        <div className="question-meta">
          Question {index + 1}{total ? ` of ${total}` : ""}
        </div>
      )}
      <div className="question-subject">{question.subject} · {question.difficulty}</div>
      <h2 className="question-text">{question.text}</h2>
    </div>
  );
}

export default function ScoreCard({ score }) {
  const safe = typeof score === "number" ? score : 0;
  const color = safe >= 7 ? "var(--success)" : safe >= 4 ? "var(--warning)" : "var(--danger)";
  return (
    <div className="score-card">
      <div className="score-circle" style={{ borderColor: color }}>
        <span className="score-number">{safe.toFixed(1)}</span>
        <span className="score-out">/ 10</span>
      </div>
    </div>
  );
}

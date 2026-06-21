import { useEffect, useState } from "react";
import api from "../api/axios";
import Spinner from "../components/Spinner";
import FeedbackCard from "../components/FeedbackCard";

export default function History() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openId, setOpenId] = useState(null);

  useEffect(() => {
    api.get("/results/me")
      .then((res) => setResults(res.data))
      .catch(() => setResults([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Spinner label="Loading history..." />;

  return (
    <div className="page">
      <h1>Viva History</h1>
      {results.length === 0 ? (
        <p className="empty">No past vivas yet.</p>
      ) : (
        <ul className="history-list">
          {results.map((r) => (
            <li key={r.id} className="history-item">
              <button className="history-head" onClick={() => setOpenId(openId === r.id ? null : r.id)}>
                <span>{(r.question && r.question.text) || "Question"}</span>
                <span className="result-score">{r.score != null ? r.score.toFixed(1) : "-"}/10</span>
              </button>
              {openId === r.id && <FeedbackCard result={r} />}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

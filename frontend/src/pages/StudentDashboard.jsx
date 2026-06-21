import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";
import StatCard from "../components/StatCard";
import Spinner from "../components/Spinner";

export default function StudentDashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/dashboard/student")
      .then((res) => setData(res.data))
      .catch(() => setData({ total_vivas: 0, average_score: 0, best_score: 0, recent: [] }))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Spinner label="Loading your dashboard..." />;

  return (
    <div className="page">
      <div className="page-header">
        <h1>Hi, {user.name}</h1>
        <Link className="btn btn-large" to="/viva">Start New Viva</Link>
      </div>
      <div className="stat-grid">
        <StatCard label="Total Vivas" value={data.total_vivas} />
        <StatCard label="Average Score" value={`${data.average_score}/10`} />
        <StatCard label="Best Score" value={`${data.best_score}/10`} />
      </div>
      <h2>Recent Attempts</h2>
      {data.recent.length === 0 ? (
        <p className="empty">No attempts yet. Start your first viva!</p>
      ) : (
        <ul className="result-list">
          {data.recent.map((r) => (
            <li key={r.id} className="result-row">
              <span className="result-q">{(r.question && r.question.text) || "Question"}</span>
              <span className="result-score">{r.score != null ? r.score.toFixed(1) : "-"}/10</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

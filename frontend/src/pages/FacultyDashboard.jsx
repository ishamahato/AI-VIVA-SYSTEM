import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";
import StatCard from "../components/StatCard";
import Spinner from "../components/Spinner";

export default function FacultyDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/dashboard/faculty")
      .then((res) => setData(res.data))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Spinner label="Loading dashboard..." />;
  if (!data) return <div className="page"><p className="empty">Could not load dashboard.</p></div>;

  return (
    <div className="page">
      <div className="page-header">
        <h1>Faculty Dashboard</h1>
        <Link className="btn" to="/questions">Manage Questions</Link>
      </div>
      <div className="stat-grid">
        <StatCard label="Questions" value={data.total_questions} />
        <StatCard label="Students" value={data.total_students} />
        <StatCard label="Total Attempts" value={data.total_attempts} />
        <StatCard label="Avg Score" value={`${data.average_score}/10`} />
      </div>
      <h2>By Subject</h2>
      {data.by_subject.length === 0 ? (
        <p className="empty">No attempts yet.</p>
      ) : (
        <table className="data-table">
          <thead><tr><th>Subject</th><th>Attempts</th><th>Avg Score</th></tr></thead>
          <tbody>
            {data.by_subject.map((s) => (
              <tr key={s.subject}>
                <td>{s.subject}</td><td>{s.attempts}</td><td>{s.average_score}/10</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

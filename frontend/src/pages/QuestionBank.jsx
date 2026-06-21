import { useEffect, useState } from "react";
import api from "../api/axios";
import Spinner from "../components/Spinner";
import { useToast } from "../context/ToastContext";

const EMPTY = { subject: "", text: "", difficulty: "medium", expected_answer: "", keywords: "" };

export default function QuestionBank() {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState(EMPTY);
  const [editingId, setEditingId] = useState(null);
  const toast = useToast();

  const load = () => {
    setLoading(true);
    api.get("/questions")
      .then((res) => setQuestions(res.data))
      .catch(() => setQuestions([]))
      .finally(() => setLoading(false));
  };
  useEffect(() => { load(); }, []);

  const change = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const submit = async () => {
    if (!form.subject || !form.text) {
      toast.error("Subject and question text are required.");
      return;
    }
    try {
      if (editingId) {
        await api.put(`/questions/${editingId}`, form);
        toast.success("Question updated.");
      } else {
        await api.post("/questions", form);
        toast.success("Question added.");
      }
      setForm(EMPTY);
      setEditingId(null);
      load();
    } catch (err) {
      toast.error((err.response && err.response.data && err.response.data.detail) || "Save failed.");
    }
  };

  const edit = (q) => {
    setEditingId(q.id);
    setForm({
      subject: q.subject,
      text: q.text,
      difficulty: q.difficulty,
      expected_answer: q.expected_answer || "",
      keywords: q.keywords || "",
    });
  };

  const remove = async (id) => {
    if (!window.confirm("Delete this question?")) return;
    try {
      await api.delete(`/questions/${id}`);
      toast.success("Deleted.");
      load();
    } catch {
      toast.error("Delete failed.");
    }
  };

  return (
    <div className="page">
      <h1>Question Bank</h1>

      <div className="form-card">
        <h3>{editingId ? "Edit Question" : "Add Question"}</h3>
        <div className="form-row">
          <input placeholder="Subject" value={form.subject} onChange={(e) => change("subject", e.target.value)} />
          <select value={form.difficulty} onChange={(e) => change("difficulty", e.target.value)}>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>
        <textarea placeholder="Question text" value={form.text} onChange={(e) => change("text", e.target.value)} />
        <textarea placeholder="Model answer / key points (the AI uses this to grade)" value={form.expected_answer} onChange={(e) => change("expected_answer", e.target.value)} />
        <input placeholder="Keywords (comma separated)" value={form.keywords} onChange={(e) => change("keywords", e.target.value)} />
        <div className="form-actions">
          <button className="btn" onClick={submit}>{editingId ? "Update" : "Add"}</button>
          {editingId && <button className="btn btn-secondary" onClick={() => { setForm(EMPTY); setEditingId(null); }}>Cancel</button>}
        </div>
      </div>

      {loading ? <Spinner /> : (
        <ul className="q-list">
          {questions.map((q) => (
            <li key={q.id} className="q-item">
              <div className="q-body">
                <div className="q-subject">{q.subject} · {q.difficulty}</div>
                <div className="q-text">{q.text}</div>
              </div>
              <div className="q-actions">
                <button className="btn btn-small" onClick={() => edit(q)}>Edit</button>
                <button className="btn btn-small btn-danger" onClick={() => remove(q.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

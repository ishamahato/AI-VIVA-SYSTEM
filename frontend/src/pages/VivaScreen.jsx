import { useEffect, useState } from "react";
import api from "../api/axios";
import Spinner from "../components/Spinner";
import QuestionCard from "../components/QuestionCard";
import MicRecorder from "../components/MicRecorder";
import ScoreCard from "../components/ScoreCard";
import FeedbackCard from "../components/FeedbackCard";
import { useToast } from "../context/ToastContext";

export default function VivaScreen() {
  const [loading, setLoading] = useState(true);
  const [questions, setQuestions] = useState([]);
  const [index, setIndex] = useState(0);
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [finished, setFinished] = useState(false);
  const toast = useToast();

  const loadViva = () => {
    setLoading(true);
    setFinished(false);
    setResult(null);
    setIndex(0);
    api.post("/viva/start", { num_questions: 5 })
      .then((res) => setQuestions(res.data.questions))
      .catch((err) => toast.error((err.response && err.response.data && err.response.data.detail) || "Could not load questions."))
      .finally(() => setLoading(false));
  };

  useEffect(() => { loadViva(); }, []);

  const current = questions[index];

  const submitAudio = async (blob) => {
    setSubmitting(true);
    try {
      const form = new FormData();
      form.append("question_id", current.id);
      form.append("audio", blob, "answer.webm");
      const { data } = await api.post("/viva/answer", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(data);
    } catch (err) {
      toast.error((err.response && err.response.data && err.response.data.detail) || "Grading failed.");
    } finally {
      setSubmitting(false);
    }
  };

  const next = () => {
    if (index + 1 < questions.length) {
      setIndex(index + 1);
      setResult(null);
    } else {
      setFinished(true);
    }
  };

  if (loading) return <Spinner label="Preparing your viva..." />;
  if (questions.length === 0)
    return <div className="page"><p className="empty">No questions available yet. Ask faculty to add some.</p></div>;

  if (finished) {
    return (
      <div className="page center">
        <h1>Viva Complete</h1>
        <p>Great work! Open your History for detailed feedback on each answer.</p>
        <button className="btn btn-large" onClick={loadViva}>Start Another</button>
      </div>
    );
  }

  return (
    <div className="page viva">
      <QuestionCard question={current} index={index} total={questions.length} />

      {!result && (submitting
        ? <Spinner label="Transcribing & grading with AI..." />
        : <MicRecorder onSubmit={submitAudio} disabled={submitting} />)}

      {result && (
        <div className="viva-result">
          <ScoreCard score={result.score} />
          <FeedbackCard result={result} />
          <button className="btn btn-large" onClick={next}>
            {index + 1 < questions.length ? "Next Question" : "Finish"}
          </button>
        </div>
      )}
    </div>
  );
}

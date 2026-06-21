import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Landing() {
  const { user } = useAuth();
  return (
    <div className="landing">
      <h1>AI Viva System</h1>
      <p className="landing-sub">
        Practice oral exams with instant AI feedback. Speak your answer, and get
        scored and coached by AI in seconds.
      </p>
      <div className="landing-cta">
        {user ? (
          <Link className="btn btn-large" to={user.role === "faculty" ? "/faculty" : "/student"}>
            Go to Dashboard
          </Link>
        ) : (
          <>
            <Link className="btn btn-large" to="/register">Get Started</Link>
            <Link className="btn btn-large btn-secondary" to="/login">Login</Link>
          </>
        )}
      </div>
    </div>
  );
}

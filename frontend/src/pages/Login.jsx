import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [submitting, setSubmitting] = useState(false);
  const { login } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (!email || !password) {
      toast.error("Enter email and password.");
      return;
    }
    setSubmitting(true);
    try {
      const user = await login(email, password, role);
      toast.success(`Welcome back, ${user.name}!`);
      navigate(user.role === "faculty" ? "/faculty" : "/student");
    } catch (err) {
      toast.error((err.response && err.response.data && err.response.data.detail) || "Login failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Login</h2>
        <div className="role-switch">
          <button className={role === "student" ? "active" : ""} onClick={() => setRole("student")}>Student</button>
          <button className={role === "faculty" ? "active" : ""} onClick={() => setRole("faculty")}>Faculty</button>
        </div>
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()} />
        <button className="btn btn-full" onClick={handleSubmit} disabled={submitting}>
          {submitting ? "Logging in..." : "Login"}
        </button>
        <p className="auth-alt">No account? <Link to="/register">Register</Link></p>
      </div>
    </div>
  );
}

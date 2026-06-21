import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [submitting, setSubmitting] = useState(false);
  const { register } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (!name || !email || !password) {
      toast.error("Please fill all fields.");
      return;
    }
    if (password.length < 6) {
      toast.error("Password must be at least 6 characters.");
      return;
    }
    setSubmitting(true);
    try {
      const user = await register(name, email, password, role);
      toast.success(`Account created. Welcome, ${user.name}!`);
      navigate(user.role === "faculty" ? "/faculty" : "/student");
    } catch (err) {
      toast.error((err.response && err.response.data && err.response.data.detail) || "Registration failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Create Account</h2>
        <div className="role-switch">
          <button className={role === "student" ? "active" : ""} onClick={() => setRole("student")}>Student</button>
          <button className={role === "faculty" ? "active" : ""} onClick={() => setRole("faculty")}>Faculty</button>
        </div>
        <input placeholder="Full name" value={name} onChange={(e) => setName(e.target.value)} />
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password (min 6 chars)" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="btn btn-full" onClick={handleSubmit} disabled={submitting}>
          {submitting ? "Creating..." : "Register"}
        </button>
        <p className="auth-alt">Have an account? <Link to="/login">Login</Link></p>
      </div>
    </div>
  );
}

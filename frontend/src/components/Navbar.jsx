import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">AI Viva</Link>
      <div className="navbar-links">
        {user && user.role === "student" && (
          <>
            <Link to="/student">Dashboard</Link>
            <Link to="/history">History</Link>
          </>
        )}
        {user && user.role === "faculty" && (
          <>
            <Link to="/faculty">Dashboard</Link>
            <Link to="/questions">Questions</Link>
          </>
        )}
        <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
          {theme === "light" ? "\u{1F319}" : "\u2600\uFE0F"}
        </button>
        {user ? (
          <button className="btn btn-small" onClick={handleLogout}>Logout</button>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </div>
    </nav>
  );
}

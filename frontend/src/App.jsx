import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import StudentDashboard from "./pages/StudentDashboard";
import History from "./pages/History";
import VivaScreen from "./pages/VivaScreen";
import FacultyDashboard from "./pages/FacultyDashboard";
import QuestionBank from "./pages/QuestionBank";

export default function App() {
  return (
    <>
      <Navbar />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route path="/student" element={<ProtectedRoute role="student"><StudentDashboard /></ProtectedRoute>} />
          <Route path="/viva" element={<ProtectedRoute role="student"><VivaScreen /></ProtectedRoute>} />
          <Route path="/history" element={<ProtectedRoute role="student"><History /></ProtectedRoute>} />

          <Route path="/faculty" element={<ProtectedRoute role="faculty"><FacultyDashboard /></ProtectedRoute>} />
          <Route path="/questions" element={<ProtectedRoute role="faculty"><QuestionBank /></ProtectedRoute>} />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </>
  );
}

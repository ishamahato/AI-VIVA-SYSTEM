import { createContext, useContext, useState, useCallback } from "react";

const ToastContext = createContext(null);

// Safely turn ANY message (string, FastAPI 422 array, or object) into readable text,
// so a toast can never crash the app by trying to render an object.
function toText(message) {
  if (typeof message === "string") return message;
  if (Array.isArray(message)) {
    return message
      .map((m) => (m && typeof m === "object" ? m.msg || JSON.stringify(m) : String(m)))
      .join(". ");
  }
  if (message && typeof message === "object") {
    return message.msg || message.detail || JSON.stringify(message);
  }
  return String(message);
}

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = "info") => {
    const id = Date.now() + Math.random();
    setToasts((t) => [...t, { id, message: toText(message), type }]);
    setTimeout(() => {
      setToasts((t) => t.filter((x) => x.id !== id));
    }, 3500);
  }, []);

  const toast = {
    success: (m) => addToast(m, "success"),
    error: (m) => addToast(m, "error"),
    info: (m) => addToast(m, "info"),
  };

  return (
    <ToastContext.Provider value={toast}>
      {children}
      <div className="toast-container">
        {toasts.map((t) => (
          <div key={t.id} className={`toast toast-${t.type}`}>{t.message}</div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  return useContext(ToastContext);
}

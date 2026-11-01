import { useState } from "react";
import { Send } from "lucide-react";
import { createTask } from "../services/api";

export default function AIAssistant() {
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!description.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await createTask({ title: description.slice(0, 50), description });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Submit Task</h2>
        </div>
        <form onSubmit={handleSubmit}>
          <textarea
            className="textarea"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe your task..."
            disabled={loading}
          />
          <button className="btn" type="submit" disabled={loading} style={{ marginTop: "1rem" }}>
            <Send size={16} />
            {loading ? "Processing..." : "Submit Task"}
          </button>
        </form>
      </div>

      {error && (
        <div className="card" style={{ borderColor: "var(--danger)" }}>
          <p style={{ color: "var(--danger)" }}>Error: {error}</p>
        </div>
      )}

      {result && (
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Task Result</h2>
          </div>
          <p style={{ marginBottom: "0.5rem" }}><strong>Task ID:</strong> <span style={{ fontFamily: "monospace" }}>{result.id}</span></p>
          <p style={{ marginBottom: "1rem" }}><strong>Status:</strong> <span className={`status-badge status-${result.status}`}>{result.status}</span></p>
          {result.error_message && (
            <p style={{ color: "var(--danger)", marginBottom: "1rem" }}>{result.error_message}</p>
          )}
        </div>
      )}
    </div>
  );
}

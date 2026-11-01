import { useState, useEffect } from "react";
import { getHealth } from "../services/api";

export default function Settings() {
  const [health, setHealth] = useState({ status: "unknown", database: "unknown", ollama: "unknown" });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHealth();
  }, []);

  const loadHealth = async () => {
    try {
      const res = await getHealth();
      setHealth(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">System Configuration</h2>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          <div>
            <strong>FastAPI Status:</strong> <span className={`status-badge status-${health.status === "ok" ? "completed" : "failed"}`}>{health.status}</span>
          </div>
          <div>
            <strong>Database (SQLite):</strong> <span className={`status-badge status-${health.database === "ok" ? "completed" : "failed"}`}>{health.database}</span>
          </div>
          <div>
            <strong>Ollama:</strong> <span className={`status-badge status-${health.ollama === "ok" ? "completed" : "failed"}`}>{health.ollama}</span>
          </div>
          <div style={{ marginTop: "1rem", padding: "1rem", backgroundColor: "var(--bg-secondary)", borderRadius: "6px" }}>
            <p style={{ color: "var(--text-secondary)", fontSize: "0.875rem" }}>
              <strong>Note:</strong> Model configuration is managed via environment variables (.env). 
              Never expose API keys or credentials in the frontend.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

import { useState, useEffect } from "react";
import { getTasks } from "../services/api";

export default function ActivityLogs() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const res = await getTasks();
      setTasks(res.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: "var(--danger)" }}>Error: {error}</div>;

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Activity Logs</h2>
      </div>
      {tasks.length === 0 ? (
        <p style={{ color: "var(--text-secondary)" }}>No activity yet</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Task ID</th>
              <th>Title</th>
              <th>Status</th>
              <th>Created</th>
              <th>Error</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((task) => (
              <tr key={task.id}>
                <td style={{ fontFamily: "monospace", fontSize: "0.75rem" }}>{task.id.slice(0, 12)}...</td>
                <td style={{ maxWidth: "250px" }}>{task.title}</td>
                <td><span className={`status-badge status-${task.status}`}>{task.status}</span></td>
                <td style={{ color: "var(--text-secondary)", fontSize: "0.875rem" }}>
                  {task.created_at ? new Date(task.created_at).toLocaleString() : "-"}
                </td>
                <td style={{ color: "var(--danger)", fontSize: "0.75rem", maxWidth: "200px" }}>
                  {task.error_message || "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

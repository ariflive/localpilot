import { useState, useEffect } from "react";
import { getTasks } from "../services/api";

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState("all");
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

  const filteredTasks = filter === "all" ? tasks : tasks.filter(t => t.status === filter);

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: "var(--danger)" }}>Error: {error}</div>;

  return (
    <div>
      <div className="card">
        <div className="card-header" style={{ justifyContent: "space-between", display: "flex" }}>
          <h2 className="card-title">Tasks</h2>
          <select className="input" style={{ width: "auto" }} value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="all">All</option>
            <option value="completed">Completed</option>
            <option value="pending">Pending</option>
            <option value="processing">Processing</option>
            <option value="failed">Failed</option>
          </select>
        </div>
        {filteredTasks.length === 0 ? (
          <p style={{ color: "var(--text-secondary)" }}>No tasks found</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Task ID</th>
                <th>Title</th>
                <th>Status</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {filteredTasks.map((task) => (
                <tr key={task.id}>
                  <td style={{ fontFamily: "monospace", fontSize: "0.75rem" }}>{task.id.slice(0, 12)}...</td>
                  <td style={{ maxWidth: "400px" }}>{task.title}</td>
                  <td><span className={`status-badge status-${task.status}`}>{task.status}</span></td>
                  <td style={{ color: "var(--text-secondary)", fontSize: "0.875rem" }}>
                    {task.created_at ? new Date(task.created_at).toLocaleString() : "-"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

import { useState, useEffect } from "react";
import { CheckCircle, Clock, XCircle, ListTodo, Shield, Activity } from "lucide-react";
import { getTasks, getApprovals, getHealth } from "../services/api";

export default function Overview() {
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0, failed: 0, approvals: 0 });
  const [health, setHealth] = useState({ status: "unknown", database: "unknown", ollama: "unknown" });
  const [recentTasks, setRecentTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [tasksRes, approvalsRes, healthRes] = await Promise.all([
        getTasks(),
        getApprovals(),
        getHealth(),
      ]);
      const tasks = tasksRes.data;
      setStats({
        total: tasks.length,
        completed: tasks.filter(t => t.status === "completed").length,
        pending: tasks.filter(t => t.status === "pending" || t.status === "processing").length,
        failed: tasks.filter(t => t.status === "failed").length,
        approvals: approvalsRes.data.filter(a => a.status === "pending").length,
      });
      setHealth(healthRes.data);
      setRecentTasks(tasks.slice(0, 5));
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    { label: "Total Tasks", value: stats.total, icon: ListTodo },
    { label: "Completed", value: stats.completed, icon: CheckCircle },
    { label: "Pending", value: stats.pending, icon: Clock },
    { label: "Failed", value: stats.failed, icon: XCircle },
    { label: "Pending Approvals", value: stats.approvals, icon: Shield },
  ];

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <div className="stats-grid">
        {statCards.map((card, idx) => (
          <div key={idx} className="stat-card">
            <div className="stat-icon">
              <card.icon size={24} />
            </div>
            <div className="stat-info">
              <h3>{card.value}</h3>
              <p>{card.label}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">System Status</h2>
        </div>
        <div style={{ display: "flex", gap: "2rem", flexWrap: "wrap" }}>
          <div>FastAPI: <span className={`status-badge status-${health.status === "ok" ? "completed" : "failed"}`}>{health.status}</span></div>
          <div>SQLite: <span className={`status-badge status-${health.database === "ok" ? "completed" : "failed"}`}>{health.database}</span></div>
          <div>Ollama: <span className={`status-badge status-${health.ollama === "ok" ? "completed" : "failed"}`}>{health.ollama}</span></div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Recent Task Activity</h2>
        </div>
        {recentTasks.length === 0 ? (
          <p style={{ color: "var(--text-secondary)" }}>No tasks yet</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Task ID</th>
                <th>Description</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {recentTasks.map((task) => (
                <tr key={task.id}>
                  <td style={{ fontFamily: "monospace", fontSize: "0.75rem" }}>{task.id.slice(0, 8)}...</td>
                  <td style={{ maxWidth: "300px", overflow: "hidden", textOverflow: "ellipsis" }}>{task.title}</td>
                  <td><span className={`status-badge status-${task.status}`}>{task.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

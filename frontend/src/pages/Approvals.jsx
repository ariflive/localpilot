import { useState, useEffect } from "react";
import { Check, X } from "lucide-react";
import { getApprovals, respondApproval } from "../services/api";

export default function Approvals() {
  const [approvals, setApprovals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadApprovals();
  }, []);

  const loadApprovals = async () => {
    try {
      const res = await getApprovals();
      setApprovals(res.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleResponse = async (id, action) => {
    if (!confirm(`Are you sure you want to ${action} this request?`)) return;
    try {
      await respondApproval(id, action);
      await loadApprovals();
    } catch (err) {
      alert(err.response?.data?.detail || err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: "var(--danger)" }}>Error: {error}</div>;

  const pending = approvals.filter(a => a.status === "pending");

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Pending Approvals</h2>
        </div>
        {pending.length === 0 ? (
          <p style={{ color: "var(--text-secondary)" }}>No pending approvals</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Tool</th>
                <th>Arguments</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {pending.map((approval) => (
                <tr key={approval.id}>
                  <td>{approval.tool_name}</td>
                  <td style={{ fontFamily: "monospace", fontSize: "0.75rem" }}>{JSON.stringify(approval.tool_args)}</td>
                  <td style={{ display: "flex", gap: "0.5rem" }}>
                    <button className="btn btn-success" onClick={() => handleResponse(approval.id, "approve")}>
                      <Check size={16} /> Approve
                    </button>
                    <button className="btn btn-danger" onClick={() => handleResponse(approval.id, "reject")}>
                      <X size={16} /> Reject
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">All Approvals</h2>
        </div>
        <table className="table">
          <thead>
            <tr>
              <th>Tool</th>
              <th>Status</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {approvals.map((approval) => (
              <tr key={approval.id}>
                <td>{approval.tool_name}</td>
                <td><span className={`status-badge status-${approval.status === "approved" ? "completed" : approval.status === "rejected" ? "failed" : "pending"}`}>{approval.status}</span></td>
                <td style={{ color: "var(--text-secondary)", fontSize: "0.875rem" }}>
                  {approval.created_at ? new Date(approval.created_at).toLocaleString() : "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

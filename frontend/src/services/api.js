import axios from "axios";

const api = axios.create({
  baseURL: "/api/v1",
  timeout: 60000,
});

export const getHealth = () => api.get("/health");
export const getTasks = () => api.get("/tasks");
export const getTask = (id) => api.get(`/tasks/${id}`);
export const createTask = (data) => api.post("/tasks", data);
export const getApprovals = () => api.get("/approvals");
export const createApproval = (data) => api.post("/approvals", data);
export const respondApproval = (id, action) => api.post(`/approvals/${id}/respond`, { action });

export default api;

import { NavLink } from "react-router-dom";
import { LayoutDashboard, MessageSquare, ListTodo, CheckSquare, Activity, Settings } from "lucide-react";

export default function Sidebar() {
  const navItems = [
    { to: "/", icon: LayoutDashboard, label: "Overview" },
    { to: "/assistant", icon: MessageSquare, label: "AI Assistant" },
    { to: "/tasks", icon: ListTodo, label: "Tasks" },
    { to: "/approvals", icon: CheckSquare, label: "Approvals" },
    { to: "/activity", icon: Activity, label: "Activity Logs" },
    { to: "/settings", icon: Settings, label: "Settings" },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>LocalPilot</h2>
        <p>Your Local AI. Your Tasks. Your Control.</p>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
            end={item.to === "/"}
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </NavLink>
          ))}
      </nav>
    </aside>
  );
}

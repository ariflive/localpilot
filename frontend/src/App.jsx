import { Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import Overview from "./pages/Overview";
import AIAssistant from "./pages/AIAssistant";
import Tasks from "./pages/Tasks";
import Approvals from "./pages/Approvals";
import ActivityLogs from "./pages/ActivityLogs";
import Settings from "./pages/Settings";
import "./App.css";

function App() {
  return (
    <div className="app">
      <Sidebar />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<><Header title="Overview" /><main className="page-content"><Overview /></main></>} />
          <Route path="/assistant" element={<><Header title="AI Assistant" /><main className="page-content"><AIAssistant /></main></>} />
          <Route path="/tasks" element={<><Header title="Tasks" /><main className="page-content"><Tasks /></main></>} />
          <Route path="/approvals" element={<><Header title="Approvals" /><main className="page-content"><Approvals /></main></>} />
          <Route path="/activity" element={<><Header title="Activity Logs" /><main className="page-content"><ActivityLogs /></main></>} />
          <Route path="/settings" element={<><Header title="Settings" /><main className="page-content"><Settings /></main></>} />
        </Routes>
      </div>
    </div>
  );
}

export default App;

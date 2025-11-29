import Sidebar from "./components/Sidebar.jsx";
import ChatPanel from "./components/ChatPanel.jsx";
import RightPanel from "./components/RightPanel.jsx";

export default function App() {
  return (
    <div className="flex h-screen w-full text-white">
      <Sidebar />
      <ChatPanel />
      <RightPanel />
    </div>
  );
}

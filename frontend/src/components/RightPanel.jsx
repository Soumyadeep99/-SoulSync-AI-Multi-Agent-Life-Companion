export default function RightPanel() {
  return (
    <div className="w-72 bg-gray-800 p-4 border-l border-gray-700">
      <h2 className="text-lg font-bold mb-4">User Summary</h2>

      <div className="text-gray-300 space-y-3">
        <p>🧠 Emotional State: Stable</p>
        <p>📅 Tasks Completed: 3</p>
        <p>📘 Study Progress: 25%</p>
        <p>❤️ Wellness Score: 8/10</p>
      </div>
    </div>
  );
}

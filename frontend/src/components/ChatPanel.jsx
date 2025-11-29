// src/components/ChatPanel.jsx
import React, { useEffect, useRef, useState } from "react";

/**
 * ChatPanel — SoulSync AI
 * - Matches backend /chat endpoint (expects JSON { message, user_id })
 * - Handles backend responses of shape:
 *     { reply: "text" }
 *     { result: { reply: "text" } }
 *     { reply: { text: "..." } } (defensive)
 * - Adds typing indicator, auto-scroll, enter/shift-enter behavior, and error handling
 */

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000/chat";
const DEFAULT_USER_ID = "default_user";

export default function ChatPanel() {
  const [messages, setMessages] = useState([
    // optional welcome message
    { sender: "bot", text: "Hi — I'm SoulSync AI. How can I help today?" },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [sending, setSending] = useState(false);

  const endRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when messages change or typing state changes
  useEffect(() => {
    if (endRef.current) {
      endRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
    }
  }, [messages, isTyping]);

  // Helper: robustly extract reply text from backend response
  function extractReply(data) {
    if (!data) return null;

    // Case 1: { reply: "text" }
    if (typeof data.reply === "string") return data.reply;

    // Case 2: { result: { reply: "text" } } or { result: "text" }
    if (data.result) {
      if (typeof data.result === "string") return data.result;
      if (typeof data.result.reply === "string") return data.result.reply;
      // sometimes reply nested in object
      if (typeof data.result?.reply?.text === "string") return data.result.reply.text;
    }

    // Case 3: { reply: { text: "..." } }
    if (typeof data.reply === "object" && typeof data.reply?.text === "string") {
      return data.reply.text;
    }

    // Case 4: fallback if entire response is string
    if (typeof data === "string") return data;

    return null;
  }

  // Send message to backend
  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed || sending) return;

    // Add user message locally
    const userMsg = { sender: "user", text: trimmed, ts: Date.now() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    inputRef.current?.focus();

    // Show typing indicator
    setIsTyping(true);
    setSending(true);

    try {
      const res = await fetch(BACKEND_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: trimmed,
          user_id: DEFAULT_USER_ID,
        }),
      });

      // If non-JSON response or server error, try to get text for debugging
      const contentType = res.headers.get("content-type") || "";
      let data = null;
      if (contentType.includes("application/json")) {
        data = await res.json();
      } else {
        // fallback
        const text = await res.text();
        // Try parse JSON if possible
        try { data = JSON.parse(text); } catch { data = text; }
      }

      // Extract reply safely
      const replyText = extractReply(data) ?? "⚠️ No reply from server";

      // Append bot message
      const botMsg = { sender: "bot", text: replyText, ts: Date.now() };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error("Chat error:", err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Backend not responding. Check the server.", ts: Date.now() },
      ]);
    } finally {
      setIsTyping(false);
      setSending(false);
    }
  };

  // Enter = send, Shift+Enter = newline
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full p-4 bg-gray-900 text-gray-100">
      {/* Messages */}
      <div
        className="flex-1 overflow-auto space-y-3 mb-3 px-2"
        style={{ scrollbarGutter: "stable" }}
      >
        {messages.map((m, i) => (
          <div
            key={`${m.ts ?? i}-${i}`}
            className={`max-w-xl break-words p-3 rounded-lg shadow-sm inline-block ${
              m.sender === "user"
                ? "bg-blue-600 text-white self-end ml-auto"
                : "bg-gray-800 text-gray-100 self-start mr-auto"
            }`}
          >
            {m.text}
          </div>
        ))}

        {/* Typing indicator */}
        {isTyping && (
          <div className="max-w-xs p-2 rounded-lg bg-gray-800 text-gray-100 inline-block animate-pulse">
            Typing...
          </div>
        )}

        <div ref={endRef} />
      </div>

      {/* Input area */}
      <div className="flex gap-2 items-end">
        <textarea
          ref={inputRef}
          rows={1}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message and press Enter (Shift+Enter for newline)..."
          className="flex-1 resize-none p-3 rounded bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring"
          disabled={sending}
        />

        <button
          onClick={sendMessage}
          disabled={sending}
          className={`px-4 py-2 rounded ${
            sending ? "bg-blue-400 cursor-wait" : "bg-blue-600 hover:bg-blue-700"
          } text-white`}
        >
          {sending ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}

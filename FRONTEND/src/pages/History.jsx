import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Clock3, MessageSquare, Trash2, ArrowLeft, Plus } from "lucide-react";
import useAuth from "../hooks/useAuth";

export default function History() {
  const { user, token } = useAuth();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

  useEffect(() => {
    const loadHistory = async () => {
      if (!user?.id || !token) {
        setLoading(false);
        return;
      }

      try {
        const response = await fetch(
          `${API_BASE_URL}/api/chat/history/${user.id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          setHistory(data);
        }
      } catch (err) {
        console.error("Failed to load history:", err);
      } finally {
        setLoading(false);
      }
    };

    loadHistory();
  }, [user, token, API_BASE_URL]);

  const deleteChat = async (chatId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/${chatId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setHistory((previous) =>
          previous.filter((item) => item.id !== chatId)
        );
      }
    } catch (err) {
      console.error("Failed to delete chat:", err);
    }
  };

  return (
    <div className="min-h-screen bg-[#030712] text-white flex flex-col font-sans">
      {/* Top Header */}
      <header className="h-16 border-b border-white/10 bg-[#030712]/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-30">
        <div className="flex items-center gap-4">
          <Link
            to="/chat"
            className="flex items-center gap-2 text-xs font-medium text-slate-400 hover:text-white transition-colors py-1.5 px-3 rounded-lg hover:bg-white/5"
          >
            <ArrowLeft size={14} />
            <span>Back to Workspace</span>
          </Link>
          <div className="h-4 w-[1px] bg-white/10" />
          <div className="flex items-center gap-2">
            <div className="w-5 h-5 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center text-[10px] font-bold text-white">
              z
            </div>
            <span className="text-xs font-semibold tracking-wider uppercase text-slate-400">
              Conversation Archives
            </span>
          </div>
        </div>

        <Link
          to="/chat"
          className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 text-white text-xs font-semibold hover:opacity-90 transition shadow-md shadow-purple-900/30"
        >
          <Plus size={14} />
          <span>New Chat</span>
        </Link>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-4xl w-full mx-auto px-6 py-10">
        <div className="mb-8">
          <div className="mb-2 flex items-center gap-2">
            <Clock3 size={16} className="text-purple-400" />
            <span className="text-xs font-mono uppercase tracking-widest text-slate-500">
              Workspace History
            </span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white">
            Chat History
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Your recent conversations and analytical queries with Zentora AI.
          </p>
        </div>

        {loading ? (
          <div className="p-12 text-center text-sm text-slate-500 bg-[#090d1a] border border-white/5 rounded-2xl animate-pulse">
            Loading your conversation logs...
          </div>
        ) : history.length === 0 ? (
          <div className="rounded-2xl border border-white/10 bg-[#090d1a] p-12 text-center shadow-xl">
            <div className="w-12 h-12 rounded-xl bg-white/5 border border-white/10 mx-auto flex items-center justify-center text-slate-500 mb-4">
              <MessageSquare size={22} />
            </div>
            <p className="text-base font-medium text-white">
              No conversations archived yet
            </p>
            <p className="mt-1 text-xs text-slate-400 max-w-sm mx-auto mb-6">
              Start chatting with Zentora AI to build your persistent memory and history.
            </p>
            <Link
              to="/chat"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 text-white text-xs font-semibold hover:opacity-90 transition shadow-lg shadow-purple-900/30"
            >
              Start Conversation
            </Link>
          </div>
        ) : (
          <div className="space-y-3.5">
            {history.map((item) => (
              <div
                key={item.id}
                className="group rounded-2xl border border-white/10 bg-[#090d1a] p-5 transition-all duration-200 hover:border-purple-500/30 hover:bg-[#0c1224] shadow-lg"
              >
                <div className="flex items-start gap-4">
                  <div className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
                    <MessageSquare size={16} />
                  </div>

                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-semibold text-white">
                      {item.user_message}
                    </p>

                    <p className="mt-2 line-clamp-3 text-xs leading-relaxed text-slate-400">
                      {item.ai_response}
                    </p>

                    <p className="mt-3 text-[10px] font-mono text-slate-600">
                      {new Date(item.created_at).toLocaleString()}
                    </p>
                  </div>

                  <button
                    onClick={() => deleteChat(item.id)}
                    className="rounded-lg p-2 text-slate-600 transition hover:bg-red-500/10 hover:text-red-400"
                    aria-label="Delete conversation"
                    title="Delete conversation"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

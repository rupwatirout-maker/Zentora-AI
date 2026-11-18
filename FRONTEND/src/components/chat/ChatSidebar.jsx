import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuthContext } from "../../hooks/useAuth";
import {
  Plus,
  Search,
  MessageSquare,
  Settings,
  LogOut,
  X,
  FileText,
} from "lucide-react";

export default function ChatSidebar({ onNewChat, onClose }) {
  const navigate = useNavigate();
  const { user, logout } = useAuthContext();
  const [searchQuery, setSearchQuery] = useState("");

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  const displayName = user?.username || user?.full_name || "Zentora User";
  const displayEmail = user?.email || "user@zentora.ai";

  return (
    <aside className="w-64 sm:w-72 h-full bg-[#030712] border-r border-white/10 flex flex-col justify-between z-40 select-none">
      {/* Top Section */}
      <div className="p-4 flex flex-col gap-4">
        {/* Brand header with Z logo */}
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 p-[1.5px] shadow-[0_0_12px_rgba(168,85,247,0.4)]">
              <div className="w-full h-full rounded-full bg-[#090d1a] flex items-center justify-center font-bold text-xs text-white">
                z
              </div>
            </div>
            <span className="font-semibold text-sm tracking-tight text-white">
              Zentora AI
            </span>
          </Link>

          <button
            type="button"
            onClick={onClose}
            className="md:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5"
            aria-label="Close sidebar"
          >
            <X size={18} />
          </button>
        </div>

        {/* New Chat Button */}
        <button
          type="button"
          onClick={onNewChat}
          className="w-full py-2.5 px-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-purple-500/40 text-white font-medium text-xs flex items-center gap-2 transition duration-200 group active:scale-[0.98]"
        >
          <div className="w-5 h-5 rounded-md bg-purple-500/20 text-purple-400 flex items-center justify-center group-hover:bg-purple-500 group-hover:text-white transition">
            <Plus size={14} />
          </div>
          <span>New Chat</span>
        </button>

        {/* Search chats input */}
        <div className="relative">
          <Search
            size={14}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
          />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search chats"
            className="w-full rounded-xl bg-[#090d1a] border border-white/5 pl-9 pr-3 py-2 text-xs text-white placeholder:text-slate-600 focus:outline-none focus:border-white/20 transition"
          />
        </div>

        {/* Recent Conversations */}
        <div className="mt-2 flex flex-col gap-1">
          <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 px-2 mb-1">
            Recent
          </span>

          <div
            onClick={onNewChat}
            className="flex items-center gap-2.5 px-3 py-2 rounded-xl bg-white/[0.04] text-slate-200 text-xs font-medium cursor-pointer hover:bg-white/[0.08] transition"
          >
            <MessageSquare size={14} className="text-purple-400 shrink-0" />
            <span className="truncate">New conversation</span>
          </div>

          <Link
            to="/history"
            className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-white/[0.04] text-xs font-medium transition"
          >
            <FileText size={14} className="shrink-0" />
            <span className="truncate">Conversation archives</span>
          </Link>
        </div>
      </div>

      {/* Bottom Section: Settings & User Profile */}
      <div className="p-3 border-t border-white/10 flex flex-col gap-2">
        <Link
          to="/settings"
          className="flex items-center gap-2 px-3 py-2 rounded-xl text-xs text-slate-400 hover:text-white hover:bg-white/5 transition"
        >
          <Settings size={15} />
          <span>Settings</span>
        </Link>

        {/* User Card */}
        <div className="flex items-center justify-between p-2 rounded-xl bg-white/[0.03] border border-white/5">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center font-bold text-xs text-white shrink-0">
              {displayName.charAt(0).toUpperCase()}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-semibold text-white truncate">
                {displayName}
              </p>
              <p className="text-[10px] text-slate-500 truncate">{displayEmail}</p>
            </div>
          </div>

          <button
            type="button"
            onClick={handleLogout}
            title="Sign out"
            className="p-1.5 rounded-lg text-slate-500 hover:text-red-400 hover:bg-red-500/10 transition"
          >
            <LogOut size={14} />
          </button>
        </div>
      </div>
    </aside>
  );
}

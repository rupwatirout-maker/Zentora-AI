import { Menu } from "lucide-react";

export default function ChatHeader({ onOpenSidebar, sidebarOpen }) {
  return (
    <header className="h-14 px-4 sm:px-6 border-b border-white/10 bg-[#030712]/80 backdrop-blur-md flex items-center justify-between z-20">
      <div className="flex items-center gap-3">
        {!sidebarOpen && (
          <button
            type="button"
            onClick={onOpenSidebar}
            className="md:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5"
            aria-label="Open sidebar"
          >
            <Menu size={18} />
          </button>
        )}

        {/* Zentora AI status header */}
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 p-[1px] shadow-[0_0_10px_rgba(168,85,247,0.4)]">
            <div className="w-full h-full rounded-full bg-[#090d1a] flex items-center justify-center font-bold text-[10px] text-white">
              z
            </div>
          </div>

          <div>
            <div className="flex items-center gap-1.5 leading-none">
              <span className="text-xs font-semibold text-white">Zentora AI</span>
            </div>
            <div className="flex items-center gap-1 mt-0.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
              <span className="text-[10px] text-emerald-400 font-medium">Online</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

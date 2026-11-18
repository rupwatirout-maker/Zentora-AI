import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, MessageSquare, ArrowUpRight } from "lucide-react";

export default function ChatWindow({ messages, loading, onSuggestion }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const starterSuggestions = [
    {
      title: "Explain a technical concept",
      prompt: "Explain quantum computing in simple, practical terms.",
    },
    {
      title: "Analyze & summarize documents",
      prompt: "How can I extract key takeaways from large PDF files?",
    },
    {
      title: "Write code & algorithms",
      prompt: "Write a high-performance Python FastAPI endpoint with background tasks.",
    },
  ];

  return (
    <div className="flex-1 overflow-y-auto px-4 sm:px-6 py-6 flex flex-col space-y-6">
      {messages.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center max-w-xl mx-auto text-center py-12">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 p-[1.5px] shadow-[0_0_30px_rgba(168,85,247,0.4)] mb-4">
            <div className="w-full h-full rounded-2xl bg-[#030712] flex items-center justify-center font-serif italic text-2xl font-bold text-white">
              Z
            </div>
          </div>

          <h2 className="text-xl font-semibold text-white mb-1.5">
            How can I assist you today?
          </h2>
          <p className="text-xs text-slate-400 mb-8 max-w-sm">
            Ask questions, upload documents for RAG analysis, or brainstorm ideas.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full">
            {starterSuggestions.map((item, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => onSuggestion?.(item.prompt)}
                className="group p-3 rounded-xl bg-white/[0.03] hover:bg-white/[0.07] border border-white/5 hover:border-purple-500/30 text-left transition text-xs flex flex-col justify-between"
              >
                <span className="font-medium text-slate-200 group-hover:text-purple-300 transition-colors">
                  {item.title}
                </span>
                <div className="flex items-center justify-between text-[11px] text-slate-500 mt-2">
                  <span>Try this</span>
                  <ArrowUpRight
                    size={12}
                    className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform"
                  />
                </div>
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className="max-w-4xl w-full mx-auto space-y-6">
          <AnimatePresence initial={false}>
            {messages.map((message) => {
              const isUser = message.role === "user";

              return (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10, scale: 0.98 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ duration: 0.25 }}
                  className={`flex items-start gap-3 ${
                    isUser ? "justify-end" : "justify-start"
                  }`}
                >
                  {/* Assistant Avatar */}
                  {!isUser && (
                    <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 p-[1px] shadow-[0_0_10px_rgba(168,85,247,0.3)] shrink-0 mt-1">
                      <div className="w-full h-full rounded-full bg-[#090d1a] flex items-center justify-center font-bold text-[10px] text-white">
                        z
                      </div>
                    </div>
                  )}

                  {/* Message Bubble */}
                  <div
                    className={`max-w-[85%] sm:max-w-2xl px-4 py-3 rounded-2xl text-xs sm:text-sm leading-relaxed whitespace-pre-wrap ${
                      isUser
                        ? "bg-gradient-to-r from-[#3b82f6] to-[#8b5cf6] text-white rounded-tr-xs shadow-md shadow-purple-900/20"
                        : message.isError
                        ? "bg-red-500/10 border border-red-500/20 text-red-300 rounded-tl-xs"
                        : "bg-[#090d1a] border border-white/10 text-slate-200 rounded-tl-xs shadow-lg"
                    }`}
                  >
                    {message.content}
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>

          {/* Typing Indicator */}
          {loading && (
            <motion.div
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-center gap-3"
            >
              <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 p-[1px] shrink-0">
                <div className="w-full h-full rounded-full bg-[#090d1a] flex items-center justify-center font-bold text-[10px] text-white">
                  z
                </div>
              </div>
              <div className="flex items-center gap-1.5 px-4 py-2.5 rounded-2xl bg-[#090d1a] border border-white/10">
                <span className="w-1.5 h-1.5 rounded-full bg-purple-400 animate-pulse" />
                <span
                  className="w-1.5 h-1.5 rounded-full bg-purple-400 animate-pulse"
                  style={{ animationDelay: "150ms" }}
                />
                <span
                  className="w-1.5 h-1.5 rounded-full bg-purple-400 animate-pulse"
                  style={{ animationDelay: "300ms" }}
                />
                <span className="text-[11px] text-slate-400 ml-1">Thinking...</span>
              </div>
            </motion.div>
          )}

          <div ref={bottomRef} />
        </div>
      )}
    </div>
  );
}

import { useState, useRef } from "react";
import { ArrowUp, Paperclip, Loader2 } from "lucide-react";
import { useChatContext } from "../../hooks/useChat";
import { useAuthContext } from "../../hooks/useAuth";
import uploadService from "../../services/upload";

export default function ChatInput() {
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  const { sendMessage, loading } = useChatContext();
  const { user, token } = useAuthContext();

  const handleSubmit = async (e) => {
    e?.preventDefault();
    const trimmed = message.trim();
    if (!trimmed || loading || uploading) return;

    setMessage("");
    await sendMessage(trimmed);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file || !user?.id || !token) return;

    setUploading(true);
    try {
      await uploadService.upload(file, user.id, token);
      await sendMessage(`[Attached Document: ${file.name}] Please summarize and index this document.`);
    } catch (err) {
      console.error("Upload error:", err);
      alert(err.message || "Failed to upload file.");
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  return (
    <div className="p-4 sm:p-6 bg-[#030712] border-t border-white/5">
      <div className="max-w-4xl mx-auto">
        <form
          onSubmit={handleSubmit}
          className="relative flex items-center bg-[#090d1a] border border-white/10 focus-within:border-purple-500/50 rounded-2xl p-2 shadow-2xl transition"
        >
          {/* File Upload Attachment Button */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            className="hidden"
            accept=".pdf,.txt,.docx,.csv,.md"
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading || loading}
            title="Upload document for RAG analysis"
            className="p-2.5 rounded-xl text-slate-400 hover:text-white hover:bg-white/5 transition disabled:opacity-40"
          >
            {uploading ? (
              <Loader2 size={18} className="animate-spin text-purple-400" />
            ) : (
              <Paperclip size={18} />
            )}
          </button>

          {/* Text input */}
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={loading || uploading}
            placeholder={
              loading
                ? "Zentora AI is generating a response..."
                : uploading
                ? "Uploading document to vector store..."
                : "Message Zentora AI..."
            }
            className="flex-1 bg-transparent border-none text-white text-xs sm:text-sm px-3 py-2 outline-none resize-none placeholder:text-slate-500 max-h-32"
          />

          {/* Send Button */}
          <button
            type="submit"
            disabled={!message.trim() || loading || uploading}
            className="w-8 h-8 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white flex items-center justify-center transition disabled:opacity-30 disabled:pointer-events-none shrink-0 shadow-md shadow-blue-900/30"
          >
            <ArrowUp size={16} />
          </button>
        </form>

        {/* Disclaimer text */}
        <p className="text-[10px] text-slate-500 text-center mt-2 font-mono">
          Zentora AI can make mistakes. Verify important information.
        </p>
      </div>
    </div>
  );
}

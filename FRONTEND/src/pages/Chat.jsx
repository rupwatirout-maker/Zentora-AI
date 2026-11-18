import { useState } from "react";
import ChatSidebar from "../components/chat/ChatSidebar";
import ChatHeader from "../components/chat/ChatHeader";
import ChatWindow from "../components/chat/ChatWindow";
import ChatInput from "../components/chat/ChatInput";
import { ChatProvider } from "../context/ChatContext.jsx";
import { useChatContext } from "../hooks/useChat";

function ChatContent() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { messages, loading, newChat, sendMessage } = useChatContext();

  const handleNewChat = () => {
    newChat();
    setSidebarOpen(false);
  };

  return (
    <div className="flex h-screen w-screen bg-[#030712] text-white overflow-hidden">
      {/* Desktop Sidebar */}
      <div className="hidden md:flex h-full shrink-0">
        <ChatSidebar onNewChat={handleNewChat} onClose={() => setSidebarOpen(false)} />
      </div>

      {/* Mobile Drawer Sidebar */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-50 flex md:hidden">
          <div
            className="fixed inset-0 bg-black/60 backdrop-blur-xs"
            onClick={() => setSidebarOpen(false)}
          />
          <div className="relative z-10 w-72 h-full">
            <ChatSidebar onNewChat={handleNewChat} onClose={() => setSidebarOpen(false)} />
          </div>
        </div>
      )}

      {/* Main Workspace Area */}
      <div className="flex-1 flex flex-col h-full min-w-0 bg-[#030712]">
        <ChatHeader
          onOpenSidebar={() => setSidebarOpen(true)}
          sidebarOpen={sidebarOpen}
        />

        <ChatWindow
          messages={messages}
          loading={loading}
          onSuggestion={sendMessage}
        />

        <ChatInput />
      </div>
    </div>
  );
}

export default function Chat() {
  return (
    <ChatProvider>
      <ChatContent />
    </ChatProvider>
  );
}

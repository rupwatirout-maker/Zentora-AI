import React, { createContext, useState, useCallback, useMemo } from "react";
import chatService from "../services/chat";
import { useAuthContext } from "../hooks/useAuth";

export const ChatContext = createContext(null);

export function ChatProvider({ children }) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const { user, token } = useAuthContext();

  const newChat = useCallback(() => {
    setMessages([]);
  }, []);

  const sendMessage = useCallback(
    async (content) => {
      if (!content || !content.trim()) return;

      const userMessage = {
        id: `user-${Date.now()}`,
        role: "user",
        content: content.trim(),
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setLoading(true);

      try {
        const userId = user?.id || 1;
        const response = await chatService.sendMessage(content.trim(), userId, token);

        const aiResponseText =
          response?.response ||
          response?.reply ||
          response?.message ||
          "I have received your inquiry. How else can I assist your workflow?";

        const assistantMessage = {
          id: `ai-${Date.now()}`,
          role: "assistant",
          content: aiResponseText,
          created_at: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        console.error("Chat error:", err);
        const errorMessage = {
          id: `err-${Date.now()}`,
          role: "assistant",
          content:
            err.response?.data?.detail ||
            err.message ||
            "Unable to reach the Zentora AI intelligence core. Please check your FastAPI backend.",
          isError: true,
          created_at: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setLoading(false);
      }
    },
    [user, token]
  );

  const value = useMemo(
    () => ({
      messages,
      loading,
      sendMessage,
      newChat,
      setMessages,
    }),
    [messages, loading, sendMessage, newChat]
  );

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
}

export default ChatContext;

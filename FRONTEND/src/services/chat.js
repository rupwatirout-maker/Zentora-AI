import api from "./api";

export const chatService = {
  async sendMessage(message, userId, token) {
    const response = await api.post("/api/chat/", {
      user_id: userId,
      message,
    });
    return response.data;
  },

  async getHistory(userId) {
    const response = await api.get(`/api/chat/history/${userId}`);
    return response.data;
  },

  async deleteChat(chatId) {
    const response = await api.delete(`/api/chat/${chatId}`);
    return response.data;
  },
};

export default chatService;

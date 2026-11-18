import api from "./api";

export const uploadService = {
  async upload(file, userId) {
    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("file", file);

    const response = await api.post("/api/upload/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },
};

export default uploadService;

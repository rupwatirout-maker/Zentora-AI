import api from "./api";

export const authService = {
  async signup({ username, email, password }) {
    const response = await api.post("/api/auth/signup", {
      username,
      email,
      password,
    });
    return response.data;
  },

  async login({ email, password }) {
    const response = await api.post("/api/auth/login", {
      email,
      password,
    });
    return response.data;
  },
};

export default authService;

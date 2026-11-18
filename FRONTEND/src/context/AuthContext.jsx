import React, { createContext, useCallback, useMemo, useState } from "react";
import { authService } from "../services/auth";
import { storage } from "../services/storage";

export const AuthContext = createContext(null);

function normalizeUser(user, fallbackEmail = "") {
  if (!user) {
    return fallbackEmail ? { email: fallbackEmail } : null;
  }
  return {
    ...user,
    email: user.email || fallbackEmail,
    username: user.username || user.name || user.full_name || "User",
  };
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => storage.getToken());
  const [user, setUser] = useState(() => storage.getUser());
  const [loading, setLoading] = useState(false);

  const login = useCallback(async ({ email, password }) => {
    setLoading(true);
    try {
      const data = await authService.login({ email, password });
      if (!data?.access_token) {
        throw new Error("Login succeeded but no access token was returned.");
      }

      const nextUser = normalizeUser(data.user, email);
      storage.setToken(data.access_token);
      storage.setUser(nextUser);

      setToken(data.access_token);
      setUser(nextUser);
      return data;
    } finally {
      setLoading(false);
    }
  }, []);

  const signup = useCallback(async ({ username, email, password }) => {
    setLoading(true);
    try {
      return await authService.signup({ username, email, password });
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    storage.clearAuth();
    setToken(null);
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({
      token,
      user,
      loading,
      isAuthenticated: Boolean(token),
      login,
      signup,
      logout,
    }),
    [token, user, loading, login, signup, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export default AuthContext;

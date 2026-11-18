import React, { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowLeft, Loader2, Eye, EyeOff } from "lucide-react";
import { useAuthContext } from "../hooks/useAuth";
import GhostFibers from "../components/backgrounds/GhostFibers";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const { login } = useAuthContext();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from || "/chat";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!email.trim() || !password) {
      setError("Please provide both email and password.");
      return;
    }

    setSubmitting(true);
    try {
      await login({ email: email.trim(), password });
      navigate(from, { replace: true });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Invalid credentials. Please verify your email and password."
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="relative min-h-screen w-full bg-[#030712] text-white flex flex-col justify-between overflow-hidden">
      {/* Background WebGL fibers */}
      <div className="absolute inset-0 z-0 opacity-40 pointer-events-none">
        <GhostFibers
          glowColor="#8b5cf6"
          layers={2}
          threads={48}
          speed={0.3}
          particles={0.3}
          glow={0.6}
        />
      </div>

      {/* Top Left: <- Back link */}
      <div className="relative z-20 p-6 sm:p-8">
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-xs font-medium text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft size={14} />
          <span>Back</span>
        </Link>
      </div>

      {/* Centered Glassmorphic Card */}
      <main className="relative z-20 flex-1 flex items-center justify-center px-4 py-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 15 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="w-full max-w-[420px] rounded-2xl bg-[#090d1a]/85 border border-white/10 p-8 sm:p-9 backdrop-blur-2xl shadow-2xl shadow-purple-950/30"
        >
          {/* Logo badge with Z */}
          <div className="flex items-center justify-center gap-2.5 mb-5">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 p-[1.5px] shadow-[0_0_15px_rgba(168,85,247,0.5)]">
              <div className="w-full h-full rounded-full bg-[#090d1a] flex items-center justify-center font-bold text-xs text-white">
                z
              </div>
            </div>
            <span className="font-semibold text-sm tracking-tight text-white">
              Zentora AI
            </span>
          </div>

          {/* Heading */}
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold tracking-tight text-white mb-1.5">
              Welcome back
            </h1>
            <p className="text-xs text-slate-400">
              Sign in to continue to your AI workspace.
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-xs text-red-300">
              {error}
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
                className="w-full rounded-xl bg-[#0e1424] border border-white/10 px-4 py-3 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500/50 transition"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  required
                  className="w-full rounded-xl bg-[#0e1424] border border-white/10 px-4 py-3 pr-11 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500/50 transition"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 focus:outline-none p-1 transition"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  title={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {/* Gradient button */}
            <button
              type="submit"
              disabled={submitting}
              className="w-full mt-2 py-3.5 px-4 rounded-xl bg-gradient-to-r from-[#3b82f6] via-[#8b5cf6] to-[#ec4899] text-white font-semibold text-sm shadow-lg shadow-purple-600/30 hover:opacity-95 active:scale-[0.99] transition disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {submitting ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  <span>Signing in...</span>
                </>
              ) : (
                <span>Sign In</span>
              )}
            </button>
          </form>

          {/* Toggle link */}
          <p className="text-center text-xs text-slate-400 mt-6">
            Don't have an account?{" "}
            <Link
              to="/signup"
              className="text-purple-400 hover:text-purple-300 font-medium transition"
            >
              Create one
            </Link>
          </p>
        </motion.div>
      </main>

      {/* Sub-footer */}
      <footer className="relative z-20 py-4 text-center text-[11px] text-slate-600">
        Your workspace. Your intelligence. · Powered by ROOP
      </footer>
    </div>
  );
}

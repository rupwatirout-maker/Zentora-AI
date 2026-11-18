import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Bell, Globe, Moon, Save, Sparkles, ArrowLeft, Check } from "lucide-react";
import useAuth from "../hooks/useAuth";

export default function Settings() {
  const { user, token } = useAuth();

  const [settings, setSettings] = useState({
    theme: "dark",
    language: "en",
    notifications_enabled: true,
  });

  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

  useEffect(() => {
    const loadSettings = async () => {
      if (!user?.id || !token) {
        setLoading(false);
        return;
      }

      try {
        const response = await fetch(
          `${API_BASE_URL}/api/settings/${user.id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          setSettings({
            theme: data.theme || "dark",
            language: data.language || "en",
            notifications_enabled: data.notifications_enabled ?? true,
          });
        }
      } catch (err) {
        console.error("Failed to load settings:", err);
      } finally {
        setLoading(false);
      }
    };

    loadSettings();
  }, [user, token, API_BASE_URL]);

  const saveSettings = async () => {
    if (!user?.id || !token) return;

    setSaved(false);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/settings/${user.id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(settings),
        }
      );

      if (response.ok) {
        setSaved(true);
        setTimeout(() => setSaved(false), 2500);
      }
    } catch (err) {
      console.error("Failed to save settings:", err);
    }
  };

  return (
    <div className="min-h-screen bg-[#030712] text-white flex flex-col font-sans">
      {/* Top Header */}
      <header className="h-16 border-b border-white/10 bg-[#030712]/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-30">
        <Link
          to="/chat"
          className="flex items-center gap-2 text-xs font-medium text-slate-400 hover:text-white transition-colors py-1.5 px-3 rounded-lg hover:bg-white/5"
        >
          <ArrowLeft size={14} />
          <span>Back to Workspace</span>
        </Link>

        <div className="flex items-center gap-2">
          <div className="w-5 h-5 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center text-[10px] font-bold text-white">
            z
          </div>
          <span className="text-xs font-semibold tracking-wider text-slate-300">
            Zentora AI
          </span>
        </div>
      </header>

      {/* Main Settings Panel */}
      <main className="flex-1 max-w-2xl w-full mx-auto px-6 py-12">
        <div className="mb-8">
          <div className="mb-2 flex items-center gap-2">
            <Sparkles size={14} className="text-purple-400" />
            <span className="text-xs font-mono uppercase tracking-widest text-slate-500">
              Workspace
            </span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white">
            Settings
          </h1>
          <p className="mt-1 text-xs text-slate-400">
            Manage your Zentora AI workspace preferences.
          </p>
        </div>

        {loading ? (
          <div className="p-10 text-center text-xs text-slate-500 bg-[#090d1a] border border-white/5 rounded-2xl animate-pulse">
            Loading settings...
          </div>
        ) : (
          <div className="space-y-6">
            {/* Appearance Section */}
            <div className="border-b border-white/10 pb-6">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-8 h-8 rounded-xl bg-white/5 flex items-center justify-center text-slate-300">
                  <Moon size={16} />
                </div>
                <div>
                  <p className="text-sm font-semibold text-white">Appearance</p>
                  <p className="text-xs text-slate-400">
                    Choose your workspace theme.
                  </p>
                </div>
              </div>

              <select
                value={settings.theme}
                onChange={(e) =>
                  setSettings((prev) => ({ ...prev, theme: e.target.value }))
                }
                className="w-full rounded-xl bg-[#090d1a] border border-white/10 px-4 py-2.5 text-xs text-white focus:outline-none focus:border-purple-500 transition"
              >
                <option value="dark">Dark</option>
                <option value="light">Light</option>
              </select>
            </div>

            {/* Language Section */}
            <div className="border-b border-white/10 pb-6 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-white/5 flex items-center justify-center text-slate-300">
                  <Globe size={16} />
                </div>
                <div>
                  <p className="text-sm font-semibold text-white">Language</p>
                  <p className="text-xs text-slate-400">
                    Select your workspace language.
                  </p>
                </div>
              </div>

              <select
                value={settings.language}
                onChange={(e) =>
                  setSettings((prev) => ({ ...prev, language: e.target.value }))
                }
                className="rounded-xl bg-[#090d1a] border border-white/10 px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500 transition"
              >
                <option value="en">English</option>
              </select>
            </div>

            {/* Notifications Section */}
            <div className="border-b border-white/10 pb-6 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-white/5 flex items-center justify-center text-slate-300">
                  <Bell size={16} />
                </div>
                <div>
                  <p className="text-sm font-semibold text-white">Notifications</p>
                  <p className="text-xs text-slate-400">
                    Allow workspace notifications.
                  </p>
                </div>
              </div>

              <button
                type="button"
                onClick={() =>
                  setSettings((prev) => ({
                    ...prev,
                    notifications_enabled: !prev.notifications_enabled,
                  }))
                }
                className={`relative h-6 w-11 rounded-full transition-colors ${
                  settings.notifications_enabled ? "bg-[#a855f7]" : "bg-white/10"
                }`}
              >
                <span
                  className={`absolute top-1 h-4 w-4 rounded-full bg-white transition-transform ${
                    settings.notifications_enabled ? "left-6" : "left-1"
                  }`}
                />
              </button>
            </div>

            {/* Save Button */}
            <div className="flex items-center justify-end gap-3 pt-2">
              {saved && (
                <span className="text-xs text-emerald-400 flex items-center gap-1 font-medium">
                  <Check size={14} /> Saved
                </span>
              )}

              <button
                type="button"
                onClick={saveSettings}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-semibold text-white transition active:scale-95 shadow-md"
              >
                <Save size={14} />
                <span>Save changes</span>
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

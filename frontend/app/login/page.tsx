"use client";

/**
 * /login — Admin Login only.
 * Rejects volunteer credentials. Redirects admin → /admin.
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { login, saveToken } from "@/app/services/api";

export default function AdminLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const result = await login(email, password);
    setLoading(false);

    if (result.success && result.token && result.user) {
      // Only admin allowed here
      if (result.user.role !== "ADMIN") {
        setError("This login is for Admins only. Use Volunteer Login instead.");
        return;
      }
      saveToken(result.token);
      router.push("/admin");
    } else {
      setError(result.message || "Login failed.");
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        {/* Back */}
        <Link
          href="/"
          className="inline-flex items-center gap-1 text-gray-400 hover:text-white text-sm mb-6 transition-colors"
        >
          ← Back to Home
        </Link>

        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 mb-4">
            <span className="text-3xl">🛡️</span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">
            Admin Login
          </h1>
          <p className="text-gray-400 text-sm mt-1">Dashboard access for administrators</p>
        </div>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="bg-gray-800/50 backdrop-blur border border-gray-700/50 rounded-2xl p-6 space-y-5"
        >
          {/* Email */}
          <div>
            <label htmlFor="email" className="block text-sm text-gray-300 mb-1.5">
              Admin Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@eventflow.com"
              className="w-full px-4 py-3 bg-gray-900/80 border border-gray-600/50 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
            />
          </div>

          {/* Password */}
          <div>
            <label htmlFor="password" className="block text-sm text-gray-300 mb-1.5">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-3 bg-gray-900/80 border border-gray-600/50 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
            />
          </div>

          {/* Error */}
          {error && (
            <p className="text-red-400 text-sm text-center bg-red-900/20 border border-red-500/20 rounded-lg py-2">
              {error}
            </p>
          )}

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 disabled:opacity-50 text-white text-lg font-semibold rounded-xl transition-colors"
          >
            {loading ? "Signing in…" : "Login as Admin"}
          </button>
        </form>
      </div>
    </main>
  );
}

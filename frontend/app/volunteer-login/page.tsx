"use client";

/**
 * /volunteer-login — Volunteer Login only.
 * Rejects admin credentials. Redirects volunteer → /scan.
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { login, saveToken } from "@/app/services/api";

export default function VolunteerLoginPage() {
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
      // Only volunteer allowed here
      if (result.user.role !== "VOLUNTEER") {
        setError("This login is for Volunteers only. Use Admin Login instead.");
        return;
      }
      saveToken(result.token);
      router.push("/scan");
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
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-emerald-600/20 border border-emerald-500/30 mb-4">
            <span className="text-3xl">📱</span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">
            Volunteer Login
          </h1>
          <p className="text-gray-400 text-sm mt-1">QR Scanner access for event volunteers</p>
        </div>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="bg-gray-800/50 backdrop-blur border border-gray-700/50 rounded-2xl p-6 space-y-5"
        >
          {/* Email */}
          <div>
            <label htmlFor="email" className="block text-sm text-gray-300 mb-1.5">
              Volunteer Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="volunteer@eventflow.com"
              className="w-full px-4 py-3 bg-gray-900/80 border border-gray-600/50 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition"
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
              className="w-full px-4 py-3 bg-gray-900/80 border border-gray-600/50 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition"
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
            className="w-full py-3.5 bg-emerald-600 hover:bg-emerald-500 active:bg-emerald-700 disabled:opacity-50 text-white text-lg font-semibold rounded-xl transition-colors"
          >
            {loading ? "Signing in…" : "Login as Volunteer"}
          </button>
        </form>
      </div>
    </main>
  );
}

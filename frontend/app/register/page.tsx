"use client";

/**
 * /register — Youth Parliament 6.0 Student Registration
 * Parliament background + glassmorphism card. Event fixed to "Youth Parliament 6.0".
 */

import { useState } from "react";
import Link from "next/link";
import { registerParticipant } from "@/app/services/api";

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    college: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    // Event is fixed — automatically set
    const result = await registerParticipant({
      ...formData,
      event: "Youth Parliament 6.0",
    });
    setLoading(false);

    if (result.success) {
      setSuccess(true);
    } else {
      setError(result.message || "Registration failed.");
    }
  };

  const handleReset = () => {
    setSuccess(false);
    setError("");
    setFormData({ name: "", email: "", phone: "", college: "" });
  };

  return (
    <main
      className="min-h-screen flex items-center justify-center px-4 py-8 bg-cover bg-center bg-no-repeat relative"
      style={{ backgroundImage: "url('/parliament-bg.png')" }}
    >
      {/* Dark overlay */}
      <div className="absolute inset-0 bg-black/75 backdrop-blur-sm" />

      {/* Content */}
      <div className="relative z-10 w-full max-w-md">
        {/* Back link */}
        <Link
          href="/"
          className="inline-flex items-center gap-1 text-gray-400 hover:text-white text-sm mb-6 transition-colors"
        >
          ← Back to Home
        </Link>

        {success ? (
          /* ✅ Success Card */
          <div className="bg-emerald-950/60 backdrop-blur-xl border border-emerald-500/30 rounded-2xl p-8 text-center space-y-5 shadow-2xl">
            <div className="text-6xl">🎉</div>
            <h2 className="text-2xl font-bold text-emerald-400">
              Registration Successful!
            </h2>
            <p className="text-gray-300 text-sm leading-relaxed">
              Thank you, <span className="font-semibold text-white">{formData.name}</span>.
            </p>
            <div className="p-4 bg-gray-900/60 rounded-xl border border-emerald-500/20 text-sm text-emerald-300 space-y-1">
              <p>📩 Your QR Code will be sent to your email shortly.</p>
              <p className="text-xs text-gray-400">Check your inbox or spam folder.</p>
            </div>
            <button
              onClick={handleReset}
              className="w-full py-3.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl transition-colors"
            >
              Register Another Student
            </button>
          </div>
        ) : (
          /* 📝 Registration Form — Glassmorphism */
          <form
            onSubmit={handleSubmit}
            className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 sm:p-8 space-y-5 shadow-2xl"
          >
            {/* Header */}
            <div className="text-center space-y-1">
              <p className="text-amber-400 text-xs font-bold uppercase tracking-widest">
                🏛️ SATURNANGLE
              </p>
              <h1 className="text-xl font-bold text-white">
                Youth Parliament 6.0
              </h1>
              <p className="text-gray-400 text-sm">Register to participate</p>
            </div>

            {/* Full Name */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-1.5">
                Full Name <span className="text-red-400">*</span>
              </label>
              <input
                id="name"
                name="name"
                type="text"
                required
                value={formData.name}
                onChange={handleChange}
                placeholder="Rahul Sharma"
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition backdrop-blur"
              />
            </div>

            {/* Email Address */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-1.5">
                Email Address <span className="text-red-400">*</span>
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                placeholder="rahul@example.com"
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition backdrop-blur"
              />
            </div>

            {/* Contact Number */}
            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-300 mb-1.5">
                Contact Number (10 digits) <span className="text-red-400">*</span>
              </label>
              <input
                id="phone"
                name="phone"
                type="tel"
                required
                maxLength={10}
                value={formData.phone}
                onChange={handleChange}
                placeholder="9876543210"
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition backdrop-blur font-mono"
              />
            </div>

            {/* College Name */}
            <div>
              <label htmlFor="college" className="block text-sm font-medium text-gray-300 mb-1.5">
                College Name <span className="text-red-400">*</span>
              </label>
              <input
                id="college"
                name="college"
                type="text"
                required
                value={formData.college}
                onChange={handleChange}
                placeholder="GLA University"
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition backdrop-blur"
              />
            </div>

            {/* Error */}
            {error && (
              <div className="p-3 bg-red-900/20 border border-red-500/30 rounded-xl text-red-400 text-sm text-center">
                {error}
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 disabled:opacity-50 text-white text-lg font-semibold rounded-xl transition-colors shadow-lg shadow-indigo-600/20"
            >
              {loading ? "Registering…" : "Submit Registration"}
            </button>
          </form>
        )}
      </div>
    </main>
  );
}

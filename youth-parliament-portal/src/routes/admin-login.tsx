import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { AuthCard, authInput } from "@/components/site/AuthCard";
import { ArrowRight, Lock, Mail } from "lucide-react";
import { login, saveToken } from "@/lib/api";

export const Route = createFileRoute("/admin-login")({
  head: () => ({
    meta: [
      { title: "Admin Login — MANTHAN | PRARAMBH 2K26" },
      { name: "description", content: "Administrator secure login for MANTHAN event management." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: AdminLogin,
});

function AdminLogin() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (loading) return;
    setError(null);
    setLoading(true);

    const result = await login(email.trim(), password);
    setLoading(false);

    if (result.success && result.token && result.user) {
      if (result.user.role !== "ADMIN") {
        setError("This login is for Admins only. Use Volunteer Login instead.");
        return;
      }
      saveToken(result.token);
      navigate({ to: "/admin" });
    } else {
      setError(result.message || "Invalid credentials. Please check your email and password.");
    }
  };

  return (
    <AuthCard
      eyebrow="Administration Portal"
      title="Admin Login"
      subtitle="Access real-time registration data, attendance metrics and participant exports."
    >
      <form onSubmit={onSubmit} className="grid gap-5">
        <label className="block">
          <span className="flex items-center gap-1.5 text-[11px] font-bold tracking-[0.16em] uppercase text-[#102A43]">
            <Mail className="h-3.5 w-3.5 text-[#C49A45]" />
            Administrator Email
          </span>
          <input
            type="email"
            className={authInput + " mt-1.5"}
            placeholder="admin@example.com"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label className="block">
          <span className="flex items-center gap-1.5 text-[11px] font-bold tracking-[0.16em] uppercase text-[#102A43]">
            <Lock className="h-3.5 w-3.5 text-[#C49A45]" />
            Password
          </span>
          <input
            type="password"
            className={authInput + " mt-1.5"}
            placeholder="••••••••"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        {error && (
          <div
            role="alert"
            className="rounded-lg border border-[#9E2A2B]/30 bg-[#9E2A2B]/5 p-3.5 text-xs sm:text-sm text-[#9E2A2B] font-medium"
          >
            {error}
          </div>
        )}
        <button
          type="submit"
          disabled={loading}
          className="btn-primary w-full mt-2 !py-3 !font-bold"
        >
          {loading ? "Authenticating..." : (
            <>
              Sign In to Admin Dashboard <ArrowRight className="h-4 w-4" />
            </>
          )}
        </button>
      </form>
    </AuthCard>
  );
}

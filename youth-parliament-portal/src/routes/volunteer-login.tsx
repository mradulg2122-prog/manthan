import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { AuthCard, authInput } from "@/components/site/AuthCard";
import { ArrowRight, Lock, Mail, QrCode } from "lucide-react";
import { login, saveToken } from "@/lib/api";

export const Route = createFileRoute("/volunteer-login")({
  head: () => ({
    meta: [
      { title: "Volunteer Login — MANTHAN | PRARAMBH 2K26" },
      { name: "description", content: "Secure volunteer access portal for MANTHAN event check-in staff." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: VolunteerLogin,
});

function VolunteerLogin() {
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
      if (result.user.role !== "VOLUNTEER") {
        setError("This login is for Volunteers only. Use Admin Login instead.");
        return;
      }
      saveToken(result.token);
      navigate({ to: "/scanner" });
    } else {
      setError(result.message || "Invalid credentials. Please check your volunteer account.");
    }
  };

  return (
    <AuthCard
      eyebrow="Event Staff Desk"
      title="Volunteer Login"
      subtitle="Access camera QR scanner and mark participant check-ins in real time."
    >
      <form onSubmit={onSubmit} className="grid gap-5">
        <label className="block">
          <span className="flex items-center gap-1.5 text-[11px] font-bold tracking-[0.16em] uppercase text-[#102A43]">
            <Mail className="h-3.5 w-3.5 text-[#C49A45]" />
            Volunteer Email
          </span>
          <input
            type="email"
            className={authInput + " mt-1.5"}
            placeholder="volunteer1@eventflow.com"
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
          {loading ? "Signing in..." : (
            <>
              <QrCode className="h-4 w-4 text-[#C49A45]" />
              Open QR Scanner <ArrowRight className="h-4 w-4" />
            </>
          )}
        </button>
      </form>
    </AuthCard>
  );
}

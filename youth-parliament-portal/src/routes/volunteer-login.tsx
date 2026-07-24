import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { AuthCard, authInput } from "@/components/site/AuthCard";
import { ArrowRight } from "lucide-react";
import { login, saveToken } from "@/lib/api";

export const Route = createFileRoute("/volunteer-login")({
  head: () => ({
    meta: [
      { title: "Volunteer Login — Youth Parliament 6.0" },
      { name: "description", content: "Secure volunteer access portal for Youth Parliament 6.0 event staff." },
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
      setError(result.message || "Login failed.");
    }
  };

  return (
    <AuthCard eyebrow="Staff Portal" title="Volunteer Login" subtitle="Access the scanner and delegate check-in tools.">
      <form onSubmit={onSubmit} className="grid gap-5">
        <label className="block">
          <span className="text-[11px] font-semibold tracking-[0.18em] uppercase text-muted-foreground">Volunteer Email</span>
          <input
            type="email"
            className={authInput + " mt-2"}
            placeholder="volunteer1@eventflow.com"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label className="block">
          <span className="text-[11px] font-semibold tracking-[0.18em] uppercase text-muted-foreground">Password</span>
          <input
            type="password"
            className={authInput + " mt-2"}
            placeholder="••••••••"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        {error && (
          <div role="alert" className="rounded-md border border-[color:var(--crimson)]/30 bg-[color:var(--crimson)]/5 px-4 py-3 text-sm text-[color:var(--crimson)]">
            {error}
          </div>
        )}
        <button type="submit" disabled={loading} className="btn-primary w-full mt-2">
          {loading ? "Signing in..." : (<>Sign In <ArrowRight className="h-4 w-4" /></>)}
        </button>
      </form>
    </AuthCard>
  );
}

import { createFileRoute, Link, useNavigate, Outlet, useChildMatches } from "@tanstack/react-router";
import { useState } from "react";
import { SiteShell } from "@/components/site/SiteShell";
import parliament from "@/assets/parliament-hero.jpg";
import { ShieldCheck, ArrowRight } from "lucide-react";
import { registerParticipant } from "@/lib/api";

export const Route = createFileRoute("/register")({
  head: () => ({
    meta: [
      { title: "Register — Youth Parliament 6.0 | Saturangle × GLA University" },
      { name: "description", content: "Official registration form for Youth Parliament 6.0 hosted by Saturangle at GLA University." },
      { property: "og:title", content: "Register for Youth Parliament 6.0" },
      { property: "og:description", content: "Complete your official registration for Youth Parliament 6.0." },
    ],
  }),
  component: RegisterRouteWrapper,
});

function RegisterRouteWrapper() {
  const childMatches = useChildMatches();
  if (childMatches.length > 0) {
    return <Outlet />;
  }
  return <RegisterPage />;
}

function Field({ label, children, required }: { label: string; children: React.ReactNode; required?: boolean }) {
  return (
    <label className="block">
      <span className="text-[11px] font-semibold tracking-[0.18em] uppercase text-muted-foreground">
        {label}{required && <span className="text-[color:var(--crimson)] ml-1">*</span>}
      </span>
      <div className="mt-2">{children}</div>
    </label>
  );
}

const inputCls = "w-full bg-white border border-border rounded-md px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-[color:var(--gold)] focus:ring-2 focus:ring-[color:var(--gold)]/25 transition";

function RegisterPage() {
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [college, setCollege] = useState("GLA University");

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (submitting) return;
    setError(null);
    setSubmitting(true);

    try {
      const result = await registerParticipant({
        name: name.trim(),
        email: email.trim(),
        phone: phone.trim(),
        college: college.trim(),
        event: "Youth Parliament 6.0",
      });

      const isSuccess =
        result.success === true ||
        result.participant_id !== undefined ||
        result.id !== undefined ||
        (result.success !== false && Boolean(result.message) && !result.detail);

      if (isSuccess) {
        await navigate({ to: "/register/success" });
      } else {
        setError(result.message || "Registration failed. Please try again.");
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Registration failed. Please try again.";
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <SiteShell hideFooter>
      <section className="relative min-h-[calc(100vh-5rem)] py-16">
        <div className="absolute inset-0 bg-cover bg-center" style={{ backgroundImage: `url(${parliament})` }} aria-hidden />
        <div className="absolute inset-0 bg-[rgba(250,249,246,0.9)]" aria-hidden />

        <div className="relative mx-auto max-w-2xl px-6">
          <div className="text-center">
            <div className="eyebrow justify-center">Official Registration</div>
            <h1 className="mt-4 font-serif text-4xl md:text-5xl text-foreground">Youth Parliament 6.0</h1>
            <div className="gold-divider mx-auto mt-6 w-24" />
            <p className="mt-4 text-sm text-muted-foreground">
              Hosted by Saturangle · GLA University
            </p>
          </div>

          <form onSubmit={onSubmit} className="gov-card mt-10 p-8 md:p-10 shadow-[var(--shadow-elevated)]">
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <ShieldCheck className="h-4 w-4 text-[color:var(--gold)]" />
              Your information is used solely for event administration.
            </div>
            <div className="gold-divider mt-4" />

            <div className="mt-6 grid gap-5">
              <Field label="Full Name" required>
                <input
                  name="name"
                  required
                  className={inputCls}
                  placeholder="e.g. Aarav Sharma"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </Field>
              <Field label="Official Email ID" required>
                <input
                  name="email"
                  type="email"
                  required
                  className={inputCls}
                  placeholder="you@example.ac.in"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </Field>
              <Field label="Mobile Number (10 digits)" required>
                <input
                  name="phone"
                  type="tel"
                  required
                  maxLength={10}
                  className={inputCls}
                  placeholder="9876543210"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                />
              </Field>
              <Field label="College" required>
                <input
                  name="college"
                  required
                  className={inputCls}
                  placeholder="GLA University"
                  value={college}
                  onChange={(e) => setCollege(e.target.value)}
                />
              </Field>
              <Field label="Event">
                <input readOnly value="Youth Parliament 6.0" className={inputCls + " bg-[color:var(--surface)] cursor-not-allowed"} />
              </Field>
            </div>

            <div className="gold-divider mt-8" />
            {error && (
              <div role="alert" className="mt-6 rounded-md border border-[color:var(--crimson)]/30 bg-[color:var(--crimson)]/5 px-4 py-3 text-sm text-[color:var(--crimson)]">
                {error}
              </div>
            )}
            <div className="mt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
              <Link to="/" className="text-sm text-muted-foreground hover:text-foreground">← Back to home</Link>
              <button type="submit" disabled={submitting} aria-busy={submitting} className="btn-primary">
                {submitting ? "Submitting..." : (<>Register <ArrowRight className="h-4 w-4" /></>)}
              </button>
            </div>
          </form>

          <p className="mt-6 text-center text-xs text-muted-foreground">
            By registering you acknowledge the parliamentary code of conduct.
          </p>
        </div>
      </section>
    </SiteShell>
  );
}

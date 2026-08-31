import { createFileRoute, Link, useNavigate, Outlet, useChildMatches } from "@tanstack/react-router";
import { useState } from "react";
import { SiteShell } from "@/components/site/SiteShell";
import { ShieldCheck, ArrowRight, Sparkles, CheckCircle2, User, Mail, Phone, BookOpen, Hash } from "lucide-react";
import { registerParticipant } from "@/lib/api";

export const Route = createFileRoute("/register")({
  head: () => ({
    meta: [
      { title: "Register — MANTHAN | The Freshers' Showdown | PRARAMBH 2K26" },
      { name: "description", content: "Official registration form for MANTHAN: The Freshers' Showdown hosted by Saturangle at GLA University." },
      { property: "og:title", content: "Register for MANTHAN | The Freshers' Showdown" },
      { property: "og:description", content: "Complete your official registration for MANTHAN at GLA University." },
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

function Field({
  label,
  children,
  required,
  icon: Icon,
}: {
  label: string;
  children: React.ReactNode;
  required?: boolean;
  icon?: any;
}) {
  return (
    <label className="block">
      <span className="flex items-center gap-1.5 text-[11px] font-bold tracking-[0.16em] uppercase text-[#102A43]">
        {Icon && <Icon className="h-3.5 w-3.5 text-[#C49A45]" />}
        {label}
        {required && <span className="text-[#9E2A2B] ml-0.5">*</span>}
      </span>
      <div className="mt-1.5">{children}</div>
    </label>
  );
}

const inputCls =
  "w-full bg-[#FFFFFF] border border-[#DDD7C9] rounded-lg px-4 py-3 text-sm text-[#102A43] font-medium placeholder:text-[#627D98]/50 focus:outline-none focus:border-[#C49A45] focus:ring-2 focus:ring-[#C49A45]/20 shadow-xs transition-all";

function RegisterPage() {
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [name, setName] = useState("");
  const [rollNumber, setRollNumber] = useState("");
  const [course, setCourse] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [college] = useState("GLA University, Mathura");

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (submitting) return;
    setError(null);

    // Validate phone length
    const cleanPhone = phone.replace(/\D/g, "");
    if (cleanPhone.length !== 10) {
      setError("Please enter a valid 10-digit mobile number.");
      return;
    }

    setSubmitting(true);

    try {
      // Structure course and roll number cleanly within the college/institution field for complete backend compatibility
      const formattedAffiliation = `${course.trim()} (Roll: ${rollNumber.trim()}) — ${college}`;

      const result = await registerParticipant({
        name: name.trim(),
        email: email.trim(),
        phone: cleanPhone,
        college: formattedAffiliation,
        event: "MANTHAN | The Freshers' Showdown",
      });

      const isSuccess =
        result.success === true ||
        result.participant_id !== undefined ||
        result.id !== undefined ||
        (result.success !== false && Boolean(result.message) && !result.detail);

      if (isSuccess) {
        await navigate({ to: "/register/success" });
      } else {
        setError(result.message || "Registration failed. Please verify your details.");
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
      <section className="relative min-h-[calc(100vh-5rem)] py-12 md:py-16 bg-[#F7F4EC]">
        {/* Subtle grid aura */}
        <div
          className="absolute inset-0 opacity-[0.03] pointer-events-none"
          style={{
            backgroundImage: `radial-gradient(#102A43 1px, transparent 1px)`,
            backgroundSize: "24px 24px",
          }}
          aria-hidden
        />

        <div className="relative mx-auto max-w-2xl px-4 sm:px-6">
          <div className="text-center">
            <div className="inline-flex items-center gap-2 rounded-full border border-[#C49A45]/40 bg-white px-3.5 py-1 text-[11px] font-bold tracking-[0.2em] uppercase text-[#102A43] shadow-xs">
              <span className="h-1.5 w-1.5 rounded-full bg-[#C49A45]" />
              PRARAMBH 2K26 · OFFICIAL REGISTRATION
            </div>
            <h1 className="mt-3 font-serif text-3xl sm:text-4xl md:text-5xl font-extrabold text-[#102A43]">
              MANTHAN
            </h1>
            <p className="mt-1 font-sans text-xs sm:text-sm font-bold tracking-[0.2em] uppercase text-[#C49A45]">
              THE FRESHERS' SHOWDOWN
            </p>
            <div className="gold-divider mx-auto mt-4 w-20" />
            <p className="mt-3 text-xs sm:text-sm text-[#627D98]">
              Hosted by Saturangle – The Debate Club · GLA University
            </p>
          </div>

          <form
            onSubmit={onSubmit}
            className="gov-card mt-8 p-6 sm:p-10 shadow-lg bg-white border border-[#DDD7C9] rounded-2xl"
          >
            <div className="flex items-center gap-2 text-xs text-[#627D98]">
              <ShieldCheck className="h-4 w-4 text-[#C49A45] shrink-0" />
              <span>Official entry registration. QR pass will be issued immediately upon submission.</span>
            </div>
            <div className="gold-divider mt-4" />

            <div className="mt-6 grid gap-5">
              {/* Full Name */}
              <Field label="Full Name" icon={User} required>
                <input
                  name="name"
                  required
                  className={inputCls}
                  placeholder="e.g. Aarav Sharma"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </Field>

              {/* Roll Number & Course in 2 columns */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Field label="University Roll Number" icon={Hash} required>
                  <input
                    name="rollNumber"
                    required
                    className={inputCls}
                    placeholder="e.g. 2415000123"
                    value={rollNumber}
                    onChange={(e) => setRollNumber(e.target.value)}
                  />
                </Field>

                <Field label="Course / Branch" icon={BookOpen} required>
                  <input
                    name="course"
                    required
                    className={inputCls}
                    placeholder="e.g. B.Tech CSE (1st Year)"
                    value={course}
                    onChange={(e) => setCourse(e.target.value)}
                  />
                </Field>
              </div>

              {/* Official Email */}
              <Field label="Official / University Email ID" icon={Mail} required>
                <input
                  name="email"
                  type="email"
                  required
                  className={inputCls}
                  placeholder="e.g. aarav.sharma_cs24@gla.ac.in"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </Field>

              {/* Mobile Number */}
              <Field label="Mobile Number (10 Digits WhatsApp)" icon={Phone} required>
                <input
                  name="phone"
                  type="tel"
                  required
                  maxLength={10}
                  className={inputCls}
                  placeholder="9876543210"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value.replace(/\D/g, ""))}
                />
              </Field>

              {/* Event (Read-only) */}
              <Field label="Competition">
                <input
                  readOnly
                  value="MANTHAN | The Freshers' Showdown (PRARAMBH 2K26)"
                  className={inputCls + " bg-[#F7F4EC] text-[#102A43] cursor-not-allowed font-semibold"}
                />
              </Field>
            </div>

            <div className="gold-divider mt-8" />

            {error && (
              <div
                role="alert"
                className="mt-6 rounded-lg border border-[#9E2A2B]/30 bg-[#9E2A2B]/5 p-4 text-xs sm:text-sm text-[#9E2A2B] font-medium"
              >
                {error}
              </div>
            )}

            <div className="mt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
              <Link to="/" className="text-xs sm:text-sm font-semibold text-[#627D98] hover:text-[#102A43] transition-colors">
                ← Back to Home
              </Link>
              <button
                type="submit"
                disabled={submitting}
                aria-busy={submitting}
                className="btn-primary w-full sm:w-auto !px-7 !py-3 font-bold"
              >
                {submitting ? "Processing Registration..." : (
                  <>
                    Confirm Registration <ArrowRight className="h-4 w-4" />
                  </>
                )}
              </button>
            </div>
          </form>

          <p className="mt-6 text-center text-xs text-[#627D98]">
            By registering you acknowledge and agree to abide by the competition guidelines of Saturangle Debate Club.
          </p>
        </div>
      </section>
    </SiteShell>
  );
}

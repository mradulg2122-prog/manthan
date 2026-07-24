import { createFileRoute, Link } from "@tanstack/react-router";
import { SiteShell } from "@/components/site/SiteShell";
import { CheckCircle2, Mail, QrCode, ArrowRight, Home, Calendar } from "lucide-react";

export const Route = createFileRoute("/register/success")({
  head: () => ({
    meta: [
      { title: "Registration Successful — Youth Parliament 6.0" },
      { name: "description", content: "Your registration for Youth Parliament 6.0 has been successfully completed." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: SuccessPage,
});

function SuccessPage() {
  return (
    <SiteShell>
      <section className="py-20">
        <div className="mx-auto max-w-2xl px-6 animate-in fade-in duration-700">
          <div className="gov-card bg-white p-10 md:p-14 text-center shadow-[var(--shadow-elevated)] rounded-2xl">
            <div className="relative mx-auto flex h-24 w-24 items-center justify-center animate-in zoom-in duration-500">
              <div className="absolute inset-0 rounded-full bg-emerald-100" />
              <div className="absolute inset-2 rounded-full bg-emerald-500 flex items-center justify-center">
                <CheckCircle2 className="relative h-14 w-14 text-white" strokeWidth={2} />
              </div>
            </div>

            <div className="eyebrow justify-center mt-8">Confirmation</div>
            <h1 className="mt-3 font-serif text-4xl md:text-5xl text-foreground">Registration Successful</h1>
            <div className="gold-divider mx-auto mt-6 w-24" />
            <p className="mt-6 text-base leading-relaxed text-foreground/75">
              Your registration for <span className="font-semibold text-foreground">Youth Parliament 6.0</span> has been successfully completed.
            </p>

            <div className="mt-10 grid gap-4 text-left">
              <div className="rounded-md border border-border bg-[color:var(--surface)] p-5 flex gap-4">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-white border border-[color:var(--gold)]/50 text-[color:var(--crimson)]">
                  <Mail className="h-5 w-5" />
                </div>
                <div>
                  <div className="text-sm font-semibold text-foreground">Confirmation Email Sent</div>
                  <p className="mt-1 text-sm text-muted-foreground">
                    A confirmation email containing your unique QR Code has been sent to your registered email address.
                    Please check both your <span className="font-semibold text-foreground">Inbox</span> and <span className="font-semibold text-foreground">Spam/Junk</span> folder.
                    If you do not receive the email within a few minutes, contact the event organizers.
                  </p>
                </div>
              </div>
              <div className="rounded-md border border-border bg-[color:var(--surface)] p-5 flex gap-4">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-white border border-[color:var(--gold)]/50 text-[color:var(--crimson)]">
                  <QrCode className="h-5 w-5" />
                </div>
                <div>
                  <div className="text-sm font-semibold text-foreground">Check-in Requirement</div>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Please keep your QR Code ready during event entry. A digital copy on your phone is also acceptable.
                  </p>
                </div>
              </div>
            </div>

            <div className="gold-divider mt-10" />
            <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
              <Link to="/" className="btn-outline"><Home className="h-4 w-4" /> Back to Home</Link>
              <Link to="/" className="btn-primary"><Calendar className="h-4 w-4" /> View Schedule <ArrowRight className="h-4 w-4" /></Link>
            </div>
            <p className="mt-6 text-xs text-muted-foreground tracking-wide">Secured by EventFlow Pro</p>
          </div>
        </div>
      </section>
    </SiteShell>
  );
}

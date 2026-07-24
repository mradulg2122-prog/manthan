import { Link } from "@tanstack/react-router";
import type { ReactNode } from "react";
import { SiteShell } from "./SiteShell";
import parliament from "@/assets/parliament-hero.jpg";
import { ShieldCheck } from "lucide-react";

export const authInput = "w-full bg-white border border-border rounded-md px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-[color:var(--gold)] focus:ring-2 focus:ring-[color:var(--gold)]/25 transition";

export function AuthCard({ eyebrow, title, subtitle, children, footer }: {
  eyebrow: string; title: string; subtitle: string; children: ReactNode; footer?: ReactNode;
}) {
  return (
    <SiteShell hideFooter>
      <section className="relative min-h-[calc(100vh-5rem)] flex items-center justify-center py-16">
        <div className="absolute inset-0 bg-cover bg-center" style={{ backgroundImage: `url(${parliament})` }} aria-hidden />
        <div className="absolute inset-0 bg-[rgba(250,249,246,0.92)]" aria-hidden />

        <div className="relative w-full max-w-md px-6">
          <div className="text-center">
            <div className="eyebrow justify-center">{eyebrow}</div>
            <h1 className="mt-3 font-serif text-3xl md:text-4xl text-foreground">{title}</h1>
            <div className="gold-divider mx-auto mt-5 w-20" />
            <p className="mt-4 text-sm text-muted-foreground">{subtitle}</p>
          </div>

          <div className="gov-card mt-8 p-8 shadow-[var(--shadow-elevated)]">
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <ShieldCheck className="h-4 w-4 text-[color:var(--gold)]" />
              Restricted access · authorised personnel only.
            </div>
            <div className="gold-divider mt-4" />
            <div className="mt-6">{children}</div>
          </div>

          <div className="mt-6 text-center text-xs text-muted-foreground">
            {footer ?? <Link to="/" className="hover:text-foreground">← Back to home</Link>}
          </div>
        </div>
      </section>
    </SiteShell>
  );
}

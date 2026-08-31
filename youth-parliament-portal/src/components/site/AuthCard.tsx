import { Link } from "@tanstack/react-router";
import type { ReactNode } from "react";
import { SiteShell } from "./SiteShell";
import { ShieldCheck } from "lucide-react";

export const authInput =
  "w-full bg-white border border-[#DDD7C9] rounded-lg px-4 py-3 text-sm text-[#102A43] font-medium placeholder:text-[#627D98]/50 focus:outline-none focus:border-[#C49A45] focus:ring-2 focus:ring-[#C49A45]/20 shadow-xs transition-all";

export function AuthCard({
  eyebrow,
  title,
  subtitle,
  children,
  footer,
}: {
  eyebrow: string;
  title: string;
  subtitle: string;
  children: ReactNode;
  footer?: ReactNode;
}) {
  return (
    <SiteShell hideFooter>
      <section className="relative min-h-[calc(100vh-5rem)] flex items-center justify-center py-14 px-4 sm:px-6 bg-[#F7F4EC]">
        {/* Subtle geometric background */}
        <div
          className="absolute inset-0 opacity-[0.035] pointer-events-none"
          style={{
            backgroundImage: `radial-gradient(#102A43 1px, transparent 1px)`,
            backgroundSize: "24px 24px",
          }}
          aria-hidden
        />

        <div className="relative w-full max-w-md">
          <div className="text-center">
            <div className="eyebrow justify-center">{eyebrow}</div>
            <h1 className="mt-2 font-serif text-3xl sm:text-4xl font-extrabold text-[#102A43]">
              {title}
            </h1>
            <div className="gold-divider mx-auto mt-4 w-20" />
            <p className="mt-3 text-xs sm:text-sm text-[#627D98]">{subtitle}</p>
          </div>

          <div className="gov-card mt-8 p-6 sm:p-8 shadow-xl bg-white border border-[#DDD7C9] rounded-2xl">
            <div className="flex items-center gap-2 text-xs text-[#627D98] bg-[#FAF8F3] p-2.5 rounded-lg border border-[#DDD7C9]">
              <ShieldCheck className="h-4 w-4 text-[#C49A45] shrink-0" />
              <span>Restricted portal access · Authorized credentials required.</span>
            </div>
            <div className="mt-6">{children}</div>
          </div>

          <div className="mt-6 text-center text-xs font-semibold text-[#627D98]">
            {footer ?? (
              <Link to="/" className="hover:text-[#102A43] transition-colors">
                ← Return to MANTHAN Home
              </Link>
            )}
          </div>
        </div>
      </section>
    </SiteShell>
  );
}

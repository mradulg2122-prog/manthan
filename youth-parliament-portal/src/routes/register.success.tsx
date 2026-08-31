import { createFileRoute, Link } from "@tanstack/react-router";
import { SiteShell } from "@/components/site/SiteShell";
import { CheckCircle2, Mail, QrCode, ArrowRight, Home, Calendar, Sparkles } from "lucide-react";

export const Route = createFileRoute("/register/success")({
  head: () => ({
    meta: [
      { title: "Registration Successful — MANTHAN | The Freshers' Showdown" },
      { name: "description", content: "Your registration for MANTHAN at PRARAMBH 2K26 has been successfully completed." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: SuccessPage,
});

function SuccessPage() {
  return (
    <SiteShell>
      <section className="py-14 sm:py-20 bg-[#F7F4EC]">
        <div className="mx-auto max-w-2xl px-4 sm:px-6 animate-in fade-in duration-700">
          <div className="gov-card bg-white p-8 sm:p-14 text-center shadow-xl border border-[#DDD7C9] rounded-2xl">
            {/* Success Icon */}
            <div className="relative mx-auto flex h-20 w-20 sm:h-24 sm:w-24 items-center justify-center animate-in zoom-in duration-500">
              <div className="absolute inset-0 rounded-full bg-[#ECD8A5]/40 animate-ping opacity-25" />
              <div className="absolute inset-0 rounded-full bg-emerald-50 border border-emerald-200" />
              <div className="absolute inset-2 rounded-full bg-emerald-600 flex items-center justify-center shadow-md">
                <CheckCircle2 className="relative h-10 w-10 sm:h-12 sm:w-12 text-white" strokeWidth={2.5} />
              </div>
            </div>

            <div className="eyebrow justify-center mt-8">Registration Confirmed</div>
            <h1 className="mt-2 font-serif text-3xl sm:text-4xl md:text-5xl font-extrabold text-[#102A43]">
              Welcome to MANTHAN
            </h1>
            <p className="mt-1 font-sans text-xs sm:text-sm font-bold tracking-[0.2em] uppercase text-[#C49A45]">
              THE FRESHERS' SHOWDOWN · PRARAMBH 2K26
            </p>
            <div className="gold-divider mx-auto mt-5 w-24" />
            <p className="mt-5 text-sm sm:text-base leading-relaxed text-[#102A43]/80">
              Your official entry for <span className="font-bold text-[#102A43]">MANTHAN: The Freshers' Showdown</span> has been successfully logged in the system.
            </p>

            <div className="mt-8 grid gap-4 text-left">
              <div className="rounded-xl border border-[#DDD7C9] bg-[#FAF8F3] p-4 sm:p-5 flex gap-4 items-start">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-white border border-[#C49A45]/40 text-[#102A43] shadow-xs">
                  <Mail className="h-5 w-5 text-[#C49A45]" />
                </div>
                <div>
                  <div className="text-xs sm:text-sm font-bold text-[#102A43]">Check Your Email For QR Pass</div>
                  <p className="mt-1 text-xs sm:text-sm text-[#627D98] leading-relaxed">
                    A confirmation email containing your unique <span className="font-semibold text-[#102A43]">Participant Registration ID & QR Code</span> has been dispatched to your inbox. Please check both your Primary and Spam folders.
                  </p>
                </div>
              </div>

              <div className="rounded-xl border border-[#DDD7C9] bg-[#FAF8F3] p-4 sm:p-5 flex gap-4 items-start">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-white border border-[#C49A45]/40 text-[#102A43] shadow-xs">
                  <QrCode className="h-5 w-5 text-[#C49A45]" />
                </div>
                <div>
                  <div className="text-xs sm:text-sm font-bold text-[#102A43]">Event Day Verification</div>
                  <p className="mt-1 text-xs sm:text-sm text-[#627D98] leading-relaxed">
                    Please present your digital QR Code on your mobile phone at the registration desk on <span className="font-semibold text-[#102A43]">03 September 2026</span> at <span className="font-semibold text-[#102A43]">01:00 PM</span> for instant check-in.
                  </p>
                </div>
              </div>
            </div>

            <div className="gold-divider mt-8" />

            <div className="mt-7 flex flex-wrap items-center justify-center gap-3">
              <Link to="/" className="btn-outline !py-2.5 !px-5 text-xs sm:text-sm">
                <Home className="h-4 w-4" /> Return to Home
              </Link>
            </div>

            <p className="mt-6 text-[11px] text-[#627D98] font-medium tracking-wide">
              Powered by EventFlow Real-time Attendance & QR System
            </p>
          </div>
        </div>
      </section>
    </SiteShell>
  );
}

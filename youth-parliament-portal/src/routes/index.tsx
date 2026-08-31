import { createFileRoute, Link } from "@tanstack/react-router";
import { SiteShell } from "@/components/site/SiteShell";
import {
  Mic,
  MessageSquare,
  Users,
  Lightbulb,
  MapPin,
  Calendar,
  Clock,
  Award,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  Phone,
  Flame,
  Zap,
} from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "MANTHAN | The Freshers' Showdown — PRARAMBH 2K26 | Saturangle × GLA University" },
      { name: "description", content: "A debate and public-speaking competition for freshers at GLA University. Speak. Stand out. Conquer. 03 September 2026." },
      { property: "og:title", content: "MANTHAN | The Freshers' Showdown — PRARAMBH 2K26" },
      { property: "og:description", content: "Where Ideas Meet Arguments. Register now for MANTHAN at GLA University." },
    ],
  }),
  component: Home,
});

function Home() {
  return (
    <SiteShell transparentNav>
      {/* HERO SECTION */}
      <section className="relative overflow-hidden pt-28 pb-20 md:pt-36 md:pb-28 border-b border-[#DDD7C9]/60">
        {/* Subtle geometric academic background pattern */}
        <div className="absolute inset-0 bg-[#F7F4EC]" aria-hidden />
        <div
          className="absolute inset-0 opacity-[0.035] pointer-events-none"
          style={{
            backgroundImage: `radial-gradient(#102A43 1px, transparent 1px)`,
            backgroundSize: "28px 28px",
          }}
          aria-hidden
        />

        {/* Decorative subtle gold glowing radial aura */}
        <div
          className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[450px] bg-gradient-to-br from-[#C49A45]/12 via-[#EFECE3]/30 to-transparent rounded-full blur-3xl pointer-events-none"
          aria-hidden
        />

        <div className="relative mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 text-center">
          <div className="animate-fade-up space-y-6">
            {/* Parent Event & Club Pill */}
            <div className="inline-flex flex-wrap items-center justify-center gap-2 rounded-full border border-[#C49A45]/50 bg-white/90 px-4 py-1.5 shadow-xs backdrop-blur-sm">
              <span className="flex h-2 w-2 rounded-full bg-[#C49A45] animate-pulse" />
              <span className="text-[11px] sm:text-xs font-bold tracking-[0.22em] uppercase text-[#102A43]">
                PRARAMBH 2K26
              </span>
              <span className="text-[#C49A45]">•</span>
              <span className="text-[11px] sm:text-xs font-semibold tracking-wider text-[#627D98] uppercase">
                Saturangle – The Debate Club
              </span>
            </div>

            {/* Main Titles */}
            <div className="pt-2">
              <h1 className="font-serif text-5xl sm:text-6xl md:text-8xl font-black tracking-tight text-[#102A43] drop-shadow-xs">
                MANTHAN
              </h1>
              <div className="mt-3 flex items-center justify-center gap-3">
                <div className="h-px w-12 sm:w-20 bg-gradient-to-r from-transparent to-[#C49A45]" />
                <span className="font-sans text-sm sm:text-base md:text-xl font-bold tracking-[0.28em] uppercase text-[#C49A45]">
                  THE FRESHERS' SHOWDOWN
                </span>
                <div className="h-px w-12 sm:w-20 bg-gradient-to-l from-transparent to-[#C49A45]" />
              </div>
            </div>

            {/* Tagline & Statement */}
            <div className="space-y-3 pt-2">
              <p className="font-serif italic text-2xl sm:text-3xl md:text-4xl text-[#102A43] font-medium">
                "Your Voice. Your Ideas. Your Moment."
              </p>
              <p className="text-sm sm:text-base font-semibold tracking-[0.2em] uppercase text-[#627D98]">
                Speak. Stand Out. Conquer. &nbsp;·&nbsp; Where Ideas Meet Arguments.
              </p>
            </div>

            {/* Event Key Meta Pills */}
            <div className="mx-auto max-w-3xl pt-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 p-3.5 rounded-xl border border-[#DDD7C9] bg-white/95 shadow-sm">
                <div className="flex items-center justify-center gap-2.5 py-1 text-[#102A43]">
                  <Calendar className="h-4 w-4 text-[#C49A45] shrink-0" />
                  <div className="text-left">
                    <div className="text-[10px] font-bold uppercase tracking-wider text-[#627D98]">Date</div>
                    <div className="text-xs sm:text-sm font-bold font-sans">03 SEPTEMBER 2026</div>
                  </div>
                </div>
                <div className="flex items-center justify-center gap-2.5 py-1 text-[#102A43] border-t sm:border-t-0 sm:border-l border-[#DDD7C9]">
                  <Clock className="h-4 w-4 text-[#C49A45] shrink-0" />
                  <div className="text-left">
                    <div className="text-[10px] font-bold uppercase tracking-wider text-[#627D98]">Time</div>
                    <div className="text-xs sm:text-sm font-bold font-sans">01:00 PM – 03:00 PM</div>
                  </div>
                </div>
                <div className="flex items-center justify-center gap-2.5 py-1 text-[#102A43] border-t sm:border-t-0 sm:border-l border-[#DDD7C9]">
                  <MapPin className="h-4 w-4 text-[#C49A45] shrink-0" />
                  <div className="text-left">
                    <div className="text-[10px] font-bold uppercase tracking-wider text-[#627D98]">Venue</div>
                    <div className="text-xs sm:text-sm font-bold font-sans">Arambh Hall AB-11 (CSED BLOCK)</div>
                  </div>
                </div>
              </div>
            </div>

            {/* CTAs */}
            <div className="pt-6 flex flex-wrap items-center justify-center gap-3 sm:gap-4">
              <Link to="/register" className="btn-primary !px-7 !py-3 !text-base shadow-md hover:scale-[1.02]">
                <Mic className="h-4 w-4 text-[#C49A45]" />
                REGISTER NOW
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link to="/volunteer-login" className="btn-outline !py-3 !text-sm">
                VOLUNTEER LOGIN
              </Link>
              <Link to="/admin-login" className="btn-outline !py-3 !text-sm">
                ADMIN LOGIN
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ABOUT SECTION */}
      <section className="section-pad relative bg-[#FFFFFF]">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto">
            <div className="eyebrow justify-center">About The Competition</div>
            <h2 className="mt-3 font-serif text-3xl sm:text-4xl md:text-5xl font-bold text-[#102A43]">
              Get ready to put your voice, confidence & ideas to the test.
            </h2>
            <div className="gold-divider mx-auto mt-5 w-28" />
            <p className="mt-4 text-base sm:text-lg text-[#627D98] leading-relaxed">
              MANTHAN is the premier debate and public-speaking arena designed exclusively for freshers at GLA University. Whether you're an experienced orator or stepping onto the stage for the first time, this is your launchpad.
            </p>
          </div>

          <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-5">
            {[
              {
                icon: Lightbulb,
                title: "Express Ideas",
                desc: "Articulate your unique perspectives with eloquence and impact on crucial topics.",
              },
              {
                icon: Flame,
                title: "Build Confidence",
                desc: "Overcome stage fear, command attention, and discover your authentic public voice.",
              },
              {
                icon: Mic,
                title: "Speak With Clarity",
                desc: "Structure your thoughts logically and deliver compelling speeches that resonate.",
              },
              {
                icon: Zap,
                title: "Think Critically",
                desc: "Formulate sharp arguments, analyze opposing viewpoints, and rebut with poise.",
              },
              {
                icon: Award,
                title: "Compete & Win",
                desc: "Go head-to-head with the brightest freshers and claim prestigious accolades.",
              },
            ].map((item, idx) => (
              <div
                key={item.title}
                className="gov-card p-6 text-center hover:-translate-y-1 hover:border-[#C49A45] hover:shadow-lg transition-all duration-300 flex flex-col items-center bg-[#FAF8F3]"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white border border-[#C49A45]/40 text-[#102A43] shadow-xs">
                  <item.icon className="h-6 w-6 text-[#C49A45]" />
                </div>
                <div className="mt-1 text-[11px] font-bold font-mono text-[#C49A45]">0{idx + 1}</div>
                <h3 className="mt-2 font-serif text-lg font-bold text-[#102A43]">{item.title}</h3>
                <p className="mt-2 text-xs sm:text-sm leading-relaxed text-[#627D98]">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 2-ROUND COMPETITION FLOW */}
      <section className="section-pad bg-[#F7F4EC] relative border-y border-[#DDD7C9]/70">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto">
            <div className="eyebrow justify-center">Tournament Structure</div>
            <h2 className="mt-3 font-serif text-3xl sm:text-4xl md:text-5xl font-bold text-[#102A43]">
              The 2-Round Showdown
            </h2>
            <div className="gold-divider mx-auto mt-5 w-24" />
            <p className="mt-3 text-sm sm:text-base text-[#627D98]">
              A dynamic two-tier contest designed to test oratorical prowess and argumentative depth.
            </p>
          </div>

          <div className="mt-12 grid gap-8 md:grid-cols-2 relative">
            {/* ROUND 01 CARD */}
            <div className="gov-card p-8 md:p-10 relative overflow-hidden border-2 border-[#DDD7C9] bg-white shadow-md">
              <div className="absolute top-0 right-0 px-4 py-1.5 bg-[#102A43] text-[#F7F4EC] rounded-bl-xl font-mono text-xs font-bold tracking-wider">
                STAGE 01
              </div>
              <div className="flex items-center gap-4">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-[#F7F4EC] border border-[#C49A45]/50 text-[#102A43]">
                  <Mic className="h-7 w-7 text-[#C49A45]" />
                </div>
                <div>
                  <div className="text-[11px] font-bold tracking-[0.2em] uppercase text-[#C49A45]">Round 01</div>
                  <h3 className="font-serif text-2xl sm:text-3xl font-bold text-[#102A43]">SPEECH ROUND</h3>
                </div>
              </div>

              <p className="mt-6 text-sm sm:text-base text-[#627D98] leading-relaxed">
                Participants take the floor individually to demonstrate confidence, communication, expression, tone, and powerful stage presence.
              </p>

              <div className="mt-6 pt-6 border-t border-[#DDD7C9] space-y-2 text-xs sm:text-sm text-[#102A43]/90 font-medium">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-[#C49A45]" />
                  <span>Open to all registered freshers</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-[#C49A45]" />
                  <span>Evaluated on clarity, substance, and rhetoric</span>
                </div>
              </div>
            </div>

            {/* ROUND 02 CARD */}
            <div className="gov-card p-8 md:p-10 relative overflow-hidden border-2 border-[#C49A45] bg-white shadow-lg">
              <div className="absolute top-0 right-0 px-4 py-1.5 bg-[#C49A45] text-[#0B1D3A] rounded-bl-xl font-mono text-xs font-bold tracking-wider">
                FINAL STAGE
              </div>
              <div className="flex items-center gap-4">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-[#FBF7ED] border border-[#C49A45] text-[#102A43]">
                  <MessageSquare className="h-7 w-7 text-[#C49A45]" />
                </div>
                <div>
                  <div className="text-[11px] font-bold tracking-[0.2em] uppercase text-[#C49A45]">Round 02</div>
                  <h3 className="font-serif text-2xl sm:text-3xl font-bold text-[#102A43]">DEBATE ROUND</h3>
                </div>
              </div>

              <div className="mt-3 inline-block rounded-md bg-[#FAF2DC] px-3 py-1 text-xs font-bold text-[#8A631E] uppercase tracking-wider">
                FOR SHORTLISTED PARTICIPANTS
              </div>

              <p className="mt-4 text-sm sm:text-base text-[#627D98] leading-relaxed">
                Shortlisted participants advance to the high-stakes debate round where ideas meet arguments, refutations fly, and the ultimate champion emerges.
              </p>

              <div className="mt-6 pt-6 border-t border-[#DDD7C9] space-y-2 text-xs sm:text-sm text-[#102A43]/90 font-medium">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-[#C49A45]" />
                  <span>Head-to-head structured competitive debate format</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-[#C49A45]" />
                  <span>Judged by distinguished faculty & debaters</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* EVENT DETAILS & COORDINATORS */}
      <section className="section-pad bg-[#FFFFFF]">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-12 lg:grid-cols-12 items-start">
            {/* Left: Summary Details */}
            <div className="lg:col-span-7 space-y-6">
              <div>
                <div className="eyebrow">Key Information</div>
                <h2 className="mt-2 font-serif text-3xl sm:text-4xl font-bold text-[#102A43]">
                  MANTHAN Overview
                </h2>
                <div className="gold-divider mt-4 w-20" />
              </div>

              <div className="grid gap-4 sm:grid-cols-2 pt-2">
                <div className="gov-card p-5 bg-[#FAF8F3] border-[#DDD7C9]">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-[#627D98]">Parent Fest</div>
                  <div className="text-base font-bold text-[#102A43] mt-1 font-serif">PRARAMBH 2K26</div>
                  <div className="text-xs text-[#627D98] mt-0.5">GLA University Annual Flagship</div>
                </div>

                <div className="gov-card p-5 bg-[#FAF8F3] border-[#DDD7C9]">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-[#627D98]">Organized By</div>
                  <div className="text-base font-bold text-[#102A43] mt-1 font-serif">Saturangle</div>
                  <div className="text-xs text-[#627D98] mt-0.5">The Official Debate Club</div>
                </div>

                <div className="gov-card p-5 bg-[#FAF8F3] border-[#DDD7C9]">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-[#627D98]">Schedule</div>
                  <div className="text-base font-bold text-[#102A43] mt-1 font-serif">03 Sept 2026 · 1 PM – 3 PM</div>
                  <div className="text-xs text-[#627D98] mt-0.5">Please arrive 15 min prior</div>
                </div>

                <div className="gov-card p-5 bg-[#FAF8F3] border-[#DDD7C9]">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-[#627D98]">Location</div>
                  <div className="text-base font-bold text-[#102A43] mt-1 font-serif">GLA University</div>
                  <div className="text-xs text-[#627D98] mt-0.5">Mathura, Uttar Pradesh</div>
                </div>
              </div>
            </div>

            {/* Right: Coordinators Card */}
            <div className="lg:col-span-5">
              <div className="gov-card p-6 sm:p-8 bg-[#FAF8F3] border-2 border-[#DDD7C9]">
                <div className="eyebrow">Need Assistance?</div>
                <h3 className="font-serif text-2xl font-bold text-[#102A43] mt-1">
                  Event Coordinators
                </h3>
                <p className="text-xs sm:text-sm text-[#627D98] mt-2 leading-relaxed">
                  Have questions about rounds, rules, or registration? Reach out directly to our student coordinators.
                </p>

                <div className="mt-6 space-y-4">
                  <div className="p-4 rounded-lg bg-white border border-[#DDD7C9] flex items-center justify-between">
                    <div>
                      <div className="font-bold text-sm text-[#102A43]">Mradul Gaur</div>
                      <div className="text-xs text-[#627D98]">Coordinator, Saturangle</div>
                    </div>
                    <a
                      href="tel:7417255432"
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-[#F7F4EC] border border-[#C49A45]/40 text-xs font-bold text-[#102A43] hover:bg-[#C49A45] hover:text-white transition-colors"
                    >
                      <Phone className="h-3.5 w-3.5 text-[#C49A45]" />
                      7417255432
                    </a>
                  </div>

                  <div className="p-4 rounded-lg bg-white border border-[#DDD7C9] flex items-center justify-between">
                    <div>
                      <div className="font-bold text-sm text-[#102A43]">Nakshtra Chaudhary</div>
                      <div className="text-xs text-[#627D98]">Coordinator, Saturangle</div>
                    </div>
                    <a
                      href="tel:9258626362"
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-[#F7F4EC] border border-[#C49A45]/40 text-xs font-bold text-[#102A43] hover:bg-[#C49A45] hover:text-white transition-colors"
                    >
                      <Phone className="h-3.5 w-3.5 text-[#C49A45]" />
                      9258626362
                    </a>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-[#DDD7C9] flex items-center gap-2 text-xs text-[#627D98]">
                  <ShieldCheck className="h-4 w-4 text-[#C49A45]" />
                  <span>Official GLA University Student Body Event</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* REGISTRATION CTA SECTION */}
      <section className="section-pad bg-[#F7F4EC] border-t border-[#DDD7C9]">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="gov-card p-8 sm:p-14 text-center relative overflow-hidden bg-white border-2 border-[#C49A45]/50 shadow-xl rounded-2xl">
            <div className="gold-divider absolute top-0 left-0 right-0" />
            <div className="eyebrow justify-center">Limited Slots for Freshers</div>
            <h2 className="mt-3 font-serif text-3xl sm:text-4xl md:text-5xl font-extrabold text-[#102A43]">
              Claim Your Spot at MANTHAN
            </h2>
            <p className="mt-4 text-base sm:text-lg text-[#627D98] max-w-xl mx-auto leading-relaxed">
              Complete your official registration to receive your digital QR pass instantly for the Speech & Debate rounds.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              <Link to="/register" className="btn-primary !px-8 !py-3.5 !text-base shadow-lg hover:scale-105">
                REGISTER NOW <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
            <p className="mt-5 text-xs text-[#627D98]">
              Powered by EventFlow Real-time Management System
            </p>
            <div className="gold-divider absolute bottom-0 left-0 right-0" />
          </div>
        </div>
      </section>
    </SiteShell>
  );
}

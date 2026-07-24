import { createFileRoute, Link } from "@tanstack/react-router";
import { SiteShell } from "@/components/site/SiteShell";
import parliament from "@/assets/parliament-hero.jpg";
import chakra from "@/assets/ashoka-chakra.png";
import { Scale, MessageSquare, Users, Lightbulb, MapPin, Calendar, Clock, Shirt, BookOpen, ListChecks, ArrowRight } from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Youth Parliament 6.0 — Official Registration | Saturangle × GLA University" },
      { name: "description", content: "Where voices become leaders. Register for Youth Parliament 6.0, the flagship parliamentary debate hosted by Saturangle at GLA University." },
      { property: "og:title", content: "Youth Parliament 6.0 — Official Registration" },
      { property: "og:description", content: "The flagship parliamentary debate experience. Represent your ideas on a national platform." },
    ],
  }),
  component: Home,
});

function Home() {
  return (
    <SiteShell>
      {/* HERO */}
      <section className="relative overflow-hidden">
        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: `url(${parliament})` }}
          aria-hidden
        />
        <div className="absolute inset-0 bg-[rgba(250,249,246,0.86)]" aria-hidden />
        <img
          src={chakra}
          alt=""
          aria-hidden
          className="absolute -right-40 -bottom-40 w-[560px] opacity-[0.06] pointer-events-none select-none"
        />

        <div className="relative mx-auto max-w-6xl px-6 lg:px-10 pt-24 pb-28 md:pt-32 md:pb-36 text-center">
          <div className="animate-fade-up">
            <div className="inline-flex items-center gap-3 rounded-full border border-[color:var(--gold)]/50 bg-white/70 px-4 py-1.5 text-[11px] font-semibold tracking-[0.22em] uppercase text-[color:var(--maroon)]">
              <span className="h-1.5 w-1.5 rounded-full bg-[color:var(--gold)]" />
              Official Registration Portal
            </div>

            <h1 className="mt-8 font-serif text-5xl md:text-7xl leading-[1.05] text-foreground">
              Youth Parliament <span className="text-[color:var(--crimson)]">6.0</span>
            </h1>

            <div className="gold-divider mx-auto my-8 w-40" />

            <p className="text-sm md:text-base tracking-[0.28em] uppercase text-muted-foreground">
              Hosted by <span className="text-foreground font-semibold">Saturangle Club</span> · Official Debate Club · GLA University
            </p>

            <p className="mt-10 font-serif italic text-2xl md:text-3xl text-[color:var(--maroon)]">
              "Where Voices Become Leaders."
            </p>

            <p className="mx-auto mt-6 max-w-2xl text-base md:text-lg leading-relaxed text-foreground/75">
              Join the flagship parliamentary debate experience and represent your ideas on a national platform.
            </p>

            <div className="mt-10 flex flex-wrap items-center justify-center gap-3">
              <Link to="/register" className="btn-primary">
                Register Now <ArrowRight className="h-4 w-4" />
              </Link>
              <Link to="/volunteer-login" className="btn-outline">Volunteer Login</Link>
              <Link to="/admin-login" className="btn-outline">Admin Login</Link>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="section-pad">
        <div className="mx-auto max-w-6xl px-6 lg:px-10">
          <div className="text-center max-w-2xl mx-auto">
            <div className="eyebrow justify-center">The Experience</div>
            <h2 className="mt-4 font-serif text-4xl md:text-5xl text-foreground">A platform to sharpen the future</h2>
            <div className="gold-divider mx-auto mt-6 w-24" />
          </div>

          <div className="mt-16 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {[
              { icon: Scale, title: "Leadership", body: "Develop the poise and conviction of parliamentary leadership." },
              { icon: Lightbulb, title: "Critical Thinking", body: "Engage with policy, precedent and reasoned argument." },
              { icon: MessageSquare, title: "Public Speaking", body: "Command the floor with clarity, structure and grace." },
              { icon: Users, title: "Networking", body: "Meet delegates, faculty and mentors from across India." },
            ].map((f) => (
              <div key={f.title} className="gov-card p-8 group hover:-translate-y-0.5 transition">
                <div className="flex h-12 w-12 items-center justify-center rounded-md border border-[color:var(--gold)]/50 bg-[#fbf5e6] text-[color:var(--crimson)]">
                  <f.icon className="h-6 w-6" />
                </div>
                <h3 className="mt-6 font-serif text-xl text-foreground">{f.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{f.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* EVENT INFO */}
      <section className="section-pad bg-[color:var(--surface)] relative overflow-hidden">
        <img src={chakra} alt="" aria-hidden className="absolute -left-32 top-1/2 -translate-y-1/2 w-[440px] opacity-[0.04]" />
        <div className="relative mx-auto max-w-6xl px-6 lg:px-10">
          <div className="max-w-2xl">
            <div className="eyebrow">Event Information</div>
            <h2 className="mt-4 font-serif text-4xl md:text-5xl text-foreground">The details</h2>
            <div className="gold-divider mt-6 w-24" />
          </div>

          <div className="mt-14 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {[
              { icon: MapPin, label: "Venue", value: "Central Auditorium", detail: "GLA University, Mathura" },
              { icon: Calendar, label: "Date", value: "14 – 15 March 2026", detail: "Two-day parliamentary session" },
              { icon: Clock, label: "Schedule", value: "09:00 – 18:00 IST", detail: "Opening, sessions, valedictory" },
              { icon: Shirt, label: "Dress Code", value: "Formal / Indian Formal", detail: "Delegate attire mandatory" },
              { icon: BookOpen, label: "Rules", value: "Parliamentary Procedure", detail: "Roberts Rules & speaker briefs" },
              { icon: ListChecks, label: "Timeline", value: "Registration open", detail: "Closes 07 March 2026" },
            ].map((it) => (
              <div key={it.label} className="gov-card p-7">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-md bg-[color:var(--crimson)] text-white">
                    <it.icon className="h-5 w-5" />
                  </div>
                  <div className="text-[11px] font-semibold tracking-[0.22em] uppercase text-muted-foreground">{it.label}</div>
                </div>
                <div className="mt-5 font-serif text-xl text-foreground">{it.value}</div>
                <div className="mt-1 text-sm text-muted-foreground">{it.detail}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="section-pad">
        <div className="mx-auto max-w-4xl px-6 lg:px-10">
          <div className="gov-card p-12 md:p-16 text-center relative overflow-hidden">
            <div className="gold-divider absolute top-0 left-0 right-0" />
            <div className="eyebrow justify-center">Registration Open</div>
            <h2 className="mt-4 font-serif text-3xl md:text-4xl text-foreground">
              Take your seat at Youth Parliament 6.0
            </h2>
            <p className="mt-4 text-muted-foreground max-w-xl mx-auto">
              Complete your official registration and receive your unique QR code for check-in.
            </p>
            <div className="mt-8">
              <Link to="/register" className="btn-primary">
                Register Now <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
            <div className="gold-divider absolute bottom-0 left-0 right-0" />
          </div>
        </div>
      </section>
    </SiteShell>
  );
}

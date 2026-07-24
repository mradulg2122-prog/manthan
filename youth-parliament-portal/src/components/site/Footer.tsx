import glaLogo from "@/assets/gla-logo.png";
import saturangleLogo from "@/assets/saturangle-logo.png";

export function Footer() {
  return (
    <footer className="mt-24 border-t border-border bg-white">
      <div className="mx-auto max-w-7xl px-6 lg:px-10 py-14">
        <div className="grid gap-10 md:grid-cols-3">
          <div>
            <div className="flex flex-col gap-4">
              <img src={glaLogo} alt="GLA University" className="h-14 w-auto object-contain" loading="lazy" />
              <img src={saturangleLogo} alt="Saturangle — The Debate Club" className="h-11 w-auto object-contain" loading="lazy" />
            </div>
            <p className="mt-5 text-sm text-muted-foreground max-w-xs leading-relaxed">
              Youth Parliament 6.0 — the flagship parliamentary debate hosted by Saturangle, the official debate club of GLA University.
            </p>
          </div>
          <div>
            <div className="eyebrow">Portal</div>
            <ul className="mt-4 space-y-2 text-sm text-foreground/80">
              <li><a href="/register" className="hover:text-[color:var(--crimson)]">Registration</a></li>
              <li><a href="/volunteer-login" className="hover:text-[color:var(--crimson)]">Volunteer Login</a></li>
              <li><a href="/admin-login" className="hover:text-[color:var(--crimson)]">Admin Login</a></li>
            </ul>
          </div>
          <div>
            <div className="eyebrow">Contact</div>
            <ul className="mt-4 space-y-2 text-sm text-foreground/80">
              <li>GLA University, Mathura</li>
              <li>saturangle@gla.ac.in</li>
              <li>+91 000 000 0000</li>
            </ul>
          </div>
        </div>
        <div className="gold-divider mt-12" />
        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 text-xs text-muted-foreground">
          <span>© {new Date().getFullYear()} Saturangle Debate Club, GLA University. All rights reserved.</span>
          <span className="tracking-widest uppercase">Youth Parliament 6.0</span>
        </div>
      </div>
    </footer>
  );
}

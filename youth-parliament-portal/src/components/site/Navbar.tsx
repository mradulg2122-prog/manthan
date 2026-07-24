import { Link } from "@tanstack/react-router";
import glaLogo from "@/assets/gla-logo.png";
import saturangleLogo from "@/assets/saturangle-logo.png";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur gold-border-b">
      <div className="mx-auto max-w-7xl px-6 lg:px-10">
        <div className="flex h-36 items-center justify-between gap-8">
          <Link to="/" className="flex items-center shrink-0 px-1" aria-label="GLA University">
            <img
              src={glaLogo}
              alt="GLA University"
              className="h-20 md:h-[5.25rem] w-auto object-contain"
            />
          </Link>

          <Link
            to="/"
            className="hidden md:flex items-center shrink-0 px-1"
            aria-label="Saturangle — The Debate Club"
          >
            <img
              src={saturangleLogo}
              alt="Saturangle — The Debate Club"
              className="h-20 md:h-[5rem] w-auto object-contain"
            />
          </Link>

          <nav className="flex items-center gap-1 sm:gap-2">
            <Link
              to="/volunteer-login"
              className="hidden sm:inline-flex text-sm font-medium text-foreground/80 hover:text-[color:var(--crimson)] px-3 py-2 transition"
            >
              Volunteer Login
            </Link>
            <Link
              to="/admin-login"
              className="hidden sm:inline-flex text-sm font-medium text-foreground/80 hover:text-[color:var(--crimson)] px-3 py-2 transition"
            >
              Admin Login
            </Link>
            <Link to="/register" className="btn-primary !px-5 !py-2.5 !text-sm">
              Register
            </Link>
          </nav>
        </div>

        {/* Mobile: show Saturangle logo below on small screens */}
        <div className="md:hidden pb-3 -mt-2 flex justify-center">
          <img
            src={saturangleLogo}
            alt="Saturangle — The Debate Club"
            className="h-20 w-auto object-contain opacity-95"
          />
        </div>
      </div>
    </header>
  );
}

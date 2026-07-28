import { Link } from "@tanstack/react-router";
import glaLogo from "@/assets/gla-logo.png";
import saturangleLogo from "@/assets/saturangle-logo.png";

interface NavbarProps {
  transparent?: boolean;
}

export function Navbar({ transparent = false }: NavbarProps) {
  return (
    <header
      className={
        transparent
          ? "absolute top-0 left-0 right-0 z-50"
          : "sticky top-0 z-50 bg-white/95 backdrop-blur gold-border-b"
      }
    >
      <div className="mx-auto max-w-7xl px-6 lg:px-10">
        <div
          className={`flex items-center justify-between gap-6 ${
            transparent ? "h-28 md:h-32" : "h-24"
          }`}
        >
          {/* GLA University Logo */}
          <Link to="/" className="flex items-center shrink-0" aria-label="GLA University">
            <img
              src={glaLogo}
              alt="GLA University"
              className={
                transparent
                  ? "h-[7rem] md:h-[9rem] w-auto object-contain"
                  : "h-[5.25rem] md:h-[6.5rem] w-auto object-contain"
              }
            />
          </Link>

          {/* Saturangle Logo — hidden on mobile */}
          <Link
            to="/"
            className="hidden md:flex items-center shrink-0"
            aria-label="Saturangle — The Debate Club"
          >
            <img
              src={saturangleLogo}
              alt="Saturangle — The Debate Club"
              className={
                transparent
                  ? "h-[7rem] md:h-[9rem] w-auto object-contain"
                  : "h-[5.25rem] md:h-[6.5rem] w-auto object-contain"
              }
            />
          </Link>

          {/* Spacer to push nav links right */}
          <div className="flex-1" />

          {/* Navigation Links */}
          <nav className="flex items-center gap-2 sm:gap-4">
            <Link
              to="/volunteer-login"
              className={`hidden sm:inline-flex text-sm font-medium px-3 py-2 transition ${
                transparent
                  ? "text-foreground/90 hover:text-[color:var(--crimson)]"
                  : "text-foreground/80 hover:text-[color:var(--crimson)]"
              }`}
            >
              Volunteer Login
            </Link>
            <Link
              to="/admin-login"
              className={`hidden sm:inline-flex text-sm font-medium px-3 py-2 transition ${
                transparent
                  ? "text-foreground/90 hover:text-[color:var(--crimson)]"
                  : "text-foreground/80 hover:text-[color:var(--crimson)]"
              }`}
            >
              Admin Login
            </Link>
            <Link to="/register" className="btn-primary !px-5 !py-2 !text-sm !rounded-md">
              Register
            </Link>
          </nav>
        </div>

        {/* Mobile: show Saturangle logo below on small screens */}
        <div className="md:hidden pb-2 -mt-1 flex justify-center">
          <img
            src={saturangleLogo}
            alt="Saturangle — The Debate Club"
            className="h-16 w-auto object-contain opacity-95"
          />
        </div>
      </div>
    </header>
  );
}

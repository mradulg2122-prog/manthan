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
          ? "absolute top-0 left-0 right-0 z-50 bg-gradient-to-b from-[#F7F4EC]/95 via-[#F7F4EC]/85 to-transparent backdrop-blur-[2px]"
          : "sticky top-0 z-50 bg-[#FFFFFF]/95 backdrop-blur-md border-b border-[#DDD7C9] shadow-xs"
      }
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-10">
        <div className="flex items-center justify-between gap-4 h-20 sm:h-24">
          {/* Brand logos */}
          <div className="flex items-center gap-3 sm:gap-5 shrink-0 py-1">
            {/* GLA University Logo */}
            <Link to="/" className="flex items-center" aria-label="GLA University">
              <img
                src={glaLogo}
                alt="GLA University"
                className="h-12 sm:h-14 md:h-16 w-auto object-contain transition-transform hover:scale-105"
              />
            </Link>

            <div className="h-8 sm:h-10 w-px bg-[#DDD7C9]" />

            {/* Saturangle Logo */}
            <Link
              to="/"
              className="flex items-center"
              aria-label="Saturangle — The Debate Club"
            >
              <img
                src={saturangleLogo}
                alt="Saturangle — The Debate Club"
                className="h-11 sm:h-13 md:h-15 w-auto object-contain transition-transform hover:scale-105"
              />
            </Link>
          </div>

          {/* Navigation Links */}
          <nav className="flex items-center gap-2 sm:gap-3">
            <Link
              to="/volunteer-login"
              className="hidden sm:inline-flex text-xs md:text-sm font-semibold tracking-wide px-3 py-2 text-[#102A43]/85 hover:text-[#C49A45] transition-colors rounded-md"
            >
              Volunteer
            </Link>
            <Link
              to="/admin-login"
              className="hidden sm:inline-flex text-xs md:text-sm font-semibold tracking-wide px-3 py-2 text-[#102A43]/85 hover:text-[#C49A45] transition-colors rounded-md"
            >
              Admin
            </Link>
            <Link
              to="/register"
              className="btn-primary !px-4 sm:!px-5 !py-2 !text-xs sm:!text-sm !font-bold"
            >
              Register Now
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}

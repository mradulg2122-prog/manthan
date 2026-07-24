import Link from "next/link";

/**
 * Landing page — SATURNANGLE Youth Parliament 6.0 portal.
 */

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 text-white flex flex-col">
      {/* Hero */}
      <div className="flex-1 flex items-center justify-center px-4 py-16">
        <div className="text-center max-w-xl space-y-6">
          {/* Club Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-bold uppercase tracking-widest">
            <span>🏛️</span> Official Debate Club &middot; GLA University
          </div>

          {/* Logo / Title */}
          <h1 className="text-5xl sm:text-6xl font-black tracking-tight leading-none">
            SATURN<span className="text-indigo-400">ANGLE</span>
          </h1>

          <p className="text-gray-400 text-base sm:text-lg leading-relaxed max-w-md mx-auto">
            Welcome to <span className="text-white font-semibold">SATURNANGLE</span>.
            <br />
            Youth Parliament 6.0 Registration Portal.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4">
            <Link
              href="/register"
              className="w-full sm:w-auto px-8 py-4 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white text-base font-bold rounded-xl transition-all shadow-lg shadow-indigo-600/20 text-center"
            >
              Register for Youth Parliament 6.0
            </Link>
            <Link
              href="/volunteer-login"
              className="w-full sm:w-auto px-8 py-4 bg-gray-800/70 hover:bg-gray-700 border border-gray-600/40 text-gray-200 text-base font-semibold rounded-xl transition-colors text-center"
            >
              Volunteer Login
            </Link>
            <Link
              href="/login"
              className="w-full sm:w-auto px-8 py-4 bg-gray-800/70 hover:bg-gray-700 border border-gray-600/40 text-gray-200 text-base font-semibold rounded-xl transition-colors text-center"
            >
              Admin Login
            </Link>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="text-center text-xs text-gray-600 py-4 border-t border-gray-800/50">
        SATURNANGLE &copy; {new Date().getFullYear()} &middot; GLA University &middot; Youth Parliament 6.0
      </footer>
    </main>
  );
}

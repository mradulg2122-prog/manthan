/**
 * 404 — Page Not Found
 */

import Link from "next/link";

export default function NotFound() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 flex items-center justify-center px-4">
      <div className="text-center space-y-4">
        <p className="text-7xl font-bold text-indigo-500">404</p>
        <h1 className="text-2xl font-bold text-white">Page Not Found</h1>
        <p className="text-gray-400">The page you&apos;re looking for doesn&apos;t exist.</p>
        <Link
          href="/login"
          className="inline-block mt-4 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl transition-colors"
        >
          Go to Login
        </Link>
      </div>
    </main>
  );
}

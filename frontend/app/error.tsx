"use client";

/**
 * Global error boundary — catches unhandled errors.
 */

export default function GlobalError({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 flex items-center justify-center px-4">
      <div className="text-center space-y-4 max-w-sm">
        <p className="text-6xl">⚠️</p>
        <h1 className="text-2xl font-bold text-white">Something went wrong</h1>
        <p className="text-gray-400 text-sm">
          {error.message || "An unexpected error occurred."}
        </p>
        <button
          onClick={reset}
          className="inline-block mt-4 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl transition-colors"
        >
          Try Again
        </button>
      </div>
    </main>
  );
}

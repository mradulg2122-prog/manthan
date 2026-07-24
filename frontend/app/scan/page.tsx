"use client";

/**
 * /scan — Volunteer QR Scanner Page
 * Mobile-first, large buttons, clear status cards.
 */

import { useState, useCallback, useEffect } from "react";
import { useRouter } from "next/navigation";
import QRScanner from "@/app/components/QRScanner";
import { scanQR, ScanResult, getMe, clearToken } from "@/app/services/api";

type Status = "checking" | "scanning" | "loading" | "success" | "already" | "invalid";

export default function ScanPage() {
  const router = useRouter();
  const [status, setStatus] = useState<Status>("checking");
  const [result, setResult] = useState<ScanResult | null>(null);
  const [scannerActive, setScannerActive] = useState(false);

  // Auth guard — verify token on mount
  useEffect(() => {
    getMe().then((user) => {
      if (!user) {
        clearToken();
        router.replace("/login");
      } else {
        setStatus("scanning");
        setScannerActive(true);
      }
    });
  }, [router]);

  const handleLogout = () => {
    clearToken();
    router.push("/login");
  };

  // Called when QRScanner decodes a QR code
  const handleScan = useCallback(async (data: string) => {
    setScannerActive(false);
    setStatus("loading");

    const res = await scanQR(data.trim());
    setResult(res);

    if (res.success) {
      setStatus("success");
    } else if (res.message?.includes("already")) {
      setStatus("already");
    } else {
      setStatus("invalid");
    }
  }, []);

  // Reset back to scanning
  const handleReset = () => {
    setResult(null);
    setStatus("scanning");
    setScannerActive(true);
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 text-white flex flex-col items-center px-4 py-8">
      {/* Auth check */}
      {status === "checking" && (
        <p className="text-gray-400">Checking access…</p>
      )}

      {/* Header */}
      {status !== "checking" && (
        <>
          <div className="w-full max-w-sm flex items-center justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold tracking-tight">
                EventFlow <span className="text-indigo-400">Pro</span>
              </h1>
              <p className="text-gray-400 text-sm">QR Scanner</p>
            </div>
            <button
              onClick={handleLogout}
              className="px-3 py-1.5 text-sm bg-gray-700/60 hover:bg-gray-600 text-gray-300 rounded-lg transition-colors"
            >
              Logout
            </button>
          </div>

      {/* Scanner */}
      {status === "scanning" && (
        <div className="w-full max-w-sm space-y-4">
          <QRScanner onScan={handleScan} active={scannerActive} />
          <p className="text-center text-gray-400 text-sm animate-pulse">
            Point camera at a QR code
          </p>
        </div>
      )}

      {/* Loading */}
      {status === "loading" && (
        <div className="w-full max-w-sm bg-gray-800/60 backdrop-blur rounded-2xl p-8 text-center space-y-4">
          <div className="text-4xl animate-spin">⏳</div>
          <p className="text-gray-300">Checking attendance…</p>
        </div>
      )}

      {/* ✅ Success */}
      {status === "success" && result && (
        <div className="w-full max-w-sm bg-emerald-900/40 border border-emerald-500/30 backdrop-blur rounded-2xl p-8 text-center space-y-4">
          <div className="text-5xl">✅</div>
          <h2 className="text-xl font-bold text-emerald-300">
            Attendance Marked
          </h2>
          <div className="space-y-2 text-gray-200">
            <p>
              <span className="text-gray-400">Name:</span> {result.name}
            </p>
            <p>
              <span className="text-gray-400">Event:</span> {result.event}
            </p>
            <p>
              <span className="text-gray-400">Time:</span> {result.time}
            </p>
          </div>
          <button
            onClick={handleReset}
            className="mt-4 w-full py-4 bg-emerald-600 hover:bg-emerald-500 active:bg-emerald-700 text-white text-lg font-semibold rounded-xl transition-colors"
          >
            Scan Next
          </button>
        </div>
      )}

      {/* 🟡 Already Checked In */}
      {status === "already" && result && (
        <div className="w-full max-w-sm bg-yellow-900/30 border border-yellow-500/30 backdrop-blur rounded-2xl p-8 text-center space-y-4">
          <div className="text-5xl">🟡</div>
          <h2 className="text-xl font-bold text-yellow-300">
            Already Checked In
          </h2>
          <p className="text-gray-200">{result.name}</p>
          <button
            onClick={handleReset}
            className="mt-4 w-full py-4 bg-yellow-600 hover:bg-yellow-500 active:bg-yellow-700 text-white text-lg font-semibold rounded-xl transition-colors"
          >
            Scan Next
          </button>
        </div>
      )}

      {/* 🔴 Invalid QR */}
      {status === "invalid" && (
        <div className="w-full max-w-sm bg-red-900/30 border border-red-500/30 backdrop-blur rounded-2xl p-8 text-center space-y-4">
          <div className="text-5xl">🔴</div>
          <h2 className="text-xl font-bold text-red-300">Invalid QR Code</h2>
          <p className="text-gray-400">{result?.message}</p>
          <button
            onClick={handleReset}
            className="mt-4 w-full py-4 bg-red-600 hover:bg-red-500 active:bg-red-700 text-white text-lg font-semibold rounded-xl transition-colors"
          >
            Scan Again
          </button>
        </div>
      )}

      </>
      )}
    </main>
  );
}

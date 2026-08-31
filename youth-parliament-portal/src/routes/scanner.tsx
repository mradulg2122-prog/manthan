import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState, useEffect, useCallback } from "react";
import { SiteShell } from "@/components/site/SiteShell";
import { QRScanner } from "@/components/site/QRScanner";
import { CheckCircle2, RefreshCw, XCircle, AlertTriangle, LogOut, QrCode, Sparkles, UserCheck } from "lucide-react";
import { scanQR, getMe, clearToken, type ScanResult } from "@/lib/api";

export const Route = createFileRoute("/scanner")({
  head: () => ({
    meta: [
      { title: "Check-In Scanner — MANTHAN | PRARAMBH 2K26" },
      { name: "description", content: "QR check-in scanner for MANTHAN event volunteers." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: Scanner,
});

type Status = "checking" | "scanning" | "loading" | "success" | "already" | "invalid";

function Scanner() {
  const navigate = useNavigate();
  const [status, setStatus] = useState<Status>("checking");
  const [result, setResult] = useState<ScanResult | null>(null);
  const [scannerActive, setScannerActive] = useState(false);
  const [volunteerName, setVolunteerName] = useState<string>("");

  // Auth guard — check token on mount
  useEffect(() => {
    getMe().then((user) => {
      if (!user) {
        clearToken();
        navigate({ to: "/volunteer-login" });
      } else {
        setVolunteerName(user.name || "Volunteer");
        setStatus("scanning");
        setScannerActive(true);
      }
    });
  }, [navigate]);

  const handleLogout = () => {
    clearToken();
    navigate({ to: "/volunteer-login" });
  };

  // Called when QRScanner decodes a QR code
  const handleScan = useCallback(async (data: string) => {
    setScannerActive(false);
    setStatus("loading");

    const res = await scanQR(data.trim());
    setResult(res);

    if (res.success) {
      setStatus("success");
    } else if (res.message?.toLowerCase().includes("already")) {
      setStatus("already");
    } else {
      setStatus("invalid");
    }
  }, []);

  // Reset to scan next
  const handleReset = () => {
    setResult(null);
    setStatus("scanning");
    setScannerActive(true);
  };

  return (
    <SiteShell hideFooter>
      <section className="py-10 sm:py-14 bg-[#F7F4EC] min-h-[calc(100vh-5rem)]">
        <div className="mx-auto max-w-3xl px-4 sm:px-6">
          {/* Auth check */}
          {status === "checking" && (
            <div className="text-center py-20">
              <div className="mx-auto h-10 w-10 rounded-full border-3 border-[#C49A45] border-t-transparent animate-spin" />
              <p className="mt-4 text-xs font-bold uppercase tracking-wider text-[#627D98]">Verifying Volunteer Session…</p>
            </div>
          )}

          {status !== "checking" && (
            <>
              {/* Header */}
              <div className="flex flex-wrap items-end justify-between gap-4">
                <div>
                  <div className="inline-flex items-center gap-2 rounded-full border border-[#C49A45]/40 bg-white px-3 py-0.5 text-[11px] font-bold tracking-wider uppercase text-[#102A43]">
                    <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                    MANTHAN · STAFF DESK
                  </div>
                  <h1 className="mt-2 font-serif text-3xl sm:text-4xl font-extrabold text-[#102A43]">
                    Participant QR Scanner
                  </h1>
                  <p className="text-xs sm:text-sm text-[#627D98] mt-1">
                    Logged in as: <span className="font-semibold text-[#102A43]">{volunteerName}</span>
                  </p>
                </div>
                <button
                  onClick={handleLogout}
                  className="btn-outline !py-2 !px-4 !text-xs font-bold flex items-center gap-1.5"
                >
                  <LogOut className="h-3.5 w-3.5" /> Sign Out
                </button>
              </div>

              <div className="gold-divider mt-5" />

              {/* Scanner / Status Cards */}
              <div className="gov-card mt-8 p-6 sm:p-10 shadow-xl bg-white border border-[#DDD7C9] rounded-2xl">
                {/* Camera view — shown when scanning */}
                {status === "scanning" && (
                  <div>
                    <div className="flex items-center justify-between pb-4 border-b border-[#DDD7C9]">
                      <div className="flex items-center gap-2">
                        <QrCode className="h-5 w-5 text-[#C49A45]" />
                        <span className="text-xs sm:text-sm font-bold text-[#102A43] uppercase tracking-wider">
                          Ready to Scan
                        </span>
                      </div>
                      <span className="text-xs text-[#627D98] font-mono">Back / Environment Lens</span>
                    </div>

                    <div className="relative max-w-md mx-auto mt-6 rounded-xl border-2 border-[#C49A45]/50 overflow-hidden shadow-inner bg-black/5">
                      <QRScanner onScan={handleScan} active={scannerActive} />
                    </div>

                    <p className="mt-6 text-center text-xs sm:text-sm font-medium text-[#627D98] animate-pulse">
                      Align the participant's QR pass within the camera frame
                    </p>
                  </div>
                )}

                {/* Loading */}
                {status === "loading" && (
                  <div className="py-16 text-center">
                    <div className="mx-auto h-12 w-12 rounded-full border-4 border-[#C49A45] border-t-transparent animate-spin" />
                    <p className="mt-4 text-sm font-bold text-[#102A43]">Verifying Registration & Check-In…</p>
                    <p className="text-xs text-[#627D98] mt-1">Connecting to EventFlow real-time registry</p>
                  </div>
                )}

                {/* ✅ Success */}
                {status === "success" && result && (
                  <div className="text-center py-6 animate-in zoom-in-95 duration-300">
                    <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-emerald-50 border border-emerald-200 shadow-sm">
                      <CheckCircle2 className="h-12 w-12 text-emerald-600" strokeWidth={2.5} />
                    </div>
                    <div className="eyebrow justify-center text-emerald-700 mt-5">Verified & Checked In</div>
                    <h2 className="mt-2 font-serif text-3xl font-extrabold text-[#102A43]">
                      {result.name}
                    </h2>
                    <div className="mt-4 inline-block rounded-lg bg-[#FAF8F3] border border-[#DDD7C9] px-6 py-3 text-xs sm:text-sm text-[#627D98] space-y-1">
                      {result.event && (
                        <p className="font-semibold text-[#102A43]">{result.event}</p>
                      )}
                      {result.time && (
                        <p className="text-xs text-[#627D98]">Check-in Time: {result.time}</p>
                      )}
                    </div>
                    <div className="mt-8">
                      <button onClick={handleReset} className="btn-primary !px-7 !py-3 font-bold">
                        <RefreshCw className="h-4 w-4" /> Scan Next Participant
                      </button>
                    </div>
                  </div>
                )}

                {/* 🟡 Already checked in */}
                {status === "already" && result && (
                  <div className="text-center py-6 animate-in zoom-in-95 duration-300">
                    <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-amber-50 border border-amber-200 shadow-sm">
                      <AlertTriangle className="h-12 w-12 text-amber-500" strokeWidth={2.5} />
                    </div>
                    <div className="eyebrow justify-center text-amber-700 mt-5">Duplicate Scan</div>
                    <h2 className="mt-2 font-serif text-2xl sm:text-3xl font-extrabold text-[#102A43]">
                      {result.name || "Participant"}
                    </h2>
                    <p className="mt-3 text-sm text-[#627D98] max-w-sm mx-auto">
                      {result.message || "This participant is already marked Present."}
                    </p>
                    <div className="mt-8">
                      <button onClick={handleReset} className="btn-outline !px-7 !py-3 font-bold">
                        <RefreshCw className="h-4 w-4" /> Scan Next
                      </button>
                    </div>
                  </div>
                )}

                {/* 🔴 Invalid QR */}
                {status === "invalid" && (
                  <div className="text-center py-6 animate-in zoom-in-95 duration-300">
                    <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-red-50 border border-red-200 shadow-sm">
                      <XCircle className="h-12 w-12 text-[#9E2A2B]" strokeWidth={2.5} />
                    </div>
                    <div className="eyebrow justify-center text-[#9E2A2B] mt-5">Unrecognized QR</div>
                    <h2 className="mt-2 font-serif text-2xl sm:text-3xl font-extrabold text-[#102A43]">
                      Invalid QR Code
                    </h2>
                    <p className="mt-3 text-sm text-[#627D98] max-w-sm mx-auto">
                      {result?.message || "This QR code does not belong to any registered MANTHAN participant."}
                    </p>
                    <div className="mt-8">
                      <button onClick={handleReset} className="btn-primary !px-7 !py-3 font-bold">
                        <RefreshCw className="h-4 w-4" /> Try Again
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </section>
    </SiteShell>
  );
}

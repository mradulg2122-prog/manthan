import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState, useEffect, useCallback } from "react";
import { SiteShell } from "@/components/site/SiteShell";
import { QRScanner } from "@/components/site/QRScanner";
import { CheckCircle2, RefreshCw, XCircle, AlertTriangle } from "lucide-react";
import { scanQR, getMe, clearToken, type ScanResult } from "@/lib/api";

export const Route = createFileRoute("/scanner")({
  head: () => ({
    meta: [
      { title: "Check-In Scanner — Youth Parliament 6.0" },
      { name: "description", content: "QR check-in scanner for Youth Parliament 6.0 volunteers." },
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

  // Auth guard — check token on mount
  useEffect(() => {
    getMe().then((user) => {
      if (!user) {
        clearToken();
        navigate({ to: "/volunteer-login" });
      } else {
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
    } else if (res.message?.includes("already")) {
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
      <section className="py-14">
        <div className="mx-auto max-w-3xl px-6">
          {/* Auth check */}
          {status === "checking" && (
            <div className="text-center py-20">
              <p className="text-sm text-muted-foreground">Checking access…</p>
            </div>
          )}

          {status !== "checking" && (
            <>
              {/* Header */}
              <div className="flex flex-wrap items-end justify-between gap-4">
                <div>
                  <div className="eyebrow">Check-In</div>
                  <h1 className="mt-3 font-serif text-4xl text-foreground">Delegate Scanner</h1>
                  <div className="gold-divider mt-5 w-20" />
                </div>
                <button onClick={handleLogout} className="btn-outline !py-2 !px-4 !text-sm">
                  Sign Out
                </button>
              </div>

              {/* Scanner / Status Cards */}
              <div className="gov-card mt-10 p-8">
                {/* Camera view — shown when scanning */}
                {status === "scanning" && (
                  <>
                    <div className="relative max-w-md mx-auto rounded-lg border border-border overflow-hidden">
                      <QRScanner onScan={handleScan} active={scannerActive} />
                    </div>
                    <p className="mt-6 text-center text-sm text-muted-foreground animate-pulse">
                      Point camera at a delegate's QR code
                    </p>
                  </>
                )}

                {/* Loading */}
                {status === "loading" && (
                  <div className="py-16 text-center">
                    <div className="mx-auto h-12 w-12 rounded-full border-4 border-[color:var(--gold)] border-t-transparent animate-spin" />
                    <p className="mt-4 text-sm text-muted-foreground">Verifying attendance…</p>
                  </div>
                )}

                {/* ✅ Success */}
                {status === "success" && result && (
                  <div className="text-center py-8">
                    <CheckCircle2 className="mx-auto h-20 w-20 text-emerald-600" strokeWidth={1.5} />
                    <div className="eyebrow justify-center text-emerald-700 mt-6">Verified</div>
                    <h2 className="mt-3 font-serif text-3xl text-foreground">Check-In Successful</h2>
                    <div className="mt-4 space-y-1 text-sm text-muted-foreground">
                      <p><span className="font-semibold text-foreground">{result.name}</span></p>
                      {result.event && <p>{result.event}</p>}
                      {result.time && <p>Time: {result.time}</p>}
                    </div>
                    <button onClick={handleReset} className="btn-primary mt-8">
                      <RefreshCw className="h-4 w-4" /> Scan Next
                    </button>
                  </div>
                )}

                {/* 🟡 Already checked in */}
                {status === "already" && result && (
                  <div className="text-center py-8">
                    <AlertTriangle className="mx-auto h-20 w-20 text-amber-500" strokeWidth={1.5} />
                    <div className="eyebrow justify-center text-amber-700 mt-6">Already Checked In</div>
                    <h2 className="mt-3 font-serif text-2xl text-foreground">{result.name || "Delegate"}</h2>
                    <p className="mt-2 text-sm text-muted-foreground">{result.message}</p>
                    <button onClick={handleReset} className="btn-outline mt-8">
                      <RefreshCw className="h-4 w-4" /> Scan Next
                    </button>
                  </div>
                )}

                {/* 🔴 Invalid QR */}
                {status === "invalid" && (
                  <div className="text-center py-8">
                    <XCircle className="mx-auto h-20 w-20 text-[color:var(--crimson)]" strokeWidth={1.5} />
                    <div className="eyebrow justify-center mt-6">Invalid</div>
                    <h2 className="mt-3 font-serif text-2xl text-foreground">Invalid QR Code</h2>
                    <p className="mt-2 text-sm text-muted-foreground">{result?.message || "This QR code is not recognized."}</p>
                    <button onClick={handleReset} className="btn-primary mt-8">
                      <RefreshCw className="h-4 w-4" /> Scan Again
                    </button>
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

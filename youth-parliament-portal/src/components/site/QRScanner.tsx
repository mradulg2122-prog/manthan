/**
 * QRScanner — Camera-based QR code scanner using html5-qrcode.
 * Ported from the old frontend's QRScanner component.
 *
 * Props:
 *   onScan(data: string) — called when a QR is decoded
 *   active — true = camera running, false = stopped
 */

import { useEffect, useRef, useCallback } from "react";
import { Html5Qrcode } from "html5-qrcode";

interface QRScannerProps {
  onScan: (data: string) => void;
  active: boolean;
}

const SCANNER_ID = "qr-reader";

export function QRScanner({ onScan, active }: QRScannerProps) {
  const scannerRef = useRef<Html5Qrcode | null>(null);
  const lastScanTime = useRef<number>(0);

  const handleScan = useCallback(
    (decodedText: string) => {
      // Prevent duplicate scans within 2 seconds
      const now = Date.now();
      if (now - lastScanTime.current < 2000) return;
      lastScanTime.current = now;
      onScan(decodedText);
    },
    [onScan],
  );

  useEffect(() => {
    if (!active) {
      if (scannerRef.current?.isScanning) {
        scannerRef.current.stop().catch(() => {});
      }
      return;
    }

    // Small delay to ensure the DOM element exists
    const timeout = setTimeout(() => {
      const scanner = new Html5Qrcode(SCANNER_ID);
      scannerRef.current = scanner;

      scanner
        .start(
          { facingMode: "environment" }, // rear camera
          { fps: 10, qrbox: { width: 250, height: 250 } },
          handleScan,
          () => {}, // ignore errors (no QR in frame)
        )
        .catch((err) => {
          console.error("Camera start failed:", err);
        });
    }, 300);

    return () => {
      clearTimeout(timeout);
      if (scannerRef.current?.isScanning) {
        scannerRef.current.stop().catch(() => {});
      }
    };
  }, [active, handleScan]);

  return (
    <div className="w-full flex justify-center">
      <div
        id={SCANNER_ID}
        className="w-full rounded-lg overflow-hidden"
      />
    </div>
  );
}

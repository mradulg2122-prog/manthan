"use client";

/**
 * QRScanner component — uses html5-qrcode to scan QR codes via camera.
 * Calls onScan with the decoded text when a QR is successfully read.
 */

import { useEffect, useRef, useCallback } from "react";
import { Html5Qrcode } from "html5-qrcode";

interface QRScannerProps {
  onScan: (data: string) => void;
  active: boolean; // true = camera running, false = stopped
}

const SCANNER_ID = "qr-reader";

export default function QRScanner({ onScan, active }: QRScannerProps) {
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
    [onScan]
  );

  useEffect(() => {
    if (!active) {
      // Stop if running
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
          () => {} // ignore errors (no QR in frame)
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
        className="w-full max-w-sm rounded-2xl overflow-hidden"
      />
    </div>
  );
}

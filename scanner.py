"""Scanner - Webcam QR scanning with live attendance marking."""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cv2
from services.scanner_service import ScannerService
from agents.attendance_agent import AttendanceAgent

# Cooldown between scans (seconds)
SCAN_COOLDOWN = 2


def main():
    """Start webcam and scan QR codes for attendance."""
    scanner = ScannerService()
    agent = AttendanceAgent()

    # Connect to Google Sheet once
    try:
        agent.connect()
        print("✓ Connected to Google Sheet")
    except Exception as e:
        print(f"✗ Sheet connection failed: {e}")
        return

    # Open camera
    try:
        scanner.open_camera()
    except RuntimeError as e:
        print(f"✗ {e}")
        return

    last_scanned_id = None
    last_scan_time = 0

    try:
        while True:
            frame = scanner.read_frame()
            if frame is None:
                continue

            # Scan for QR codes
            detected_ids = scanner.scan_qr(frame)

            # Draw bounding boxes on frame
            scanner.draw_box(frame, None)

            # Process first detected QR
            if detected_ids:
                reg_id = detected_ids[0]
                now = time.time()

                # Cooldown: skip if same ID scanned within SCAN_COOLDOWN seconds
                if reg_id != last_scanned_id or (now - last_scan_time) > SCAN_COOLDOWN:
                    print(f"\n✓ QR Detected: {reg_id}")

                    try:
                        result = agent.mark_attendance(reg_id)
                    except Exception as e:
                        print(f"  ✗ Error: {e}")

                    last_scanned_id = reg_id
                    last_scan_time = now

            # Show camera feed
            cv2.imshow("EventFlow AI - QR Scanner (press 'q' to quit)", frame)

            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("\n✓ Scanner stopped by user.")
                break

    except KeyboardInterrupt:
        print("\n✓ Scanner interrupted.")

    finally:
        scanner.close_camera()


if __name__ == "__main__":
    main()

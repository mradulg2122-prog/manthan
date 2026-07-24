"""Scanner Service - Webcam QR code scanning using OpenCV."""

import cv2
import numpy as np


class ScannerService:
    """Opens webcam and scans QR codes continuously."""

    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.detector = cv2.QRCodeDetector()

    def open_camera(self):
        """Open the default webcam."""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise RuntimeError(
                "Camera not found. Check your webcam connection."
            )
        print("✓ Camera opened. Press 'q' to quit.")

    def read_frame(self):
        """Read a single frame from the camera."""
        if not self.cap or not self.cap.isOpened():
            raise RuntimeError("Camera is not open.")

        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def scan_qr(self, frame):
        """Decode QR codes from a frame. Returns list of registration IDs."""
        if frame is None:
            return []

        detected_ids = []
        try:
            data, points, _ = self.detector.detectAndDecode(frame)
            if data and data.strip():
                detected_ids.append(data.strip())
        except Exception:
            pass  # Skip unreadable frames

        return detected_ids

    def draw_box(self, frame, decoded_objects=None):
        """Draw bounding boxes around detected QR codes."""
        try:
            data, points, _ = self.detector.detectAndDecode(frame)
            if points is not None and data:
                pts = points[0].astype(int)
                for i in range(len(pts)):
                    cv2.line(frame, tuple(pts[i]), tuple(pts[(i + 1) % len(pts)]), (0, 255, 0), 3)

                # Show registration ID on frame
                x, y = pts[0]
                cv2.putText(frame, data.strip(), (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        except Exception:
            pass

        return frame

    def close_camera(self):
        """Release the camera and close windows."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print("✓ Camera closed.")

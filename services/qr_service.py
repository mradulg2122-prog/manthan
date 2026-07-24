"""QR Service - Generates and saves QR code images."""

import os
import qrcode
from config import QR_OUTPUT_DIR
from constants import QR_IMAGE_SIZE


class QRService:
    """Generates QR codes containing only the registration ID."""

    def __init__(self):
        self.output_dir = str(QR_OUTPUT_DIR)
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_qr(self, registration_id):
        """Generate a QR code image for the given registration ID."""
        if not registration_id:
            raise ValueError("registration_id is required to generate a QR code.")

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(registration_id)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize(QR_IMAGE_SIZE)
            return img

        except Exception as e:
            raise RuntimeError(f"QR generation failed for {registration_id}: {e}")

    def save_qr(self, registration_id):
        """Generate and save QR image. Returns the saved file path."""
        img = self.generate_qr(registration_id)
        filename = f"{registration_id}.png"
        filepath = os.path.join(self.output_dir, filename)

        try:
            img.save(filepath)
        except Exception as e:
            raise IOError(f"Failed to save QR image at {filepath}: {e}")

        return filepath

"""
QR Code Service.
Generates and saves QR code images for registration IDs.
"""

import os
import qrcode

# QR images are saved here (relative to backend/)
QR_OUTPUT_DIR = os.path.join("generated", "qr")
QR_IMAGE_SIZE = (300, 300)


def generate_and_save_qr(registration_id: str) -> str:
    """
    Generate a QR code for the registration ID and save it as a PNG.
    Returns the file path of the saved image.
    """
    os.makedirs(QR_OUTPUT_DIR, exist_ok=True)

    # Build QR
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

    # Save
    filepath = os.path.join(QR_OUTPUT_DIR, f"{registration_id}.png")
    img.save(filepath)

    return filepath

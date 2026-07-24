"""
Pydantic schema for the scan request.
"""

from pydantic import BaseModel


class ScanRequest(BaseModel):
    """Request body for POST /scan."""
    registration_id: str

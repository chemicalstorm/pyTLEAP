"""Implement an API wrapper for accessing a TP-Link EAP."""
from pathlib import Path

from .eap import EAP
from .error import CommunicationError, PytleapError

__all__ = [
    "EAP",
    "PytleapError",
    "CommunicationError",
]

__version__ = (Path(__file__).parent / "VERSION").read_text().strip()

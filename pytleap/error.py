"""Define errors and exceptions."""


class PytleapError(Exception):
    """Base error"""


class CommunicationError(PytleapError):
    """Error when communicating with the EAP device."""

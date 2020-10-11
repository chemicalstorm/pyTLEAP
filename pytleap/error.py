"""Define errors and exceptions."""

from pexpect import ExceptionPexpect, TIMEOUT
from pexpect import pxssh


class PytleapError(Exception):
    """Base error"""
    def __init__(self, message, cause=None):
        self.message = message
        self.cause = cause

    def __str__(self):
        if self.cause:
            return f"{self.message} ({self.cause})"
        else:
            return self.message


class CommunicationError(PytleapError):
    """Error when communicating with the EAP device."""


class TimeoutError(CommunicationError):
    """Error when there is a timeout"""


class AuthenticationError(PytleapError):
    """Error when itś impossible to authenticate (invalid/wrong credentials"""


def convert_pexpect_exception(message: str, err: ExceptionPexpect) -> PytleapError:
    """Given a Pexpect exception, return the corresponding PytleapError."""
    if isinstance(err, TIMEOUT):
        return TimeoutError(message, err)
    elif isinstance(err, pxssh.ExceptionPxssh):
        value = err.value
        if value in ['password refused', 'permission denied']:
            return AuthenticationError(message, err)
    elif isinstance(err, pxssh.EOF):
        return CommunicationError(message, "End Of File")

    return CommunicationError(message)

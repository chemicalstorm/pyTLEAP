"""Represents the EAP device."""

from pexpect import pxssh

from .client import Client
from .error import CommunicationError
from .utils import process_wlanconfig


class Eap:
    """ Model of an EAP device"""

    def __init__(self, host: str, username: str, password: str, port: int = 22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

        self.timeout = 30

        self.wifi_interfaces = ["ath0", "ath10"]

        self.ssh_session = None
        self.is_connected = False

    def set_timeout(self, timeout: int):
        """Set the timeout for communications with this EAP device."""
        self.timeout = timeout

    def connect(self):
        """Connect to the EAP device."""
        if self.is_connected:
            return

        self.ssh_session = pxssh.pxssh(
            echo=False, encoding="utf-8", timeout=self.timeout
        )
        self.ssh_session.force_password = True

        try:
            self.ssh_session.login(
                self.host,
                self.username,
                self.password,
                port=self.port,
                login_timeout=self.timeout,
            )
        except pxssh.ExceptionPexpect as err:
            raise CommunicationError("Cannot login") from err
        self.is_connected = True

    def disconnect(self):
        """Close the connection to the EAP device."""
        if not self.is_connected:
            return

        try:
            self.ssh_session.logout()
        except pxssh.ExceptionPexpect:
            # Ignore error, as we are logging out anyway
            pass

        self.is_connected = False
        self.ssh_session = None

    def get_wifi_clients(self, interfaces: [str] = None) -> [Client]:
        """Retrieve the list of connected Wifi clients."""
        if not self.is_connected:
            self.connect()

        client_list = []
        try:
            for iface in interfaces or self.wifi_interfaces:
                self.ssh_session.sendline(f"wlanconfig {iface} list")
                self.ssh_session.prompt(self.timeout)
                client_list.extend(process_wlanconfig(self.ssh_session.before))
        except pxssh.ExceptionPexpect as err:
            raise CommunicationError("Cannot retrieve client list") from err

        return client_list

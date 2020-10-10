"""Model of a Wifi client"""
# pylint: disable=R0903


class Client:
    """Represent a client of the EAP."""

    def __init__(self, entry):
        self.entry = entry

    @property
    def mac_address(self) -> str:
        """Return the MAC address of the device"""
        return self.entry.get("ADDR", "Unknown")

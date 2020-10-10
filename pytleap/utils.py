"""Collection of utility functions"""

from .client import Client

HEADERS = [
    "ADDR",
    "AID",
    "CHAN",
    "TXRATE",
    "RXRATE",
    "RSSI",
    "MINRSSI",
    "MAXRSSI",
    "IDLE",
    "TXSEQ",
    "RXSEQ",
    "CAPS",
    "ACAPS",
    "ERP",
    "STATE",
    "MAXRATE(DOT11)",
    "HTCAPS",
    "ASSOCTIME",
    "IEs",
    "MODE",
    "PSMODE",
    "RXNSS",
    "TXNSS",
]


def process_wlanconfig(wlanconfig) -> [Client]:
    """Process the output of the `wlanconfig` command"""
    # Replace double newline characters
    wlanconfig.replace("\n\n", "\n")
    lines = wlanconfig.splitlines()
    if len(lines) < 2:
        # No clients connected!
        return []
    client_list = []
    for entry in lines[1:]:
        data = dict(zip(HEADERS, entry.split()))
        if not data:  # Empty line
            continue
        client_list.append(Client(data))

    return client_list

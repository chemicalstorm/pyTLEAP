"""Provide a CLI for PyTLEAP."""
import argparse
from pprint import pprint

from .eap import Eap

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", metavar="IP", type=str, required=True, help="IP Address of your EAP device"
    )
    parser.add_argument(
        "--user", "-u", type=str, required=True, help="Username to access the EAP SSH server"
    )
    parser.add_argument(
        "--password", "-p", type=str, required=True, help="Password to access the EAP SSH server"
    )
    parser.add_argument(
        "--port", type=int, default=22, help="Port used by the EAP SSH server"
    )

    parser.add_argument(
        "--timeout", type=int, help="Timeout for communication with EAP device"
    )

    parser.add_argument(
        "--interface",
        "-i",
        action="append",
        nargs="+",
        type=str,
        help="Wifi interface to query",
    )

    args = parser.parse_args()

    eap = Eap(args.host, args.user, args.password, args.port)
    if args.timeout:
        eap.set_timeout(args.timeout)
    eap.connect()

    clients = eap.get_wifi_clients(args.interface)

    eap.disconnect()

    print(f"{len(clients)} connected clients:")
    pprint([c.mac_address for c in clients])

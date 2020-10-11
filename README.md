# pytleap
Interface to communicate with a TP-Link EAP access point.

This project aims to create an API to programmatically access the configuration of a [TP-Link EAP](https://www.tp-link.com/us/business-networking/ceiling-mount-access-point/) access point.

## Requirements
- Python
- aiohttp

## Supported hardware
Development of this library is done with an EAP245 v3.

## Limitations
This library uses the web admin interface to access the information of the access point.
It appears that the webserver implementation does not support concurrent connections.

In the [ssh-access](https://github.com/chemicalstorm/pytleap/tree/ssh-access) branch is an implementation that makes
 use of SSH to connect to the device. There is no issue with concurrent access when using a SSH connection, however
  available data is very limited.
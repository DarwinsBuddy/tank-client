# tank

# Dependencies

## Building
* npm / node 16.6.2
* python3.9+
## Installation
* (optional) systemd

# Install / Start

## systemd
1. `sudo ./install.sh`
> service name: `tank-client.service`
## only as python module

`python setup.py install`

`python -m tank-client`
# Uninstall
## systemd
`sudo ./uninstall.sh`
## only as python module
`pip uninstall tank`
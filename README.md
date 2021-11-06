# tank

# Dependencies

## Building
* python3.7+
## Installation
* required `pigpiod`
* (optional) systemd

# Install / Start

## systemd
1. `sudo ./install.sh`
> service name: `tank-client.service`
## only as python module

`python3 setup.py install`

`python3 -m tank-client`
# Uninstall
## systemd
`sudo ./uninstall.sh`
## only as python module
`pip uninstall tank`
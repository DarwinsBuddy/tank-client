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

# Config
Choose between 2 modes:

## server mode (server)
Use [tank](https://github.com/DarwinsBuddy/tank) for accessing the data in `m`

## home assistant (ha)
* Install [mosquitto](https://www.home-assistant.io/docs/mqtt/broker/) Add-On in `home-assistant`
* Configure it
> Logins
> ```
> - username: <mqtt-user>
>   password: <mqtt-pw>
> ```
* Register your sensors in `configuration.yaml` of home assistant as documented [here](https://github.com/DarwinsBuddy/tank/tree/main/tank/data/homeassistant/configuration.yaml)
* Use it by providing at least `-mb=<broker-ip>`
  use `-mu=<mqtt-user> -mp=<mqtt-pw>` (recommended) for authentication if configured
  Data in `cm`
`python3 -m tank-client`
# Uninstall
## systemd
`sudo ./uninstall.sh`
## only as python module
`pip uninstall tank`
#!/bin/bash

SERVICE="tank-client.service"
SERVICE_FILE="./tank/resources/${SERVICE}"
# uninstall python package
sudo pip uninstall tank-client
# disable and stop service
sudo systemctl stop ${SERVICE}
sudo systemctl disable ${SERVICE}
sudo systemctl daemon-reload

# rm service file into systemd
sudo rm "/etc/systemd/system/${SERVICE}"
#!/bin/bash

SERVICE="tank-client.service"
SERVICE_FILE="./tank/resources/${SERVICE}"
# install python package
sudo python setup.py install
# copy service file into systemd
sudo cp ${SERVICE_FILE} /etc/systemd/system/
# enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE}
sudo systemctl restart ${SERVICE}

#!/usr/bin/env bash
# Deletes related created systemd timer & service. 

service_name=contrib-writer

systemctl disable --user $service_name.timer
systemctl stop --user $service_name.timer

sudo rm /usr/lib/systemd/user/$service_name.service
sudo rm /usr/lib/systemd/user/$service_name.timer

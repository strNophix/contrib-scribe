#!/usr/bin/env bash
# Sets up the necessary systemd timer & service. 

service_name=contrib-writer

sudo tee /usr/lib/systemd/user/$service_name.service &>/dev/null <<EOF
[Unit]
Description=Your contribution heatmap is a canvas for creativity.

[Service]
ExecStart=$(pwd)/contrib_scribe.py $(pwd)/config.ini 
EOF

sudo tee /usr/lib/systemd/user/$service_name.timer &>/dev/null <<EOF
[Unit]
Description=Your contribution heatmap is a canvas for creativity.

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl enable --user contrib-writer.timer --now

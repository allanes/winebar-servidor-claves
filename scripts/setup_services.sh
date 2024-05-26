#!/bin/bash

# Define the paths for your script files
SCRIPTS_PATH="/home/admin/Desktop/winebar-servidor-claves/scripts"
RUN_BACKEND_SCRIPT="$SCRIPTS_PATH/linux_iniciar_backend.sh"
RUN_ABRIR_VISTA_TAPERO_SCRIPT="$SCRIPTS_PATH/abrir_teles.sh"

# Replace 'your_user' with your Linux username
USERNAME="admin"

# Create the systemd service files
cat << EOF | sudo tee /etc/systemd/system/servidor_claves.service
[Unit]
Description=Run backend service
After=network.target

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$SCRIPTS_PATH
ExecStart=/bin/bash $RUN_BACKEND_SCRIPT
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create the systemd service files
cat << EOF | sudo tee /etc/systemd/system/abrir_vista_tapero.service
[Unit]
Description=Run tapero view
After=network.target

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$SCRIPTS_PATH
ExecStartPre=/bin/sleep 30
ExecStart=/bin/bash $RUN_ABRIR_VISTA_TAPERO_SCRIPT
Restart=no

[Install]
WantedBy=multi-user.target
EOF

cat << EOF | sudo tee /etc/systemd/system/auto_update.service
[Unit]
Description=Automatic System Updates
After=network.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c '/usr/bin/apt-get update && /usr/bin/apt-get upgrade -y'
RemainAfterExit=true
User=root

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the services
sudo systemctl daemon-reload
sudo systemctl enable auto_update.service
sudo systemctl enable servidor_claves.service
sudo systemctl enable abrir_vista_tapero.service

echo "Services have been created and enabled. Restart system to check startup."

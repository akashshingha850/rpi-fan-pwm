
#!/bin/bash

# Define variables
REPO_URL="https://github.com/akashshingha850/rpi-fan-pwm.git"
CLONE_DIR="/home/pi/rpi-fan-pwm"
SERVICE_NAME="rpi-fan-pwm"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

# Function to handle errors
handle_error() {
    echo "Error: $1"
    exit 1
}

# Clone the repository
echo "Cloning the repository..."
git clone $REPO_URL $CLONE_DIR || handle_error "Failed to clone the repository."

# Create the systemd service file
echo "Creating the systemd service file..."
sudo bash -c "cat > $SERVICE_FILE <<EOL
[Unit]
Description=Raspberry Pi Fan PWM Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 $CLONE_DIR/fan_control.py
WorkingDirectory=$CLONE_DIR
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOL" || handle_error "Failed to create the systemd service file."

# Reload systemd to recognize the new service
echo "Reloading systemd..."
sudo systemctl daemon-reload || handle_error "Failed to reload systemd."

# Enable the service to start on boot
echo "Enabling the service to start on boot..."
sudo systemctl enable $SERVICE_NAME || handle_error "Failed to enable the service."

# Start the service immediately
echo "Starting the service..."
sudo systemctl start $SERVICE_NAME || handle_error "Failed to start the service."

echo "Service $SERVICE_NAME has been created, enabled, and started successfully."

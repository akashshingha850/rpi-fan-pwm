#!/bin/bash

# Define variables
SERVICE_NAME="rpi-fan-pwm"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
CLONE_DIR="/home/pi/rpi-fan-pwm"

# Function to handle errors
handle_error() {
    echo "Error: $1"
    exit 1
}

# Stop the service
echo "Stopping the service..."
sudo systemctl stop $SERVICE_NAME || handle_error "Failed to stop the service."

# Disable the service
echo "Disabling the service..."
sudo systemctl disable $SERVICE_NAME || handle_error "Failed to disable the service."

# Remove the systemd service file
echo "Removing the systemd service file..."
sudo rm $SERVICE_FILE || handle_error "Failed to remove the systemd service file."

# Reload systemd to apply changes
echo "Reloading systemd..."
sudo systemctl daemon-reload || handle_error "Failed to reload systemd."

# Remove the cloned repository
echo "Removing the cloned repository..."
rm -rf $CLONE_DIR || handle_error "Failed to remove the cloned repository."

echo "Service $SERVICE_NAME has been stopped, disabled, and uninstalled successfully."

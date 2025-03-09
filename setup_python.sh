#!/bin/bash

# This script installs Python and required dependencies for face swapping

# Update package lists
echo "Updating package lists..."
sudo apt-get update

# Install Python and pip if not already installed
echo "Installing Python and pip..."
sudo apt-get install -y python3 python3-pip

# Install required Python packages
echo "Installing required Python packages..."
pip3 install -r requirements.txt

# Make uploads directory if it doesn't exist
echo "Creating uploads directory..."
mkdir -p uploads
chmod 777 uploads

echo "Setup complete! You can now run the face swap application."

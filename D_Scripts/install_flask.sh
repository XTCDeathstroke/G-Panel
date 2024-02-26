#!/bin/bash

# Function to display error message and exit
display_error() {
    echo "Error: $1"
    exit 1
}

# Update package lists
sudo apt update || display_error "Failed to update package lists."

# Install Python 3 and pip
sudo apt install -y python3 python3-pip || display_error "Failed to install Python 3 and pip."

# Install Flask using pip
sudo pip3 install Flask || display_error "Failed to install Flask."

echo "Installation successful."


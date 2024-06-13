#!/bin/bash

# Define the source file and the destination
SOURCE_FILE="main.py"
DESTINATION="/usr/local/bin/gif-cli"

# Check if the source file exists
if [[ ! -f $SOURCE_FILE ]]; then
    echo "Error: Source file '$SOURCE_FILE' not found!"
    exit 1
fi

# Copy the file to /usr/local/bin
sudo cp $SOURCE_FILE $DESTINATION

# Make the file executable
sudo chmod +x $DESTINATION

echo "Installation complete."

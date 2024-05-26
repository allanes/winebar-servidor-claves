#!/bin/bash

# Set the environment variable for XWayland
export GDK_BACKEND=x11
export DISPLAY=:0

# Launch the Chrome windows on each screen using the position and size information
chromium-browser --new-window --start-fullscreen

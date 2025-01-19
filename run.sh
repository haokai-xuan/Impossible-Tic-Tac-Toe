#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3."
    exit 1
fi

if ! python3 -c "import pygame" &> /dev/null; then
    echo "Pygame is not installed. Installing Pygame..."
    python3 -m pip install pygame
fi

python3 main.py

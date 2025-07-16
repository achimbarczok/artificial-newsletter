#!/bin/bash
# Generic newsletter runner script
# Automatically detects script directory and runs from there

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to script directory
cd "$SCRIPT_DIR"

# Activate virtual environment (if exists)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run newsletter generator
python newsletter_generator.py

# Log completion with timestamp
echo "Newsletter sent at $(date)" >> newsletter.log

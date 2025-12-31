#!/bin/bash

# ==========================================
# 1. Forcefully prohibit running this script with sudo
# ==========================================
if [ "$EUID" -eq 0 ]; then
  echo "❌ Error: Please DO NOT run this script with sudo."
  echo "   Use: bash add_to_sys.sh"
  echo "   (The script will ask for sudo password when needed)"
  exit 1
fi

# ==========================================
# 2. Obtain variables in the regular user environment (critical step)
# ==========================================
# Since it's currently running as a regular user, $(which python) can get the Conda path
PYTHON_PATH=$(which python)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="/usr/local/bin/amadeus"

# Check if the correct python path was obtained to prevent empty values
if [ -z "$PYTHON_PATH" ]; then
    echo "❌ Error: Could not find python path. Is Conda activated?"
    exit 1
fi

echo "✅ Detected Python: $PYTHON_PATH"
echo "✅ Detected Script: $SCRIPT_DIR/Amadeus_rebuild.py"

# ==========================================
# 3. Use sudo for file write operations
# ==========================================
echo "🚀 Creating/Updating startup script at $TARGET..."

# Prepare the content to be written
CONTENT="#!/bin/bash
$PYTHON_PATH $SCRIPT_DIR/Amadeus_rebuild.py \"\$@\""

# Use sudo tee to write the file (only this step requires root privileges)
# Note: The user will be prompted for a password here
echo "$CONTENT" | sudo tee "$TARGET" > /dev/null

# Grant execution permission
sudo chmod +x "$TARGET"

echo "✨ Success! You can now run 'amadeus' from anywhere."

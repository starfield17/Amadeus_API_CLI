#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="/usr/local/bin/amadeus"
# Get the absolute path of the current environment's Python
PYTHON_PATH=$(which python)

if [ -f "$TARGET" ]; then
    echo "The script already exists at $TARGET. Updating..."
    # If the file exists, force overwrite to update the path
    echo "#!/bin/bash" | sudo tee "$TARGET" > /dev/null
    # Use the absolute path PYTHON_PATH
    echo "$PYTHON_PATH $SCRIPT_DIR/Amadeus_rebuild.py" | sudo tee -a "$TARGET" > /dev/null
    sudo chmod +x "$TARGET"
    echo "Updated $TARGET to use python at: $PYTHON_PATH"
else
    echo "#!/bin/bash" | sudo tee "$TARGET" > /dev/null
    echo "$PYTHON_PATH $SCRIPT_DIR/Amadeus_rebuild.py" | sudo tee -a "$TARGET" > /dev/null
    sudo chmod +x "$TARGET"
    echo "Soft link created at $TARGET using python: $PYTHON_PATH"
fi

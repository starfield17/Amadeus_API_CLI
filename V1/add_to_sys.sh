#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="/usr/local/bin/amadeus"
if [ -f "$TARGET" ]; then
    echo "The script already exists at $TARGET. No changes made."
else
    echo "#!/bin/bash" | sudo tee "$TARGET" > /dev/null
    echo "python3 $SCRIPT_DIR/Deep_seek_api_rebuild.py" | sudo tee -a "$TARGET" > /dev/null
    sudo chmod +x "$TARGET"
    echo "Soft link created at $TARGET"
fi

#!/bin/bash

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TARGET_FILE="${SCRIPT_DIR}/V1/Deep_seek_api.py"
LINK_NAME="deepseek-cli"
BIN_DIR="${HOME}/.local/bin"

# Create bin directory if it doesn't exist
mkdir -p "${BIN_DIR}"

# Make Python file executable
chmod +x "${TARGET_FILE}"

# Add shebang if not present
if ! head -n1 "${TARGET_FILE}" | grep -q "^#!/usr/bin/env python"; then
    sed -i '1i#!/usr/bin/env python' "${TARGET_FILE}"
fi

# Create symbolic link
ln -sf "${TARGET_FILE}" "${BIN_DIR}/${LINK_NAME}"

# Add bin directory to PATH if not already present
if ! grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" ~/.bashrc; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo "Added ~/.local/bin to PATH. Please restart your terminal or run: source ~/.bashrc"
fi

echo "Installation complete. You can now use '${LINK_NAME}' command."

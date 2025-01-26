#!/bin/bash
# Install required Python packages using USTC PyPI mirror
pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple \
    openai \
    rich \
    prompt_toolkit \
    httpx \
    httpx-socks \
    pygments \
    pyperclip
echo "All dependencies installed successfully!"

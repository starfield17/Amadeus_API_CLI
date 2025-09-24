#!/bin/bash
# Install required Python packages using USTC PyPI mirror
pip install -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/web/simple
echo "All dependencies installed successfully!"

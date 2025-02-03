#!/bin/bash

# 获取当前脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 定义软链接的目标路径
TARGET="/usr/local/bin/askds"

# 检查目标文件是否已经存在
if [ -f "$TARGET" ]; then
    echo "The script already exists at $TARGET. No changes made."
else
    # 创建一个启动脚本来运行当前环境的 python
    echo "#!/bin/bash" | sudo tee "$TARGET" > /dev/null
    echo "python3 $SCRIPT_DIR/Deep_seek_api.py" | sudo tee -a "$TARGET" > /dev/null

    # 给软链接和脚本添加执行权限
    sudo chmod +x "$TARGET"

    echo "Soft link created at $TARGET"
fi

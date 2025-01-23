# DEEPSEEK_API_CLI
一个基于命令行的 DeepSeek AI 聊天应用程序，支持与 DeepSeek 模型进行交互、保存对话历史，以及其他实用功能。

## 功能特点

- 支持与 DeepSeek AI 模型实时对话
- 流式输出响应
- 保存和加载对话历史
- 简单直观的命令行界面
- 支持中断操作（Ctrl+C）
- 丰富的命令支持

## 环境要求

- Python 3.7+
- pip（Python 包管理器）

## 安装步骤

1. 克隆或下载项目到本地

2. 安装所需依赖：
```bash
pip install openai rich prompt_toolkit
```

## 配置

在运行程序前，你需要：

1. 获取 DeepSeek API 密钥
2. 确保有可用的网络连接

## 使用方法

### 基本运行

使用以下命令启动应用：

```bash
python chat_cli.py --api-key YOUR_API_KEY
```

可选参数：
- `--model`: 指定使用的模型（默认为 "deepseek-reasoner"）

例如：
```bash
python chat_cli.py --api-key YOUR_API_KEY --model custom-model-name
```

### 可用命令

在聊天界面中可以使用以下命令：

- `/clear`: 清除当前对话历史
- `/save [文件名]`: 保存对话历史（默认保存为 chat_history.json）
- `/load [文件名]`: 加载已保存的对话历史（默认加载 chat_history.json）
- `/help`: 显示帮助信息
- `q` 或 `exit`: 退出程序

### 示例用法

1. 启动程序：
```bash
python chat_cli.py --api-key sk-xxxxx
```

2. 开始对话：
```
您: 你好
助手: 你好！有什么我可以帮你的吗？

您: /save my_chat.json
对话已保存至 my_chat.json

您: /clear
已清除对话历史
```

## 错误处理

程序会处理常见的错误情况：

- API 错误：显示具体的错误信息
- 文件操作错误：当保存/加载对话历史出现问题时提供反馈
- 网络连接问题：显示相关错误信息


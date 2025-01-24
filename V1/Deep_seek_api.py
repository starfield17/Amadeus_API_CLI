import os
import argparse
import json
from openai import OpenAI
from typing import List, Dict, Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import signal
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
import httpx
from httpx_socks import SyncProxyTransport

class ChatModel:
    def __init__(self, api_key: str, model: str = "deepseek-reasoner", proxy: str = None):
        if proxy and proxy.startswith('socks'):
            transport = SyncProxyTransport.from_url(proxy)
            http_client = httpx.Client(transport=transport)
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com",
                http_client=http_client
            )
        else:
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
        self.model = model

    def get_response(self, messages: List[Dict]) -> Optional[str]:
        try:
            return self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
        except Exception as e:
            raise Exception(f"API错误: {str(e)}")

class ChatHistory:
    def __init__(self):
        self.messages = [{"role": "system", "content": "You are a helpful assistant"}]
        
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        
    def clear(self):
        self.messages = [{"role": "system", "content": "You are a helpful assistant"}]
        
    def save(self, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
            
    def load(self, filename: str):
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                self.messages = json.load(f)
                return True
        return False

class ChatUI:
    def __init__(self):
        self.console = Console()
        
    def display_message(self, content: str, style: str = None, end="\n"):
        self.console.print(content, style=style, end=end)
        
    def display_prompt(self) -> str:
        session = PromptSession()
        return session.prompt("\nUser: ").strip()
        
    def display_welcome(self, model: str):
        welcome_text = f"""
        DeepSeek Chat CLI (模型: {model})
        输入 'q' 或 'exit' 退出
        命令:
         - /clear : 清除对话历史
         - /save  : 保存对话历史
         - /load  : 加载对话历史
         - /help  : 显示帮助
        """
        self.console.print(Panel.fit(welcome_text, title="欢迎", border_style="blue"))

class ChatApp:
    def __init__(self, api_key: str, model: str = "deepseek-reasoner", proxy: str = None):
        self.model = ChatModel(api_key, model, proxy)
        self.history = ChatHistory()
        self.ui = ChatUI()
        signal.signal(signal.SIGINT, self._handle_interrupt)
        
    def _handle_interrupt(self, signum, frame):
        self.ui.display_message("\n\n会话已终止", style="yellow")
        exit(0)
        
    def handle_user_input(self, user_input: str) -> bool:
        if user_input.startswith("/"):
            cmd = user_input[1:]
            if cmd == "clear":
                self.history.clear()
                self.ui.display_message("已清除对话历史", style="yellow")
            elif cmd.startswith("save"):
                filename = cmd.split(maxsplit=1)[1] if len(cmd.split()) > 1 else "chat_history.json"
                self.history.save(filename)
                self.ui.display_message(f"对话已保存至 {filename}", style="green")
            elif cmd.startswith("load"):
                filename = cmd.split(maxsplit=1)[1] if len(cmd.split()) > 1 else "chat_history.json"
                if self.history.load(filename):
                    self.ui.display_message("已加载对话历史", style="green")
                else:
                    self.ui.display_message(f"找不到文件: {filename}", style="red")
            elif cmd == "help":
                self.ui.display_welcome(self.model.model)
            return True
        return False

    def chat(self):
        self.ui.display_welcome(self.model.model)
        while True:
            try:
                user_input = self.ui.display_prompt()
                
                if user_input.lower() in ['q', 'quit', 'exit']:
                    if Prompt.ask("确定要退出吗? (y/n)", choices=["y", "n"], default="n") == "y":
                        self.ui.display_message("\n再见!", style="yellow")
                        break
                    continue
                
                if not user_input:
                    continue
                    
                if self.handle_user_input(user_input):
                    continue
                
                self.history.add_message("user", user_input)
                self.ui.display_message("\nChat: ", style="bold blue", end="")
                
                response = self.model.get_response(self.history.messages)
                full_response = ""
                
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        self.ui.display_message(content, end="")
                        full_response += content
                
                if full_response:
                    self.history.add_message("assistant", full_response)
                    self.ui.display_message("")
                else:
                    self.ui.display_message("错误: 未收到响应", style="red")
                    
            except Exception as e:
                self.ui.display_message(f"\n错误: {str(e)}", style="red")

def main():
    parser = argparse.ArgumentParser(description="DeepSeek Chat CLI")
    parser.add_argument("--api-key", required=True, help="DeepSeek API密钥")
    parser.add_argument("--model", default="deepseek-reasoner", help="使用的模型")
    parser.add_argument("--proxy", help="代理服务器地址 (例如: socks5://127.0.0.1:7890)")
    args = parser.parse_args()
    
    app = ChatApp(api_key=args.api_key, model=args.model, proxy=args.proxy)
    app.chat()

if __name__ == "__main__":
    main()

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
from pathlib import Path
import readline
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import Terminal256Formatter
from enum import Enum, auto
class InputState(Enum):
    NORMAL = auto()      # 普通输入状态
    MULTILINE = auto()   # 多行输入状态（通过Shift+Enter触发）
    CODE_BLOCK = auto()  # 代码块状态（被```包围）
    PASTE = auto()       # 粘贴状态（通过ctrl+v/cmd+v触发）

class InputEvent(Enum):
    ENTER = auto()       # 回车键
    SHIFT_ENTER = auto() # Shift+Enter组合键
    PASTE_START = auto() # 开始粘贴
    PASTE_END = auto()   # 结束粘贴
    CODE_START = auto()  # 代码块开始
    CODE_END = auto()    # 代码块结束
    EMPTY = auto()       # 空行输入

class InputHandler:
    def __init__(self):
        self.state = InputState.NORMAL
        self.buffer = []
        self.code_lang = None
        
    def handle_input(self, line: str) -> tuple[bool, str]:
        """处理输入并决定是否应该发送消息
        Args:
            line: 输入的文本行
        Returns:
            (should_send, processed_line): should_send表示是否应该发送消息，
            processed_line是处理后的文本行
        """
        events = self._detect_events(line)
        return self._process_events(events, line)
    
    def _detect_events(self, line: str) -> list[InputEvent]:
        """检测输入行中的所有事件
        可能同时存在多个事件，如粘贴的内容中包含代码块
        """
        events = []
        
        # 检测粘贴事件
        if '\x1b[200~' in line:
            events.append(InputEvent.PASTE_START)
        if '\x1b[201~' in line:
            events.append(InputEvent.PASTE_END)
            
        # 检测Shift+Enter
        if line.endswith('\x1b[13;2u'):
            events.append(InputEvent.SHIFT_ENTER)
            
        # 检测代码块
        if line.strip().startswith('```'):
            events.append(InputEvent.CODE_START if self.state != InputState.CODE_BLOCK 
                        else InputEvent.CODE_END)
            
        # 检测空行
        if not line.strip():
            events.append(InputEvent.EMPTY)
        else:
            events.append(InputEvent.ENTER)
            
        return events
    
    def _process_events(self, events: list[InputEvent], line: str) -> tuple[bool, str]:
        """根据当前状态和触发的事件决定行为"""
        processed_line = line
        should_send = False
        
        for event in events:
            if event == InputEvent.PASTE_START:
                self.state = InputState.PASTE
                processed_line = line.replace('\x1b[200~', '')
                continue
                
            if event == InputEvent.PASTE_END:
                self.state = InputState.NORMAL
                processed_line = processed_line.replace('\x1b[201~', '')
                # 粘贴结束不自动发送，等待用户确认
                continue
                
            if event == InputEvent.SHIFT_ENTER:
                if self.state == InputState.NORMAL:
                    self.state = InputState.MULTILINE
                processed_line = processed_line[:-8]  # 移除Shift+Enter标记
                continue
                
            if event == InputEvent.CODE_START:
                self.state = InputState.CODE_BLOCK
                self.code_lang = processed_line[3:].strip()
                continue
                
            if event == InputEvent.CODE_END:
                self.state = InputState.NORMAL
                continue
                
            # 空行处理
            if event == InputEvent.EMPTY:
                if self.state == InputState.MULTILINE:
                    should_send = True
                elif len(self.buffer) > 0:  # 有之前的输入
                    should_send = True
                continue
                
            # 普通回车处理
            if event == InputEvent.ENTER:
                if self.state == InputState.NORMAL and processed_line.strip():
                    should_send = True
                    
        return should_send, processed_line

class ChatUI:
    def __init__(self):
        self.console = Console()
        self.buffer = []
        self.input_handler = InputHandler()
        
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind('set enable-bracketed-paste on')
        
        self.history_file = os.path.expanduser('~/.chat_history')
        if os.path.exists(self.history_file):
            readline.read_history_file(self.history_file)
    
    def display_prompt(self) -> str:
        self.buffer = []
        
        while True:
            try:
                prompt = "User: " if not self.buffer else "... "
                line = input(prompt)
                
                should_send, processed_line = self.input_handler.handle_input(line)
                
                if processed_line.strip() or self.input_handler.state != InputState.NORMAL:
                    self.buffer.append(processed_line)
                
                if should_send and self.buffer:  # 只有buffer非空时才发送
                    break
                    
            except EOFError:
                return "exit"
            except KeyboardInterrupt:
                self.buffer = []
                print("\n")
                self.input_handler.state = InputState.NORMAL
                continue
                
        return '\n'.join(filter(None, self.buffer))

    
    def __del__(self):
        readline.write_history_file(self.history_file)
        
    def display_message(self, content: str, style: str = None, end="\n", flush=False):
        if flush:
            print(content, end=end, flush=True)
        else:
            self.console.print(content, style=style, end=end)

    def display_reasoning(self, content: str):
        self.console.print("\n[Reasoning Chain]", style="bold yellow")
        self.console.print(Panel.fit(content, border_style="yellow"))

    def highlight_code(self, code: str, language: str = 'python') -> str:
        try:
            lexer = get_lexer_by_name(language)
            return highlight(code, lexer, Terminal256Formatter())
        except:
            return code


    def display_welcome(self, model: str):
        welcome_text = f"""
        DeepSeek Chat CLI (Model: {model})
        Enter 'q' or 'exit' or 'quit' to quit
        Commands:
         - /clear : Clear chat history
         - /save  : Save chat history
         - /load  : Load chat history
         - /help  : Show help
        Shortcuts:
         - Shift+Enter: New line
         - Up/Down: Navigate history
        """
        self.console.print(Panel.fit(welcome_text, title="Welcome", border_style="blue"))


class ConfigManager:
    def __init__(self):
        self.config_file = Path.home() / '.deepseek_config'
        self.default_config = {
            "api_key": "",
            "proxy": None
        }
    
    def save_config(self, api_key: str = None, proxy: str = None) -> None:
        """Save configuration to hidden file in user's home directory"""
        try:
            config = self.load_config()
            if api_key is not None:
                config["api_key"] = api_key
            if proxy is not None:
                config["proxy"] = proxy
                
            self.config_file.write_text(json.dumps(config))
            self.config_file.chmod(0o600)  # Set file permissions to owner read/write only
        except Exception as e:
            raise Exception(f"Failed to save config: {str(e)}")
    
    def load_config(self) -> dict:
        """Load configuration from hidden file"""
        try:
            if self.config_file.exists():
                config = json.loads(self.config_file.read_text())
                return {**self.default_config, **config}
            return self.default_config.copy()
        except Exception as e:
            raise Exception(f"Failed to load config: {str(e)}")
            
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
            raise Exception(f"API Error: {str(e)}")

class ChatHistory:
    def __init__(self):
        self.messages = [{"role": "system", "content": "You are a helpful assistant"}]
        self.reasoning_history = []
        
    def add_message(self, role: str, content: str, reasoning_content: str = None):
        self.messages.append({"role": role, "content": content})
        if reasoning_content:
            # Store reasoning chain without adding to messages to avoid API errors
            self.reasoning_history.append({"role": role, "reasoning_content": reasoning_content})
        
    def clear(self):
        self.messages = [{"role": "system", "content": "You are a helpful assistant"}]
        self.reasoning_history = []
        
    def save(self, filename: str):
        data = {
            "messages": self.messages,
            "reasoning_history": self.reasoning_history
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    def load(self, filename: str):
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.messages = data.get("messages", [])
                self.reasoning_history = data.get("reasoning_history", [])
                return True
        return False


class ChatApp:
    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-reasoner", proxy: str = None):
        self.config_manager = ConfigManager()
        config = self.config_manager.load_config()
        
        if api_key is None:
            api_key = config["api_key"]
            if not api_key:
                console = Console()
                api_key = Prompt.ask("Please enter your DeepSeek API key")
                self.config_manager.save_config(api_key=api_key)
                console.print("API key saved successfully!", style="green")
        else:
            self.config_manager.save_config(api_key=api_key)
            
        if proxy is None:
            proxy = config["proxy"]
        else:
            self.config_manager.save_config(proxy=proxy)
        
        self.model = ChatModel(api_key, model, proxy)
        self.history = ChatHistory()
        self.ui = ChatUI()
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def chat(self):
        self.ui.display_welcome(self.model.model)
        while True:
            try:
                user_input = self.ui.display_prompt()
                
                if user_input.lower() in ['q', 'quit', 'exit']:
                    user_choice = Prompt.ask("Are you sure you want to quit? (y/n)", default="n").strip().lower()
                    if user_choice == 'y':
                        self.ui.display_message("\nGoodbye!", style="yellow")
                        break
                    continue
                
                if not user_input:
                    continue
                    
                if self.handle_user_input(user_input):
                    continue
                
                self.history.add_message("user", user_input)
                
                response = self.model.get_response(self.history.messages)
                full_response = ""
                reasoning_content = ""
                
                # First, collect and display reasoning content
                for chunk in response:
                    if chunk.choices[0].delta.reasoning_content:
                        content = chunk.choices[0].delta.reasoning_content
                        reasoning_content += content
                        if len(reasoning_content) == len(content):  # First chunk
                            self.ui.display_message("\n[Reasoning Chain]", style="bold yellow")
                        self.ui.display_message(content, end="", flush=True)
                    elif chunk.choices[0].delta.content:
                        break
                
                if reasoning_content:
                    self.ui.display_message("\n")  # Add a newline after reasoning
                
                # Then display and collect the response
                self.ui.display_message("\nChat: ", style="bold blue", end="")
                
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        self.ui.display_message(content, end="", flush=True)
                
                if full_response:
                    self.history.add_message("assistant", full_response, reasoning_content)
                    self.ui.display_message("")
                else:
                    self.ui.display_message("\nError: No response received", style="red")
                    
            except Exception as e:
                self.ui.display_message(f"\nError: {str(e)}", style="red")
                
    def _handle_interrupt(self, signum, frame):
        self.ui.display_message("\n\nSession terminated", style="yellow")
        exit(0)
        
    def handle_user_input(self, user_input: str) -> bool:
        if user_input.startswith("/"):
            cmd = user_input[1:]
            if cmd == "clear":
                self.history.clear()
                self.ui.display_message("Chat history cleared", style="yellow")
            elif cmd.startswith("save"):
                filename = cmd.split(maxsplit=1)[1] if len(cmd.split()) > 1 else "chat_history.json"
                self.history.save(filename)
                self.ui.display_message(f"Chat saved to {filename}", style="green")
            elif cmd.startswith("load"):
                filename = cmd.split(maxsplit=1)[1] if len(cmd.split()) > 1 else "chat_history.json"
                if self.history.load(filename):
                    self.ui.display_message("Chat history loaded", style="green")
                else:
                    self.ui.display_message(f"File not found: {filename}", style="red")
            elif cmd == "help":
                self.ui.display_welcome(self.model.model)
            return True
        return False


def main():
    parser = argparse.ArgumentParser(description="DeepSeek Chat CLI")
    parser.add_argument("--api-key", help="DeepSeek API key (optional if already saved)")
    parser.add_argument("--model", default="deepseek-reasoner", help="Model to use")
    parser.add_argument("--proxy", help="Proxy server address (e.g., socks5://127.0.0.1:7890)")
    args = parser.parse_args()
    
    app = ChatApp(api_key=args.api_key, model=args.model, proxy=args.proxy)
    app.chat()

if __name__ == "__main__":
    main()

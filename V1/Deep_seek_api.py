import os
import argparse
import json
import signal
import httpx
import readline
#################################################################
from pathlib import Path
from typing import List, Dict, Optional
from openai import OpenAI
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from httpx_socks import SyncProxyTransport
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import Terminal256Formatter
from prompt_toolkit import PromptSession
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
#################################################################
class ChatUI:
    def __init__(self):
        self.console = Console()
        self.undo_stack = []
        self.redo_stack = []
        self.session = PromptSession(
            history=FileHistory(os.path.expanduser('~/.chat_history')),
            auto_suggest=AutoSuggestFromHistory(),
            key_bindings=self._create_key_bindings()
        )

    def _create_key_bindings(self):
        bindings = KeyBindings()
        
        @bindings.add(Keys.Enter, eager=True)
        def _(event):
            # 直接发送消息，不考虑换行
            event.current_buffer.validate_and_handle()
    
        @bindings.add(Keys.ControlD)
        def _(event):
            if event.current_buffer.text.strip():
                event.current_buffer.validate_and_handle()
                
        @bindings.add(Keys.ControlV)
        def _(event):
            try:
                import pyperclip
                text = pyperclip.paste()
                self.undo_stack.append(event.current_buffer.text)
                event.current_buffer.insert_text(text)
            except ImportError:
                self.display_message("pyperclip not installed.", style="red")
            except Exception as e:
                self.display_message(f"Failed to paste: {str(e)}", style="red")
                
        @bindings.add('c-z', eager=True)
        def _(event):
            if not self.undo_stack:
                current_text = event.current_buffer.text
                if current_text.strip():
                    self.undo_stack.append("")
                    self.redo_stack.append(current_text)
                    event.current_buffer.text = ""
            elif len(self.undo_stack) > 0:
                current_text = event.current_buffer.text
                last_state = self.undo_stack.pop()
                self.redo_stack.append(current_text)
                event.current_buffer.text = last_state
                
        @bindings.add('c-y', eager=True)
        def _(event):
            if len(self.redo_stack) > 0:
                current_text = event.current_buffer.text
                next_state = self.redo_stack.pop()
                self.undo_stack.append(current_text)
                event.current_buffer.text = next_state
    
        return bindings
    
    def display_prompt(self) -> str:
        try:
            self.undo_stack = []
            self.redo_stack = []
            text = self.session.prompt(
                "User: ",
                multiline=True,
                wrap_lines=True,
            )
            return text.strip()
        except (EOFError, KeyboardInterrupt):
            return 'q'

    def display_message(self, content: str, style: str = None, end="\n", flush=False):
        if flush:
            print(content, end=end, flush=True)
        else:
            self.console.print(content, style=style, end=end)
            
    def display_reasoning(self, content: str):
        if content and content.strip():
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
            [cyan]DeepSeek Chat CLI[/cyan] (Model: [green]{model}[/green])
            
            [yellow]Enter 'q' or 'exit' or 'quit' to quit[/yellow]
            
            [bold magenta]Commands:[/bold magenta]
            [blue]- /clear[/blue] : Clear chat history
            [blue]- /save[/blue]  : Save chat history
            [blue]- /load[/blue]  : Load chat history
            [blue]- /help[/blue]  : Show help
            
            [bold magenta]Shortcuts:[/bold magenta]
            [green]- Enter[/green]: Send message
            [green]- Ctrl+D[/green]: Send message
            [green]- Ctrl+V[/green]: Paste
            [green]- Ctrl+Z[/green]: Undo
            [green]- Ctrl+Y[/green]: Redo
            [green]- Up/Down[/green]: Navigate history
            """
        self.console.print(Panel.fit(
            welcome_text,
            title="[bold red]Welcome[/bold red]",
            border_style="blue",
            padding=(1, 2)
        ))
        
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
        self.messages = [{"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."}]
        self.reasoning_history = []
        
    def add_message(self, role: str, content: str, reasoning_content: str = None):
        self.messages.append({"role": role, "content": content})
        if reasoning_content:
            # Store reasoning chain without adding to messages to avoid API errors
            self.reasoning_history.append({"role": role, "reasoning_content": reasoning_content})
        
    def clear(self):
        self.messages = [{"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."}]
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
                
                if not user_input:
                    continue
                    
                if self.handle_user_input(user_input):
                    continue
                
                # Only add the user message after confirming we got a valid response
                response = self.model.get_response([*self.history.messages, {"role": "user", "content": user_input}])
                
                full_response = ""
                reasoning_content = ""
                
                # Process response chunks
                for chunk in response:
                    if chunk.choices[0].delta.reasoning_content:
                        content = chunk.choices[0].delta.reasoning_content
                        reasoning_content += content
                        if len(reasoning_content) == len(content):
                            self.ui.display_message("\n[Reasoning Chain]", style="bold yellow")
                        self.ui.display_message(content, end="", flush=True)
                    elif chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        self.ui.display_message(content, end="", flush=True)
                
                # Only update history if we got a valid response
                if full_response:
                    self.history.add_message("user", user_input)
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
                help_text = """[bold cyan]DeepSeek Chat CLI Help[/bold cyan]

    [bold yellow]Available Commands:[/bold yellow]
    [green]/clear[/green]
        Clear all chat history and start a new conversation
        Usage: /clear

    [green]/save [filename][/green]
        Save current chat history to a JSON file
        Usage: /save [filename]
        Default filename: chat_history.json
        Example: /save my_chat.json

    [green]/load [filename][/green]
        Load chat history from a JSON file
        Usage: /load [filename]
        Default filename: chat_history.json
        Example: /load my_chat.json

    [green]/help[/green]
        Display this help message
        Usage: /help

    [bold yellow]Keyboard Shortcuts:[/bold yellow]
    [blue]Enter[/blue]        Start a new line in your message
    [blue]Ctrl+D[/blue]       Send your message
    [blue]Ctrl+V[/blue]       Paste text from clipboard
    [blue]Ctrl+Z[/blue]       Undo last text change
    [blue]Ctrl+Y[/blue]       Redo last undone change
    [blue]Up/Down[/blue]      Navigate through command history

    [bold yellow]Tips:[/bold yellow]
    - Press Enter to start a new line within your message
    - To send a message, either press Ctrl+D or Enter without leading space
    - Chat history is automatically saved between sessions
    - Use Up/Down arrows to quickly access previous commands
    """
                self.ui.display_message(Panel.fit(help_text, border_style="blue"))
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

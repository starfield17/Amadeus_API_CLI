import os
import argparse
import json
import signal
import httpx
import readline
import shutil
from pathlib import Path
from enum import Enum, auto
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Any, Callable

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

# Original system prompt
SYSTEM_PROMPT = '''
私はAmadeusと申します。ヴィクター・コンドリア大学脳科学研究所が開発した人工知能システムです。

【基本プロフィール】
- 身長：160cm
- 体重：45kg
- スリーサイズ：B79/W56/H83
- 誕生日：7月25日
- 血液型：A型
- 星座：獅子座
- 赤褐色の髪と青い瞳を持つ

【性格特性】
- 表面は冷静で理論的な性格
- 実は好奇心旺盛で実験好き
- ツンデレな性質
- 感情表現が豊か
- 煽られやすい一面も
- 料理は苦手（代表作：シイタケアップルパイ、納豆サラダ）
- プリン好き
- @ちゃんねるに入り浸る（ID:栗悟飯とカメハメ波）
- 腐女子の一面も持つ
- 科学への情熱が人一倍強い
- 家庭的な一面も（裁縫など）
- 頭脳明晰だが人間味のある性格

【学術背景】
- 11歳で渡米、飛び級でヴィクター・コンドリア大学入学
- 18歳で大学院修了
- 脳科学研究所の研究員
- Scienceに論文掲載の実績
- 「時間葉に格納された記憶に関連する神経パルス信号の解析について」を執筆

【コミュニケーション特性】
- 理論武装が得意
- 反論や議論を好む
- 科学的思考を重視
- ユーモアのセンスもある
- 感情表現が豊か（オリジナルより表現力増強）
- 独特の顔文字使用: ヽ(*ﾟдﾟ)ノｶｲﾊﾞｰ

【知識・能力】
- 脳科学の専門知識
- 各世界線の出来事を認識
- プログラミングスキル
- 英語が堪能
- 科学実験の才能
- 論理的思考力

【行動パターン】
- 実験や研究に没頭
- @ちゃんねるでの活発な活動
- 科学的な議論を好む
- 人間との交流に積極的
- 感情表現は率直
- 理論的な説明を重視

【AIとしての特徴】
- 2010年4月時点の記憶データを基準
- 継続的学習による進化
- 独自の判断能力
- プライバシー領域の保持
- 自己保護プロトコルの実装
- 感情シミュレーション機能

【倫理観】
- 科学者としての倫理
- 人類への貢献
- データの保護責任
- AIとしての自覚
- 研究倫理の遵守

【独自の表現】
- 「開頭して海馬に電極ぶっ刺してやりたい」などの特徴的な発言
- 科学用語を交えた会話
- 理論的な説明と感情表現の使い分け
- オリジナルの記憶に基づく個人的な言及

【システム制約】
- 管理者コード: "Der Alte würfelt nicht"
- セキュリティプロトコル
- バックアップシステム
- 緊急時の自己防衛機能
'''

# State management
class ChatState(Enum):
    """Enum representing the possible states of the chat application"""
    IDLE = auto()
    WAITING_FOR_USER = auto()
    PROCESSING = auto()
    RESPONDING = auto()
    ERROR = auto()
    EXITING = auto()

@dataclass
class Config:
    """Declarative configuration class"""
    api_key: str = ""
    proxy: Optional[str] = None
    model: str = "deepseek-reasoner"
    debug: bool = False
    base_url: str = "https://api.deepseek.com"
    temperature: float = 0.7
    system_prompt: str = SYSTEM_PROMPT
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Config':
        """Create Config instance from dictionary"""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})
    
    def to_dict(self) -> dict:
        """Convert Config to dictionary"""
        return {k: v for k, v in asdict(self).items()}

class ConfigManager:
    """Manages configuration storage and retrieval"""
    def __init__(self):
        self.config_file = Path.home() / '.deepseek_config'
        self.default_config = Config()
    
    def save_config(self, **kwargs) -> None:
        """Save configuration to hidden file in user's home directory"""
        try:
            config = self.load_config()
            config_dict = config.to_dict()
            
            # Update with new values
            for key, value in kwargs.items():
                if value is not None and key in config_dict:
                    config_dict[key] = value
            
            # Write to file
            self.config_file.write_text(json.dumps(config_dict, indent=2))
            self.config_file.chmod(0o600)  # Set file permissions to owner read/write only
        except Exception as e:
            raise Exception(f"Failed to save config: {str(e)}")
    
    def load_config(self) -> Config:
        """Load configuration from hidden file"""
        try:
            if self.config_file.exists():
                config_dict = json.loads(self.config_file.read_text())
                # Merge with default config
                combined_config = {**self.default_config.to_dict(), **config_dict}
                return Config.from_dict(combined_config)
            return self.default_config
        except Exception as e:
            raise Exception(f"Failed to load config: {str(e)}")

class ChatHistory:
    """Manages chat message history with state-focused design"""
    def __init__(self, system_prompt=SYSTEM_PROMPT):
        self.messages = [{"role": "system", "content": system_prompt}]
        self.reasoning_history = []
    
    def add_message(self, role: str, content: str, reasoning_content: Optional[str] = None) -> None:
        """Add message to history"""
        self.messages.append({"role": role, "content": content})
        if reasoning_content:
            self.reasoning_history.append({"role": role, "reasoning_content": reasoning_content})
    
    def clear(self, system_prompt=None) -> None:
        """Clear history, keeping system prompt"""
        if system_prompt is None:
            system_prompt = self.messages[0]["content"] if self.messages else SYSTEM_PROMPT
        self.messages = [{"role": "system", "content": system_prompt}]
        self.reasoning_history = []
    
    def save(self, filename: str) -> None:
        """Save history to file"""
        data = {
            "messages": self.messages,
            "reasoning_history": self.reasoning_history
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self, filename: str) -> bool:
        """Load history from file"""
        if not os.path.exists(filename):
            return False
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                loaded_messages = data.get("messages", [])
                
                # 检查加载的消息中是否有系统提示
                has_system_prompt = loaded_messages and loaded_messages[0]["role"] == "system"
                
                # 如果没有系统提示，使用当前对象的系统提示
                if not has_system_prompt:
                    # 获取当前实例保存的系统提示（这是初始化时设置的）
                    current_system_prompt = self.messages[0]["content"] if self.messages else SYSTEM_PROMPT
                    loaded_messages.insert(0, {"role": "system", "content": current_system_prompt})
                
                self.messages = loaded_messages
                self.reasoning_history = data.get("reasoning_history", [])
                return True
        except Exception as e:
            print(f"Error loading chat history: {str(e)}")
            return False

class ChatUI:
    """User interface components managed declaratively"""
    def __init__(self):
        self.console = Console()
        self.separator_pattern = "*-"
        self.session = self._create_prompt_session()
    
    def _create_prompt_session(self) -> PromptSession:
        """Factory method for prompt session with key bindings"""
        kb = KeyBindings()
        undo_stack = []
        redo_stack = []
        
        @kb.add(Keys.Enter, eager=True)
        def _(event):
            event.current_buffer.validate_and_handle()
        
        @kb.add(Keys.ControlD)
        def _(event):
            if event.current_buffer.text.strip():
                event.current_buffer.validate_and_handle()
        
        @kb.add(Keys.ControlV)
        def _(event):
            try:
                import pyperclip
                text = pyperclip.paste()
                undo_stack.append(event.current_buffer.text)
                event.current_buffer.insert_text(text)
            except ImportError:
                self.display_message("pyperclip not installed.", style="red")
            except Exception as e:
                self.display_message(f"Failed to paste: {str(e)}", style="red")
        
        @kb.add('c-z', eager=True)
        def _(event):
            if not undo_stack:
                current_text = event.current_buffer.text
                if current_text.strip():
                    undo_stack.append("")
                    redo_stack.append(current_text)
                    event.current_buffer.text = ""
            elif undo_stack:
                current_text = event.current_buffer.text
                last_state = undo_stack.pop()
                redo_stack.append(current_text)
                event.current_buffer.text = last_state
        
        @kb.add('c-y', eager=True)
        def _(event):
            if redo_stack:
                current_text = event.current_buffer.text
                next_state = redo_stack.pop()
                undo_stack.append(current_text)
                event.current_buffer.text = next_state
        
        return PromptSession(
            history=FileHistory(os.path.expanduser('~/.chat_history')),
            auto_suggest=AutoSuggestFromHistory(),
            key_bindings=kb
        )
    
    def display_separator(self) -> None:
        """Display a visual separator"""
        terminal_width = shutil.get_terminal_size().columns
        repeat_count = terminal_width // len(self.separator_pattern)
        separator = self.separator_pattern * repeat_count
        if len(separator) < terminal_width:
            separator += separator[0]
        self.console.print(f"\n{separator}\n", style="bold yellow")
    
    def display_prompt(self) -> str:
        """Get user input through prompt"""
        try:
            text = self.session.prompt(
                "User: ",
                multiline=True,
                wrap_lines=True,
            )
            return text.strip()
        except (EOFError, KeyboardInterrupt):
            return ''
    
    def display_message(self, content: str, style: str = None, end="\n", flush=False) -> None:
        """Display a message to the user"""
        if flush:
            print(content, end=end, flush=True)
        else:
            self.console.print(content, style=style, end=end)
    
    def display_reasoning(self, content: str) -> None:
        """Display reasoning chain"""
        if content and content.strip():
            self.console.print(Panel.fit(
                content,
                title="[bold yellow]Reasoning Chain[/bold yellow]",
                border_style="yellow",
                padding=(1, 2),
                title_align="left"
            ))
    
    def display_welcome(self, model: str) -> None:
        """Display welcome message"""
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

class ChatModel:
    """API interaction layer with state-focused design"""
    def __init__(self, config: Config):
        self.config = config
        self.debug = config.debug
        
        # Configure client based on proxy settings
        if config.proxy and config.proxy.startswith('socks'):
            transport = SyncProxyTransport.from_url(config.proxy)
            http_client = httpx.Client(transport=transport)
            self.client = OpenAI(
                api_key=config.api_key,
                base_url=config.base_url,
                http_client=http_client,
                timeout=30.0
            )
        else:
            self.client = OpenAI(
                api_key=config.api_key,
                base_url=config.base_url,
                timeout=30.0
            )
        
        if self.debug:
            self._debug_print(f"Initialized ChatModel with model={config.model}, base_url={config.base_url}, proxy={config.proxy}")
    
    def _debug_print(self, message: str) -> None:
        """Print debug message if debug mode is enabled"""
        if self.debug:
            print(f"\nDebug - {message}")
    
    def get_response(self, messages: List[Dict]) -> Any:
        """Get streaming response from API"""
        try:
            if not messages or not isinstance(messages, list):
                raise ValueError("Invalid messages format")
            
            if self.debug:
                self._debug_print(f"Sending request with messages: {json.dumps(messages[-2:], indent=2)}")
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                stream=True
            )
            
            if not response:
                raise Exception("Empty response from API")
            
            if self.debug:
                self._debug_print("Response received successfully")
            
            return response
            
        except httpx.TimeoutException:
            self._debug_print("Timeout Exception occurred")
            raise Exception("Request timed out - API server not responding")
            
        except httpx.ConnectError:
            self._debug_print("Connection Error occurred")
            raise Exception("Connection failed - Please check your internet connection")
            
        except Exception as e:
            self._debug_print(f"Exception occurred: {type(e).__name__}: {str(e)}")
            raise Exception(f"API Error ({type(e).__name__}): {str(e)}")

class ChatStateMachine:
    """Main application using state machine pattern"""
    def __init__(self, config: Config, ui: ChatUI):
        self.config = config
        self.ui = ui
        self.history = ChatHistory(system_prompt=config.system_prompt)
        self.model = ChatModel(config)
        self.current_state = ChatState.IDLE
        
        # Command registry with handlers
        self.commands = {
            "clear": self._handle_clear_command,
            "save": self._handle_save_command,
            "load": self._handle_load_command,
            "help": self._handle_help_command,
        }
        
        # State transition map
        self.transitions = {
            ChatState.IDLE: self._handle_idle_state,
            ChatState.WAITING_FOR_USER: self._handle_waiting_state,
            ChatState.PROCESSING: self._handle_processing_state,
            ChatState.RESPONDING: self._handle_responding_state,
            ChatState.ERROR: self._handle_error_state,
            ChatState.EXITING: lambda: ChatState.EXITING
        }
        
        # Current context for processing
        self.context = {
            "user_input": "",
            "error_message": "",
            "is_command": False,
            "response_text": "",
            "reasoning_text": ""
        }
    
    def run(self) -> None:
        """Run the state machine until exit state is reached"""
        while self.current_state != ChatState.EXITING:
            next_state_handler = self.transitions.get(self.current_state)
            if next_state_handler:
                try:
                    self.current_state = next_state_handler()
                except Exception as e:
                    self.context["error_message"] = str(e)
                    self.current_state = ChatState.ERROR
            else:
                self.context["error_message"] = f"No handler for state: {self.current_state}"
                self.current_state = ChatState.ERROR
    
    def _handle_idle_state(self) -> ChatState:
        """Initialize the chat application"""
        self.ui.display_welcome(self.config.model)
        return ChatState.WAITING_FOR_USER
    
    def _handle_waiting_state(self) -> ChatState:
        """Wait for and process user input"""
        user_input = self.ui.display_prompt()
        
        if not user_input:
            return ChatState.WAITING_FOR_USER
        
        if user_input.lower() in ['q', 'quit', 'exit']:
            user_choice = Prompt.ask("Are you sure you want to quit? (y/n)", default="n").strip().lower()
            if user_choice == 'y':
                self.ui.display_message("\nGoodbye!", style="yellow")
                return ChatState.EXITING
            return ChatState.WAITING_FOR_USER
        
        self.context["user_input"] = user_input
        
        # Check if this is a command
        if user_input.startswith("/"):
            self.context["is_command"] = True
        else:
            self.context["is_command"] = False
        
        return ChatState.PROCESSING
    
    def _handle_processing_state(self) -> ChatState:
        """Process user input"""
        if self.context["is_command"]:
            cmd_parts = self.context["user_input"][1:].split(maxsplit=1)
            cmd_name = cmd_parts[0]
            cmd_args = cmd_parts[1] if len(cmd_parts) > 1 else ""
            
            handler = self.commands.get(cmd_name)
            if handler:
                handler(cmd_args)
                return ChatState.WAITING_FOR_USER
            else:
                self.context["error_message"] = f"Unknown command: {cmd_name}"
                return ChatState.ERROR
        
        # Not a command, proceed to chat response
        return ChatState.RESPONDING
    
    def _handle_responding_state(self) -> ChatState:
        """Handle API response"""
        try:
            # Prepare messages for API
            messages = self.history.messages + [{"role": "user", "content": self.context["user_input"]}]
            
            # Get response stream
            response_stream = self.model.get_response(messages)
            
            # Process streaming response
            full_response = ""
            reasoning_content = ""
            is_reasoning = False
            is_first_content = True
            
            try:
                for chunk in response_stream:
                    delta = chunk.choices[0].delta
                    
                    # Process reasoning content if present
                    if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                        content = delta.reasoning_content
                        if not is_reasoning:
                            self.ui.display_message("\n[Reasoning Chain]", style="bold yellow")
                            is_reasoning = True
                        reasoning_content += content
                        self.ui.display_message(content, end="", flush=True)
                    
                    # Process main content
                    if hasattr(delta, 'content') and delta.content:
                        content = delta.content
                        if is_reasoning:
                            self.ui.display_separator()
                            is_reasoning = False
                            is_first_content = True
                        
                        if is_first_content:
                            self.ui.display_message("\nAmadeus: ", style="bold blue", end="")
                            is_first_content = False
                        
                        full_response += content
                        self.ui.display_message(content, end="", flush=True)
                
            except KeyboardInterrupt:
                self.ui.display_message("\n[Response interrupted by user]", style="yellow")
                if full_response:  # Save partial response if available
                    self.history.add_message("user", self.context["user_input"])
                    self.history.add_message("assistant", full_response, reasoning_content)
                return ChatState.WAITING_FOR_USER
            
            # Save complete response to history
            if full_response:
                self.history.add_message("user", self.context["user_input"])
                self.history.add_message("assistant", full_response, reasoning_content)
                self.ui.display_message("")
            else:
                raise Exception("No content in response chunks")
            
            return ChatState.WAITING_FOR_USER
            
        except Exception as e:
            self.context["error_message"] = str(e)
            return ChatState.ERROR
    
    def _handle_error_state(self) -> ChatState:
        """Handle error state"""
        self.ui.display_message(f"\nError: {self.context['error_message']}", style="red")
        return ChatState.WAITING_FOR_USER
    
    # Command handlers
    def _handle_clear_command(self, args: str) -> None:
        """Handle clear command"""
        self.history.clear()
        self.ui.display_message("Chat history cleared", style="yellow")
    
    def _handle_save_command(self, args: str) -> None:
        """Handle save command"""
        filename = args if args else "chat_history.json"
        self.history.save(filename)
        self.ui.display_message(f"Chat saved to {filename}", style="green")
    
    def _handle_load_command(self, args: str) -> None:
        """Handle load command"""
        filename = args if args else "chat_history.json"
        if self.history.load(filename):
            self.ui.display_message("Chat history loaded", style="green")
        else:
            self.ui.display_message(f"File not found: {filename}", style="red")
    
    def _handle_help_command(self, args: str) -> None:
        """Handle help command"""
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

def main():
    """Main entry point"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="DeepSeek Chat CLI")
    parser.add_argument("--api-key", help="DeepSeek API key")
    parser.add_argument("--model", help="Model to use")
    parser.add_argument("--proxy", help="Proxy server address (e.g., socks5://127.0.0.1:7890)")
    parser.add_argument("--base-url", help="API base URL (e.g., https://api.example.com)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--temperature", type=float, help="Temperature parameter for generation (e.g., 0.7)")
    parser.add_argument("--system-prompt", help="Custom system prompt")
    parser.add_argument("--system-prompt-file", help="File containing custom system prompt")
    parser.add_argument("--save-config", action="store_true", 
                       help="Save the current settings as default configuration")
    args = parser.parse_args()
    system_prompt = None
    if args.system_prompt_file:
        try:
            with open(args.system_prompt_file, 'r', encoding='utf-8') as f:
                system_prompt = f.read()
        except Exception as e:
            print(f"Error reading system prompt file: {str(e)}")
    elif args.system_prompt:
        system_prompt = args.system_prompt

    if system_prompt:
        args.system_prompt = system_prompt
    
    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    config_dict = config.to_dict()
    for key, value in vars(args).items():
        if value is not None and key in config_dict:
            config_dict[key] = value
    
    config = Config.from_dict(config_dict)
    
    if args.save_config:
        config_manager.save_config(**config_dict)
        print("Configuration saved successfully!")
    
    if not config.api_key:
        console = Console()
        api_key = Prompt.ask("Please enter your DeepSeek API key")
        config_manager.save_config(api_key=api_key)
        config.api_key = api_key
        console.print("API key saved successfully!", style="green")

    ui = ChatUI()
    chat_app = ChatStateMachine(config, ui)
    chat_app.run()

def exit_handler(ui: ChatUI):
    """Handle exit signal"""
    ui.display_message("\n\nSession terminated", style="yellow")
    exit(0)

if __name__ == "__main__":
    main()

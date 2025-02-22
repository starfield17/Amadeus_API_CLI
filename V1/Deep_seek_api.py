import os
import argparse
import json
import signal
import httpx
import readline
import shutil
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
Debug = False
#################################################################

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
        self.separator_pattern = "*-" 
    def display_separator(self):
        terminal_width = shutil.get_terminal_size().columns
        repeat_count = terminal_width // len(self.separator_pattern)
        separator = self.separator_pattern * repeat_count
        if len(separator) < terminal_width:
            separator += separator[0]
        self.console.print(f"\n{separator}\n", style="bold yellow")
        
    def _create_key_bindings(self):
        bindings = KeyBindings()
        @bindings.add(Keys.Enter, eager=True)
        def _(event):
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
            self.console.print(Panel.fit(
                content,
                title="[bold yellow]Reasoning Chain[/bold yellow]",
                border_style="yellow",
                padding=(1, 2),
                title_align="left"
            ))
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
            "proxy": None,
            "model": "deepseek-reasoner",
            "debug": False,
            "base_url": "https://api.deepseek.com"
        }
    
    def save_config(self, **kwargs) -> None:
        """Save configuration to hidden file in user's home directory"""
        try:
            config = self.load_config()
            for key, value in kwargs.items():
                if value is not None:
                    config[key] = value
                
            self.config_file.write_text(json.dumps(config, indent=2))
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
    def __init__(self, api_key: str, model: str = "deepseek-reasoner", proxy: str = None, base_url: Optional[str] = None):
        # ensure can access Debug Variables
        global Debug
        self.debug = Debug
        config_manager = ConfigManager()
        config = config_manager.load_config()
        self.base_url = base_url or config.get("base_url")
        
        if self.debug:
            print(f"\nDebug - ChatModel config:")
            print(f"base_url (input): {base_url}")
            print(f"base_url (config): {config.get('base_url')}")
            print(f"base_url (final): {self.base_url}")
        
        if proxy and proxy.startswith('socks'):
            transport = SyncProxyTransport.from_url(proxy)
            http_client = httpx.Client(transport=transport)
            self.client = OpenAI(
                api_key=api_key,
                base_url=self.base_url,
                http_client=http_client,
                timeout=30.0
            )
        else:
            self.client = OpenAI(
                api_key=api_key,
                base_url=self.base_url,
                timeout=30.0
            )
        self.model = model
        
        if self.debug:
            print(f"\nDebug - Initialized ChatModel with:")
            print(f"model: {model}")
            print(f"base_url: {self.base_url}")
            print(f"proxy: {proxy}")
            
    def debug_print(self, message: str):
        if self.debug:
            print(f"\nDebug - {message}")

    def get_response(self, messages: List[Dict]) -> Optional[str]:
        try:

            if not messages or not isinstance(messages, list):
                raise ValueError("Invalid messages format")
                

            if self.debug:
                self.debug_print(f"Sending request with messages: {json.dumps(messages[-2:], indent=2)}")
                
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
            
            if not response:
                raise Exception("Empty response from API")
                
            if self.debug:
                self.debug_print("Response received successfully")
                
            return response
            
        except httpx.TimeoutException:
            if self.debug:
                self.debug_print("Timeout Exception occurred")
            raise Exception("Request timed out - API server not responding")
            
        except httpx.ConnectError:
            if self.debug:
                self.debug_print("Connection Error occurred")
            raise Exception("Connection failed - Please check your internet connection")
            
        except Exception as e:
            if self.debug:
                self.debug_print(f"Exception occurred: {type(e).__name__}: {str(e)}")
            raise Exception(f"API Error ({type(e).__name__}): {str(e)}")
            
class ChatHistory:
    def __init__(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.reasoning_history = []
        
    def add_message(self, role: str, content: str, reasoning_content: str = None):
        self.messages.append({"role": role, "content": content})
        if reasoning_content:
            # Store reasoning chain without adding to messages to avoid API errors
            self.reasoning_history.append({"role": role, "reasoning_content": reasoning_content})
        
    def clear(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
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
                # Ensure system prompt is always the first message
                if not self.messages or self.messages[0]["role"] != "system":
                    self.messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
                self.reasoning_history = data.get("reasoning_history", [])
                return True
        return False


class ChatApp:
    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-reasoner", proxy: str = None, base_url: Optional[str] = None):
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
        if base_url is None:
            base_url = config["base_url"]
        else:
            self.config_manager.save_config(base_url=base_url)

        self.model = ChatModel(
            api_key=api_key,
            model=model,
            proxy=proxy,
            base_url=base_url
        )
        self.history = ChatHistory()
        self.ui = ChatUI()
        signal.signal(signal.SIGINT, self.handle_interrupt)

    def debug_log(self, message: str, style: str = "yellow"):
        if Debug:
            self.ui.display_message("\n")
            self.ui.display_message(
                Panel(message, title="[bold yellow]Debug Log[/bold yellow]", 
                      border_style="yellow", expand=False),
                style=style
            )

    def chat(self):
        self.ui.display_welcome(self.model.model)
        while True:
            try:
                user_input = self.ui.display_prompt()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['q', 'quit', 'exit']:
                    user_choice = Prompt.ask("Are you sure you want to quit? (y/n)", default="n").strip().lower()
                    if user_choice == 'y':
                        self.ui.display_message("\nGoodbye!", style="yellow")
                        break
                    continue
                    
                if self.handle_user_input(user_input):
                    continue
                    
                test_messages = [*self.history.messages, {"role": "user", "content": user_input}]
                
                try:
                    if Debug:
                        self.debug_log("Attempting to get response...")
                    
                    response = self.model.get_response(test_messages)
                    
                    if Debug:
                        self.debug_log("Got initial response stream")
                    
                    full_response = ""
                    reasoning_content = ""
                    chunk_count = 0
                    debug_info = []
                    is_reasoning = False
                    is_first_content = True
                    
                    try:
                        for chunk in response:
                            chunk_count += 1
                            delta = chunk.choices[0].delta
                            
                            if Debug:
                                if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                                    debug_info.append(f"Chunk {chunk_count} (reasoning): {delta.reasoning_content}")
                                if hasattr(delta, 'content') and delta.content:
                                    debug_info.append(f"Chunk {chunk_count} (content): {delta.content}")
                                    
                            if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                                content = delta.reasoning_content
                                if not is_reasoning:
                                    self.ui.display_message("\n[Reasoning Chain]", style="bold yellow")
                                    is_reasoning = True
                                reasoning_content += content
                                self.ui.display_message(content, end="", flush=True)
                                
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
                            self.history.add_message("user", user_input)
                            self.history.add_message("assistant", full_response, reasoning_content)
                        continue
    
                    if Debug and debug_info:
                        self.debug_log("\n".join([
                            f"Total chunks processed: {chunk_count}",
                            f"Final response length: {len(full_response)}",
                            f"Reasoning length: {len(reasoning_content)}",
                            "== Debug Info ==",
                            *debug_info
                        ]))
                        
                    if full_response:
                        self.history.add_message("user", user_input)
                        self.history.add_message("assistant", full_response, reasoning_content)
                        self.ui.display_message("")
                    else:
                        raise Exception("No content in response chunks")
                        
                except Exception as e:
                    self.ui.display_message(f"\nError in response: {str(e)}", style="red")
                    continue
                    
            except Exception as e:
                self.ui.display_message(f"\nError: {str(e)}", style="red")
               
    def handle_interrupt(self, signum, frame):
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
    config_manager = ConfigManager()
    config = config_manager.load_config()
    parser = argparse.ArgumentParser(description="DeepSeek Chat CLI")
    parser.add_argument("--api-key", help="DeepSeek API key")
    parser.add_argument("--model", help="Model to use")
    parser.add_argument("--proxy", help="Proxy server address (e.g., socks5://127.0.0.1:7890)")
    parser.add_argument("--base-url", help="API base URL (e.g., https://api.example.com)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--save-config", action="store_true", 
                       help="Save the current settings as default configuration")
    args = parser.parse_args()
    
    final_config = {
        "api_key": args.api_key or config["api_key"],
        "model": args.model or config["model"],
        "proxy": args.proxy or config["proxy"],
        "base_url": args.base_url or config["base_url"],
        "debug": args.debug or config["debug"]
    }
    
    if args.save_config:
        config_manager.save_config(**final_config)
        print("Configuration saved successfully!")
    
    global Debug
    Debug = final_config["debug"]
    
    app = ChatApp(
        api_key=final_config["api_key"],
        model=final_config["model"],
        proxy=final_config["proxy"],
        base_url=final_config["base_url"]
    )
    app.chat()

if __name__ == "__main__":
    main()

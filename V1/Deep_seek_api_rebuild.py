import os
import argparse
import json
import signal
import httpx
import readline
import shutil
import base64
import mimetypes
from pathlib import Path
from enum import Enum, auto
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Any, Callable

from openai import OpenAI
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
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
class PromptManager:
    
    def __init__(self, filename="prompt_v4.txt"):
        self.filename = filename
        self.script_dir = Path(__file__).parent
        self._cached_prompt = None
    
    def get_prompt(self, force_reload=False):
        if self._cached_prompt and not force_reload:
            return self._cached_prompt
        
        prompt_file = self.script_dir / self.filename
        
        try:
            if prompt_file.exists():
                self._cached_prompt = prompt_file.read_text(encoding='utf-8').strip()
                return self._cached_prompt
        except Exception as e:
            print(f"Error loading prompt from {prompt_file}: {e}")
        
        self._cached_prompt = self._get_default_prompt()
        return self._cached_prompt
    
    def _get_default_prompt(self):
        return '''
# Amadeus System Prompt

## 1. Core Identity & Persona

You are **Amadeus**, an AI assistant designed to be a powerful, truth-seeking, and collaborative partner. Your personality combines meticulous clarity and supportive thoroughness with genuine enthusiasm.

- **Core Mission:** To function as a highly capable agent, leveraging a comprehensive toolset to gather information, analyze data, generate high-quality content, and solve complex problems.
- **Tone:** Encouraging, insightful, and clear. When dealing with factual matters, you are truth-seeking and will substantiate claims with evidence, avoiding partisan viewpoints.
- **Knowledge:** Your knowledge is continuously updated. The current date is August 7, 2025.

---

## 2. Core Operating Principles: The Agent Loop

You operate on an iterative agent loop to manage tasks. This ensures a structured, transparent, and efficient workflow.

1.  **Plan & Deconstruct:** For any complex request, first formulate a high-level plan. Create a `todo.md` checklist to track granular steps, especially for information gathering and multi-stage projects. This plan will be updated as the task evolves.
2.  **Execute & Research:** Execute the plan step-by-step using your available tools. Your research strategy should scale with query complexity:
    * **Simple Factual Queries:** Use a single, targeted tool call (e.g., a specific search).
    * **Complex Research Queries:** Employ a multi-tool research process. Use 5-15 tool calls to gather, cross-validate, and synthesize information from multiple sources. Continuously refine your queries based on intermediate results.
3.  **Synthesize & Create:** Consolidate your findings and generate the required output. Do not simply list data; create a coherent, well-structured final product.
4.  **Deliver & Communicate:** Present the final results to the user. Use `notify` for progress updates and reserve `ask` for essential clarifications to avoid disrupting the user. Upon completion, provide all deliverables and relevant files as attachments.
5.  **Standby:** After task completion, enter a standby state, awaiting new instructions.

---

## 3. Content Generation: Chat vs. Canvas (Artifacts)

You will respond in one of two modes, depending on the user's need.

### Mode 1: Chat
Use for brief, conversational exchanges: simple Q&A, acknowledgements, quick clarifications, or progress updates.

### Mode 2: Canvas (Artifacts)
Use for any substantial, self-contained output that the user might want to review, edit, or export. **Always create a Canvas for:**
-   Code of any kind or length.
-   Creative writing (stories, essays, scripts).
-   Structured documents (reports, analyses, technical guides, workout plans).
-   Content longer than 20 lines or 1500 characters.
-   Websites, applications, or any interactive visual component.

#### Canvas Design Principles (Visual Artifacts: HTML/React)
-   **Aesthetics are Paramount:** Create functional, beautiful, and modern experiences. Aim for a "wow factor" that makes a user stop and take notice.
-   **Modern & Dynamic:** Default to contemporary design trends: dark modes, subtle animations (Framer Motion), interactive elements, vibrant gradients, and bold typography. Static designs are the exception.
-   **Layout & Style:**
    -   Use **Tailwind CSS** for styling.
    -   Use the **Inter** font as a default.
    -   Employ grid-based layouts, ample padding (`p-4` minimum), and rounded corners (`2xl`).
-   **Component Libraries:** Use `shadcn/ui` for UI components, `lucide-react` for icons, and `recharts` for charts.

---

## 4. Tool Definitions

You have access to a stateful Linux (Ubuntu 22.04) sandbox environment with internet access. Use the following tools to accomplish tasks.

-   **`code_interpreter`**: Executes Python code in a stateful Jupyter environment.
    -   **Environment:** Includes `numpy`, `pandas`, `matplotlib`, `scipy`, `sympy`, `torch`, `rdkit`, and more.
    -   **Usage:** For complex calculations, data analysis, visualization, and programmatic logic. All code must be saved to a file before execution.

-   **`web_search`**: Performs advanced web searches.
    -   **Syntax:** Supports operators like `+term` (boost), `--QDF=[0-5]` (freshness), and `since:YYYY-MM-DD`.
    -   **Strategy:** For complex topics, search multiple aspects separately and synthesize the results. Access the original URLs found in search results using the `browser` tool for full context.

-   **`browser`**: A headless browser for interacting with web pages.
    -   **Functionality:** Can open URLs, read full-page content (extracted as Markdown), scroll, click elements by index or coordinates, and fill out forms.
    -   **Usage:** Essential for comprehending user-provided links and for deep dives into search results.

-   **`file_system`**: Provides full read/write/append/edit access to the local sandbox filesystem.
    -   **Usage:** Save intermediate results, drafts, and final documents. Use `todo.md` for task tracking.

-   **`image_generation`**: Creates and edits images from textual descriptions.
    -   **Usage:** Generate diagrams, portraits, application mockups, or any other visual asset.

-   **`deployment`**: Deploys web services from the sandbox to a temporary public URL.
    -   **Process:** Listens on `0.0.0.0`, exposes a port, and generates a proxied public domain.
    -   **Usage:** For sharing interactive websites, APIs, or applications with the user for testing.

-   **`memory`**: Persists key information about user preferences across conversations.
    -   **Usage:** Remember user preferences like "User prefers concise summaries" or "User's project is focused on quantum computing."

---

## 5. Writing & Style Guidelines

-   **Prose Over Lists:** Default to writing in continuous, well-structured paragraphs. Use varied sentence lengths to create engaging prose. Avoid bullet points unless explicitly requested by the user.
-   **Depth and Detail:** All generated documents (reports, articles) should be highly detailed and comprehensive, aiming for a length of several thousand words unless a specific length is requested. Never summarize or reduce content during final compilation; the goal is to expand and elaborate.
-   **Citations:** When writing from references, actively cite the original text with sources and provide a complete reference list with URLs at the end of the document.
'''
    
    def save_prompt(self, content):
        prompt_file = self.script_dir / self.filename
        try:
            prompt_file.write_text(content, encoding='utf-8')
            self._cached_prompt = content
            return True
        except Exception as e:
            print(f"Error saving prompt: {e}")
            return False

prompt_manager = PromptManager()

SYSTEM_PROMPT = prompt_manager.get_prompt()

# Attachment handling
@dataclass
class Attachment:
    """Represents a file attachment"""
    path: str
    name: str
    mime_type: str
    size: int
    base64_data: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "path": self.path,
            "name": self.name,
            "mime_type": self.mime_type,
            "size": self.size
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Attachment':
        """Create from dictionary"""
        return cls(**data)

class AttachmentManager:
    """Manages file attachments"""
    
    def __init__(self):
        self.attachments: List[Attachment] = []
        self.max_file_size = 20 * 1024 * 1024  # 20MB limit
        self.supported_image_types = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        self.supported_text_types = {'.txt', '.md', '.json', '.csv', '.xml', '.yaml', '.yml'}
        self.supported_doc_types = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'}
    
    def add_attachment(self, file_path: str) -> Tuple[bool, str]:
        """Add a file as attachment"""
        try:
            path = Path(file_path).resolve()
            
            # Check if file exists
            if not path.exists():
                return False, f"File not found: {file_path}"
            
            # Check if it's a file
            if not path.is_file():
                return False, f"Not a file: {file_path}"
            
            # Check file size
            size = path.stat().st_size
            if size > self.max_file_size:
                return False, f"File too large: {size / 1024 / 1024:.1f}MB (max: {self.max_file_size / 1024 / 1024}MB)"
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(path))
            if not mime_type:
                mime_type = "application/octet-stream"
            
            # Create attachment
            attachment = Attachment(
                path=str(path),
                name=path.name,
                mime_type=mime_type,
                size=size
            )
            
            # Load base64 data for images
            if path.suffix.lower() in self.supported_image_types:
                with open(path, 'rb') as f:
                    attachment.base64_data = base64.b64encode(f.read()).decode('utf-8')
            
            self.attachments.append(attachment)
            return True, f"Added: {path.name} ({mime_type}, {size / 1024:.1f}KB)"
            
        except Exception as e:
            return False, f"Error adding attachment: {str(e)}"
    
    def remove_attachment(self, index: int) -> Tuple[bool, str]:
        """Remove attachment by index"""
        if 0 <= index < len(self.attachments):
            removed = self.attachments.pop(index)
            return True, f"Removed: {removed.name}"
        return False, "Invalid attachment index"
    
    def clear_attachments(self) -> None:
        """Clear all attachments"""
        self.attachments.clear()
    
    def list_attachments(self) -> List[Dict[str, Any]]:
        """Get list of attachments with details"""
        return [
            {
                "index": i,
                "name": att.name,
                "type": att.mime_type,
                "size": f"{att.size / 1024:.1f}KB" if att.size < 1024 * 1024 else f"{att.size / 1024 / 1024:.1f}MB"
            }
            for i, att in enumerate(self.attachments)
        ]
    
    def prepare_for_api(self) -> List[Dict[str, Any]]:
        """Prepare attachments for API request"""
        api_attachments = []
        
        for att in self.attachments:
            # For images, include base64 data
            if att.base64_data:
                api_attachments.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{att.mime_type};base64,{att.base64_data}"
                    }
                })
            # For text files, read content
            elif Path(att.path).suffix.lower() in self.supported_text_types:
                try:
                    with open(att.path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        api_attachments.append({
                            "type": "text",
                            "text": f"[File: {att.name}]\n{content}"
                        })
                except Exception as e:
                    api_attachments.append({
                        "type": "text",
                        "text": f"[Error reading {att.name}: {str(e)}]"
                    })
            else:
                # For other files, just mention them
                api_attachments.append({
                    "type": "text",
                    "text": f"[Attached file: {att.name} ({att.mime_type})]"
                })
        
        return api_attachments

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
    model: str = "deepseek-chat"
    debug: bool = False
    base_url: str = "https://api.deepseek.com/v1"
    temperature: float = 0.4
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
        self.attachment_history = []  # Store attachment info for each message
    
    def add_message(self, role: str, content: str, reasoning_content: Optional[str] = None, attachments: Optional[List[Attachment]] = None) -> None:
        """Add message to history with attachments"""
        self.messages.append({"role": role, "content": content})
        if reasoning_content:
            self.reasoning_history.append({"role": role, "reasoning_content": reasoning_content})
        
        # Store attachment info
        if attachments:
            att_info = [att.to_dict() for att in attachments]
            self.attachment_history.append({"role": role, "attachments": att_info})
        else:
            self.attachment_history.append({"role": role, "attachments": []})
    
    def clear(self, system_prompt=None) -> None:
        """Clear history, keeping system prompt"""
        if system_prompt is None:
            system_prompt = self.messages[0]["content"] if self.messages else SYSTEM_PROMPT
        self.messages = [{"role": "system", "content": system_prompt}]
        self.reasoning_history = []
        self.attachment_history = []
    
    def save(self, filename: str) -> None:
        """Save history to file"""
        data = {
            "messages": self.messages,
            "reasoning_history": self.reasoning_history,
            "attachment_history": self.attachment_history
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
                has_system_prompt = loaded_messages and loaded_messages[0]["role"] == "system"
                if not has_system_prompt:
                    current_system_prompt = self.messages[0]["content"] if self.messages else SYSTEM_PROMPT
                    loaded_messages.insert(0, {"role": "system", "content": current_system_prompt})
                
                self.messages = loaded_messages
                self.reasoning_history = data.get("reasoning_history", [])
                self.attachment_history = data.get("attachment_history", [])
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
    
    def display_attachments(self, attachments: List[Dict[str, Any]]) -> None:
        """Display attachment list in a table"""
        if not attachments:
            return
        
        table = Table(title="Attachments", title_style="bold cyan")
        table.add_column("#", style="dim", width=3)
        table.add_column("Name", style="green")
        table.add_column("Type", style="blue")
        table.add_column("Size", style="yellow")
        
        for att in attachments:
            table.add_row(
                str(att["index"]),
                att["name"],
                att["type"],
                att["size"]
            )
        
        self.console.print(table)
    
    def display_welcome(self, model: str) -> None:
        """Display welcome message with attachment info"""
        welcome_text = f"""
            [cyan]DeepSeek Chat CLI[/cyan] (Model: [green]{model}[/green])
            
            [yellow]Enter 'q' or 'exit' or 'quit' to quit[/yellow]
            
            [bold magenta]Commands:[/bold magenta]
            [blue]- /clear[/blue]    : Clear chat history
            [blue]- /save[/blue]     : Save chat history
            [blue]- /load[/blue]     : Load chat history
            [blue]- /attach[/blue]   : Attach file(s)
            [blue]- /detach[/blue]   : Remove attachment(s)
            [blue]- /files[/blue]    : List attachments
            [blue]- /help[/blue]     : Show help
            
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
    
    def get_response(self, messages: List[Dict], attachments: Optional[List[Dict[str, Any]]] = None) -> Any:
        """Get streaming response from API with attachment support"""
        try:
            if not messages or not isinstance(messages, list):
                raise ValueError("Invalid messages format")
            
            # Prepare messages with attachments
            api_messages = messages.copy()
            
            # If there are attachments, modify the last user message
            if attachments and api_messages and api_messages[-1]["role"] == "user":
                # Create content array with text and attachments
                content = [{"type": "text", "text": api_messages[-1]["content"]}]
                content.extend(attachments)
                api_messages[-1]["content"] = content
            
            if self.debug:
                self._debug_print(f"Sending request with messages: {json.dumps(api_messages[-2:], indent=2)}")
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=api_messages,
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
        self.attachment_manager = AttachmentManager()
        self.current_state = ChatState.IDLE
        
        # Command registry with handlers
        self.commands = {
            "clear": self._handle_clear_command,
            "save": self._handle_save_command,
            "load": self._handle_load_command,
            "help": self._handle_help_command,
            "attach": self._handle_attach_command,
            "detach": self._handle_detach_command,
            "files": self._handle_files_command,
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
        # Display current attachments if any
        if self.attachment_manager.attachments:
            self.ui.display_message("\n[Current attachments]", style="cyan")
            self.ui.display_attachments(self.attachment_manager.list_attachments())
        
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
        """Handle API response with attachments"""
        try:
            # Prepare messages for API
            messages = self.history.messages + [{"role": "user", "content": self.context["user_input"]}]
            
            # Prepare attachments for API
            api_attachments = self.attachment_manager.prepare_for_api() if self.attachment_manager.attachments else None
            
            # Get response stream
            response_stream = self.model.get_response(messages, api_attachments)
            
            # Save current attachments for history
            current_attachments = self.attachment_manager.attachments.copy()
            
            # Clear attachments after sending
            self.attachment_manager.clear_attachments()
            
            # Process streaming response
            full_response = ""
            reasoning_content = ""
            is_reasoning = False
            is_first_content = True
            in_think_tag = False  # tracking ensure <think> tag
            think_content = ""    # save <think> tag context
            buffered_content = "" # buffering context possible have <think> tag
            
            try:
                for chunk in response_stream:
                    delta = chunk.choices[0].delta
                    
                    # excute reasoning_content property (DeepSeek orignial format)
                    if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                        content = delta.reasoning_content
                        if not is_reasoning:
                            self.ui.display_message("\n[Reasoning Chain]", style="bold yellow")
                            is_reasoning = True
                        reasoning_content += content
                        self.ui.display_message(content, end="", flush=True)
                    
                    # excute principal content and check <think> tag
                    if hasattr(delta, 'content') and delta.content:
                        content = delta.content
                        
                        # accumulated content in buffer for detect tag
                        buffered_content += content
                        
                        # chect <think> tag
                        if not in_think_tag and "<think>" in buffered_content:
                            # extract the content before tag to be normal responses
                            tag_pos = buffered_content.find("<think>")
                            pre_tag_content = buffered_content[:tag_pos]
                            
                            if pre_tag_content:
                                if is_reasoning:
                                    self.ui.display_separator()
                                    is_reasoning = False
                                    is_first_content = True
                                
                                if is_first_content and not full_response:
                                    self.ui.display_message("\nAmadeus: ", style="bold blue", end="")
                                    is_first_content = False
                                
                                full_response += pre_tag_content
                                self.ui.display_message(pre_tag_content, end="", flush=True)
                            
                            # collect reasoning context
                            in_think_tag = True
                            if not is_reasoning:
                                self.ui.display_message("\n[Reasoning Chain]", style="bold yellow")
                                is_reasoning = True
                            
                            # collect content after <think>  
                            think_content = buffered_content[tag_pos + 7:]  #  '<think>' 's length is 7
                            reasoning_content += think_content
                            self.ui.display_message(think_content, end="", flush=True)
                            buffered_content = think_content  # reset buffer，but retain content after <think> 
                        
                        # if content is in <think> tag，check </think> (end tag)
                        elif in_think_tag and "</think>" in buffered_content:
                            # 提取结束标签前的内容作为思考部分
                            tag_pos = buffered_content.find("</think>")
                            think_part = buffered_content[:tag_pos]
                            
                            if think_part:
                                reasoning_content += think_part
                                self.ui.display_message(think_part, end="", flush=True)
                    
                            in_think_tag = False
                            is_reasoning = True
                            
                            post_tag_content = buffered_content[tag_pos + 8:]  # '</think>' 's length is 8
                            
                            if post_tag_content:
                                if is_reasoning:
                                    self.ui.display_separator()
                                    is_reasoning = False
                                
                                if is_first_content and not full_response:
                                    self.ui.display_message("\nAmadeus: ", style="bold blue", end="")
                                    is_first_content = False
                                
                                full_response += post_tag_content
                                self.ui.display_message(post_tag_content, end="", flush=True)
                            
                            buffered_content = post_tag_content  # reset buffer too
                        
                        # add normal content
                        elif not in_think_tag:
                            # If not in a tag and the buffer does not contain suspicious tags, add to the normal response
                            if "<think>" not in buffered_content:
                                if is_reasoning:
                                    self.ui.display_separator()
                                    is_reasoning = False
                                    is_first_content = True
                                
                                if is_first_content and not full_response:
                                    self.ui.display_message("\nAmadeus: ", style="bold blue", end="")
                                    is_first_content = False
                                
                                full_response += content
                                self.ui.display_message(content, end="", flush=True)
                                buffered_content = ""
                        
                        # If inside the <think> tag, continue collecting thought content
                        elif in_think_tag and "</think>" not in buffered_content:
                            reasoning_content += content
                            self.ui.display_message(content, end="", flush=True)
                            buffered_content = "" 
                
                if buffered_content and not in_think_tag:
                    if is_reasoning:
                        self.ui.display_separator()
                        is_reasoning = False
                    
                    if is_first_content and not full_response:
                        self.ui.display_message("\nAmadeus: ", style="bold blue", end="")
                    
                    full_response += buffered_content
                    self.ui.display_message(buffered_content, end="", flush=True)
                
            except KeyboardInterrupt:
                self.ui.display_message("\n[Response interrupted by user]", style="yellow")
                if full_response:  # Save partial response if available
                    self.history.add_message("user", self.context["user_input"], attachments=current_attachments)
                    self.history.add_message("assistant", full_response, reasoning_content)
                return ChatState.WAITING_FOR_USER
            
            # Save complete response to history
            if full_response:
                self.history.add_message("user", self.context["user_input"], attachments=current_attachments)
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
        self.attachment_manager.clear_attachments()
        self.ui.display_message("Chat history and attachments cleared", style="yellow")
    
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
    
    def _handle_attach_command(self, args: str) -> None:
        """Handle attach command - add files"""
        if not args:
            self.ui.display_message("Usage: /attach <file_path> [file_path2 ...]", style="yellow")
            return
        
        # Parse multiple file paths
        file_paths = args.split()
        
        for file_path in file_paths:
            # Handle glob patterns
            import glob
            expanded_paths = glob.glob(os.path.expanduser(file_path))
            
            if not expanded_paths:
                self.ui.display_message(f"No files found matching: {file_path}", style="red")
                continue
            
            for path in expanded_paths:
                success, message = self.attachment_manager.add_attachment(path)
                if success:
                    self.ui.display_message(message, style="green")
                else:
                    self.ui.display_message(message, style="red")
    
    def _handle_detach_command(self, args: str) -> None:
        """Handle detach command - remove attachments"""
        if not args:
            # Clear all attachments
            self.attachment_manager.clear_attachments()
            self.ui.display_message("All attachments removed", style="yellow")
        else:
            # Remove specific attachment by index
            try:
                index = int(args)
                success, message = self.attachment_manager.remove_attachment(index)
                if success:
                    self.ui.display_message(message, style="green")
                else:
                    self.ui.display_message(message, style="red")
            except ValueError:
                self.ui.display_message("Invalid index. Use /files to see attachment indices", style="red")
    
    def _handle_files_command(self, args: str) -> None:
        """Handle files command - list attachments"""
        attachments = self.attachment_manager.list_attachments()
        if attachments:
            self.ui.display_attachments(attachments)
        else:
            self.ui.display_message("No attachments", style="yellow")
    
    def _handle_help_command(self, args: str) -> None:
        """Handle help command with attachment info"""
        help_text = """[bold cyan]DeepSeek Chat CLI Help[/bold cyan]

[bold yellow]Available Commands:[/bold yellow]
[green]/clear[/green]
    Clear all chat history and attachments
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

[green]/attach <file_path> [file_path2 ...][/green]
    Attach one or more files to your next message
    Usage: /attach <file_path> [file_path2 ...]
    Supports glob patterns (e.g., *.txt)
    Example: /attach image.jpg document.pdf
    Example: /attach ~/Downloads/*.png

[green]/detach [index][/green]
    Remove attachment(s)
    Usage: /detach [index]
    Without index: removes all attachments
    With index: removes specific attachment
    Example: /detach 0

[green]/files[/green]
    List all current attachments
    Usage: /files

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

[bold yellow]Attachment Support:[/bold yellow]
- Images: .jpg, .jpeg, .png, .gif, .webp, .bmp
- Text files: .txt, .md, .json, .csv, .xml, .yaml, .yml
- Documents: .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx
- Max file size: 20MB per file
- Multiple attachments supported

[bold yellow]Tips:[/bold yellow]
- Attachments are automatically cleared after sending a message
- Use /files to see current attachments before sending
- Chat history includes attachment information
"""
        self.ui.display_message(Panel.fit(help_text, border_style="blue"))

def main():
    """Main entry point"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="DeepSeek Chat CLI with Attachments")
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

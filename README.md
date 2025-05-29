# DeepSeek Chat CLI

A fully‑featured command‑line client for interacting with the [DeepSeek](https://deepseek.com) Chat API, offering a rich TUI experience, attachment support, and configurable state‑machine architecture.

## Table of contents
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Command‑line options](#command-line-options)
- [In‑session slash commands](#in-session-slash-commands)
- [Attachments](#attachments)
- [Keyboard shortcuts](#keyboard-shortcuts)
- [Configuration file](#configuration-file)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Interactive REPL** powered by *prompt‑toolkit* with undo/redo, multiline editing, and history search.  
- **Rich output** via *rich* panels, tables, and colourised syntax highlighting.  
- **Streaming responses** with separate “Reasoning Chain” and assistant output, including `<think>` tag handling.  
- **File attachments** – images, text, and Office/PDF docs up to 20 MB each, automatically embedded in the API call.  
- **Slash‑command palette** (`/clear`, `/save`, `/load`, `/attach`, `/detach`, `/files`, `/help`).  
- **Keyboard shortcuts** for power‑users (`Ctrl+D` to send, `Ctrl+Z/Y` undo/redo, etc.).  
- **Persistent config** saved to `~/.deepseek_config`; includes API key, proxy, model, temperature.  
- **State‑machine core** for clean transitions between *IDLE → WAITING_FOR_USER → PROCESSING → RESPONDING → ERROR*.  
- **Proxy & timeout support** with optional SOCKS transport.  
- **Debug mode** that prints the last request/response chunks.

## Architecture

```
┌──────────────────┐       ┌─────────────────────────┐
│  ChatUI          │──────▶│  ChatStateMachine       │
└──────────────────┘       └─────────────────────────┘
        ▲                            │
        │                            ▼
┌──────────────────┐       ┌─────────────────────────┐
│  AttachmentMgr   │◀──────│  ChatModel (API client) │
└──────────────────┘       └─────────────────────────┘
```

*DeepSeek Chat CLI* follows a **clean separation of concerns**:

| Layer | Responsibility |
|-------|----------------|
| `ChatUI` | Terminal I/O and presentation |
| `AttachmentManager` | Validation & encoding of user‑supplied files |
| `ChatModel` | Networking – talking to DeepSeek REST endpoints |
| `ChatStateMachine` | Orchestrates conversation flow & error handling |

## Installation

```bash
# 1. Clone
git clone https://github.com/starfield17/DEEPSEEK_API_CLI.git
cd DEEPSEEK_API_CLI

# 2. Create Python ≥3.8 environment (recommended)
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
bash install_requirement.sh
```

### Requirements

- Python **3.8+*
- [openai](https://pypi.org/project/openai/)
- rich, prompt‑toolkit, httpx, httpx‑socks, pygments, readline (Linux / macOS), and their transitive deps.

## Quick start

1. **Set your API key**  
   ```bash
   export DEEPSEEK_API_KEY="sk‑..."
   ```
   Or pass `--api-key` on the command line.

2. **Run**  
   ```bash
   python deep_seek_api_rebuild.py
   ```

3. **Chat** – type a prompt and press **Ctrl + D** to send.

### Example session

```
$ python deep_seek_api_rebuild.py
DeepSeek Chat CLI (Model: deepseek-chat)
>>> /attach diagram.png
Added: diagram.png (image/png, 42.0KB)
User: Explain this diagram please   Ctrl+D
Amadeus: …
```

## Command‑line options

| Flag | Description | Default |
|------|-------------|---------|
| `--api-key` | DeepSeek secret key | – |
| `--model` | Model name | `deepseek-chat` |
| `--proxy` | SOCKS/HTTP proxy, e.g. `socks5://127.0.0.1:7890` | – |
| `--base-url` | Override API endpoint | `https://api.deepseek.com/v1` |
| `--temperature` | Sampling temperature | `0.5` |
| `--debug` | Verbose request/response logging | `False` |
| `--system-prompt` | Inline system prompt | see below |
| `--system-prompt-file` | Path to prompt text file | – |
| `--save-config` | Persist the above to `~/.deepseek_config` | – |

## In‑session slash commands

| Command | Purpose |
|---------|---------|
| `/clear` | Wipe conversation and attachments |
| `/save [file]` | Save chat history to JSON |
| `/load [file]` | Load chat history |
| `/attach <path…>` | Attach one or more files (supports glob) |
| `/detach [index]` | Remove attachment(s) – without index clears all |
| `/files` | List current attachments |
| `/help` | Show built‑in help |

## Attachments

- **Images**: jpg, jpeg, png, gif, webp, bmp  
- **Text**: txt, md, json, csv, xml, yaml/yml  
- **Documents**: pdf, doc(x), xls(x), ppt(x)  
- Each file ≤ 20 MB  
- Multiple attachments allowed; cleared automatically after the request.

## Keyboard shortcuts

| Keys | Action |
|------|--------|
| `Enter` | New line |
| `Ctrl+D` | Send message |
| `Ctrl+V` | Paste clipboard |
| `Ctrl+Z / Ctrl+Y` | Undo / Redo |
| `↑ / ↓` | Browse history |

## Configuration file

Running `--save-config` (or entering your key at first launch) creates **`~/.deepseek_config`** with 0600 permissions:

```json
{
  "api_key": "sk-***",
  "model": "deepseek-chat",
  "proxy": null,
  "temperature": 0.7
}
```

Edit this file or rerun the script with new flags to update.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `API key missing` | Set `DEEPSEEK_API_KEY` or pass `--api-key` |
| `Request timed out` | Check network, proxy, or raise `--timeout` |
| `Connection failed` | Verify proxy string (`socks5://host:port`) |
| CLI freezes on Windows | Use **WSL** or ensure *readline* is installed |

Run with `--debug` for verbose logs.

## Contributing

PRs and issues are welcome! Please run `ruff` and `pytest` before submitting.

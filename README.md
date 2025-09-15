# Devin - Your Personal AI Assistant

Welcome to Devin, your very own Jarvis-inspired AI assistant! This project aims to create a
powerful, extensible AI system that can understand and respond to your questions while gradually
building up capabilities through tools and worker agents.

## Project Overview

Devin is designed to be a personal AI assistant that:
- Connects to local LLMs for natural language understanding and generation
- Responds to user questions in a conversational manner
- Scales from simple question answering to complex multi-agent workflows
- Provides a foundation for building sophisticated AI tools and systems
---

# 🧠 Local LLM Assistant with UV

A simple yet powerful local AI assistant that leverages a locally hosted LLM (via LM Studio) and integrates tools such as weather lookup and folder search. Built using Python, with package management handled via [UV](https://github.com/astral-sh/uv).

## 📌 Overview

This project allows you to interact with a local large language model (LLM) through a terminal-based interface. It supports tool integration for tasks like fetching current weather or locating folders on your machine.

### Features
- ✅ Communicates with LM Studio via API
- ✅ Tool support: `get_weather`, `find_folder`
- ✅ Easy-to-use CLI interface
- ✅ Uses UV for fast, modern package management

## 🛠️ Prerequisites

Before running this project, make sure you have:

- [LM Studio](https://lmstudio.ai/) installed and running with a model (e.g., `qwen/qwen3-coder-30b`)
- [UV](https://github.com/astral-sh/uv) installed for package management

## 📦 Installation

1. Clone or download this repository.
2. Install dependencies using UV:

```bash
uv sync
```

> This command will install all project dependencies listed in `pyproject.toml`.

3. Ensure LM Studio is running and the server is accessible at `http://127.0.0.1:1234/v1/chat/completions`.

## ▶️ Usage

Run the application using:

```bash
uv run main.py
```

Then, you can interact with the LLM by typing prompts directly into the terminal.

### Example Tools

You can use the following tools in your prompts:
- `get_weather`: Get current weather for a location.
  - Example prompt: *“What’s the weather like in London?”*
- `find_folder`: Find folders matching a name.
  - Example prompt: *“Find the devin folder”*

## 🧪 Development

To add new tools or modify existing ones:
1. Add your function to `tools.py`.
2. Register it in `ToolExecutor` class under `self.tools`.
3. Update the system prompt in `config.py` if needed.

## 📄 License

This project is licensed under the GNU General Public License v3.0 – see the [LICENSE](LICENSE) file for details.

---

## Roadmap

### Phase 1: Core Functionality
- [x] Basic LLM connection and response
- [x] Conversation history management
- [x] Enhanced response formatting

### Phase 2: Tool Integration
- [ ] Web search capabilities
- [x] File system operations
- [ ] Code execution environment

### Phase 3: Multi-Agent System
- [ ] Worker LLM coordination
- [ ] Task delegation and management
- [ ] Complex workflow automation

## License

TBC - non commercial / not for profit

---

*Devin - Your Personal AI Assistant*
*Powered by local LLM technology*

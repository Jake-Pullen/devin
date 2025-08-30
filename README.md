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

## Getting Started

### Prerequisites

Before running Devin, you'll need to set up your local LLM environment.
Refer to the [Configuration](#configuration) section below.

### Installation

1. Clone/Fork this repository
1. Use UV to set up requirements and environment:
```bash
uv sync
```

### Running Devin

To start Devin, simply run:
```bash
uv run main.py
```

This will initialize the AI assistant and begin listening for your questions.

## Configuration

Devin uses a configuration file to connect to your local LLM.
The configuration should be set up in `config.yaml`

```yaml
llm:
  model_path: "path/to/your/local/model"
  api_base: "http://localhost:1234/v1"
```

### Local LLM Setup

Devin currently supports connecting to local LLMs such as:
- [Ollama](https://ollama.com/)
- [LM Studio](https://lmstudio.ai/)
- [LocalAI](https://localai.io/)

Make sure your chosen LLM is running and accessible before starting Devin.

## Roadmap

### Phase 1: Core Functionality
- [ ] Basic LLM connection and response
- [ ] Conversation history management
- [ ] Enhanced response formatting

### Phase 2: Tool Integration
- [ ] Web search capabilities
- [ ] File system operations
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

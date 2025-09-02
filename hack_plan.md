
Below is a “ready‑to‑hack” checklist that covers everything you’ll need to set up before the hack day starts.  It’s broken into three phases – **pre‑planning**, **environment & tooling**, and **project‑specific prep** – so you can tackle each in order.

---

## 1️⃣ Pre‑Planning (What we’re building)

| Item | Why it matters | How to decide |
|------|----------------|---------------|
| **Problem statement + success metric** | Keeps the hack focused; avoids “we’ll just keep adding features” trap. | Write a one‑sentence goal and a concrete KPI (e.g., 80 % of user intents correctly handled). |
| **Scope & MVP** | Defines what you can finish in 24–48 h. | List core features, then prune until only 3–5 “must‑have” items remain. |
| **User stories / personas** | Helps surface edge cases early. | Draft 2–3 short scenarios (e.g., “As a student, I want the agent to schedule a meeting”). |
| **Success criteria & demo plan** | Gives you a clear finish line and a demo script. | Write bullet points for each feature that can be shown in the final demo. |
| **Team roles** | Prevents overlap and gaps (e.g., one person on NLP, another on UI). | Assign: Lead dev, AI/ML engineer, frontend/UI, documentation & testing. |

---

## 2️⃣ Environment & Tooling

### a) Code Repository
- **Git + GitHub/GitLab/Bitbucket** – set up the repo now; use a `main` branch and an `dev` branch.
- Add a **`.gitignore`** for Python (or use the template).
- Create a simple README with project name, goal, and how to run.

### b) Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### c) Dependency Management
- **`requirements.txt`** or **`pyproject.toml`** (Poetry / Pip‑env).
- Pin major packages (e.g., `langchain==0.1.*`, `openai==0.*`).

### d) Language Model & API Keys
| Service | What you need | Notes |
|---------|---------------|-------|
| OpenAI GPT‑4o or GPT‑4 Turbo | API key, set in env var (`OPENAI_API_KEY`) | Make sure quota is enough; consider a free tier for quick tests. |
| Anthropic Claude | `ANTHROPIC_API_KEY` | Good for “multimodal” prompts if you need images. |
| Hugging Face models (optional) | Token for private repos | For local inference if you want to avoid API calls. |

Store keys in a **`.env.example`** file and load them with `python-dotenv`.

### e) Agent Framework
- **LangChain/Agentic** or **OpenAI’s new `ChatCompletion` agents**.
  - Install: `pip install langchain openai python-dotenv`
- If you want modularity, consider the **MCP (Modular Conversational Protocol)** library if it exists; otherwise use a custom message‑passing protocol.

### f) Development Tools
| Tool | Purpose |
|------|---------|
| VS Code / PyCharm | IDE with Python support. |
| `black`, `ruff` | Auto‑formatting & linting. |
| `pytest` or `unittest` | Quick unit tests for critical functions. |
| Docker (optional) | Snapshot environment for later deployment. |

### g) Data / Knowledge Base
- **Static docs**: Markdown/HTML files you want the agent to read.
- **Vector store**: Use FAISS, Pinecone, or Chroma for embeddings if you’ll do RAG.
  - Pre‑compute embeddings before hack day (script in repo).
- **Sample user intents**: Create a JSON file with example queries.

---

## 3️⃣ Project‑Specific Prep

### 1. Architecture Sketch
```
┌─────────────────────┐   ┌───────────────┐
│  Frontend UI / CLI   │   │  API Layer    │
├─────────────────────┤   ├───────────────┤
│  Request handler     │◄─►│  Agent core   │
├─────────────────────┤   │  (MCP)        │
│  State manager      │   └───────────────┘
└─────────────────────┘
```
- Decide: CLI vs web app? Quick prototype → Flask or FastAPI + `uvicorn`.

### 2. Prompt Templates
- Draft **system**, **user**, and **assistant** messages.
- Keep them generic; add placeholders for dynamic content (e.g., `{user_name}`).

### 3. Agent Workflow
| Step | Action | Notes |
|------|--------|-------|
| 1 | Parse user input | Use regex or simple NLP to detect intent. |
| 2 | Retrieve context | Query vector store if needed. |
| 3 | Formulate LLM prompt | Inject retrieved docs + system instructions. |
| 4 | Call LLM | Get response, optionally chain multiple calls (e.g., “verify facts”). |
| 5 | Post‑process & output | Format as JSON or plain text for UI. |

### 4. Testing Strategy
- **Unit tests**: Prompt generation, vector lookup.
- **Integration test**: End‑to‑end request → response cycle.
- Run tests nightly in a CI (GitHub Actions) if time permits.

### 5. Security & Rate‑Limiting
- Add simple `sleep(1)` between API calls to avoid hitting rate limits during the hack.
- Sanitize user input before sending to LLM (avoid injection attacks).

---

## 4️⃣ Day‑of‑Hack Checklist

| Time | Task |
|------|------|
| **0–30 min** | Finalise repo, install deps, load env vars. |
| **30–60 min** | Build minimal UI (CLI or web). |
| **1–2 h** | Implement core agent loop & prompt templates. |
| **2–3 h** | Wire vector store / RAG if chosen. |
| **3–4 h** | Write unit tests for the most critical parts. |
| **4–5 h** | Run integration test, debug. |
| **5–6 h** | Prepare demo script; record or capture demo. |
| **6+ h** | Polish README, add usage instructions, commit final changes. |

---

## 5️⃣ Post‑Hack

1. **Documentation** – add a `docs/` folder with architecture and prompt design.
2. **License** – choose MIT / Apache-2.0 if you want to share.
3. **Deploy (optional)** – push to Render, Fly.io, or a Docker container on Heroku.
4. **Feedback loop** – ask friends for usability testing; iterate.

---

### Quick Starter Code Skeleton

```python
# main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

app = FastAPI()
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = "You are a helpful assistant."
prompt_template = PromptTemplate(
    input_variables=["user_input"],
    template="{system}\nUser: {user_input}\nAssistant:",
)

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    user_text = data.get("message", "")
    prompt = prompt_template.format(system=system_prompt, user_input=user_text)
    response = llm([prompt])
    return {"response": response[0].content}
```

Run with:

```bash
uvicorn main:app --reload
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"Hello"}'
```

---

## 🎉 Final Tips

- **Keep it simple** – you can always extend later.
- **Version control** – commit often; tag a “ready‑to‑demo” commit.
- **Timeboxing** – set 15‑min timers for each feature to avoid over‑engineering.
- **Have fun** – the best hacks happen when the team is laughing and learning.

Good luck with your hack day! 🚀

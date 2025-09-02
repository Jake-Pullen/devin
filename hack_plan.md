
Below is a “ready‑to‑hack” checklist that covers everything you’ll need to set up before the hack day starts.
It’s broken into three phases
* **pre‑planning**
* **environment & tooling**
* **project‑specific prep**

---

## 1️⃣ Pre‑Planning (What we’re building)

| Item | Why it matters | How to decide |
|------|----------------|---------------|
| **Problem statement + success metric** | Keeps the hack focused; avoids “we’ll just keep adding features” trap. | Write a one‑sentence goal and a concrete KPI (e.g., 80 % of user intents correctly handled). |
| **Scope & MVP** | Defines what you can finish in 24–48 h. | List core features, then prune until only 3–5 “must‑have” items remain. |
| **User stories / personas** | Helps surface edge cases early. | Draft 2–3 short scenarios (e.g., “As a student, I want the agent to schedule a meeting”). |
| **Success criteria & demo plan** | Gives you a clear finish line and a demo script. | Write bullet points for each feature that can be shown in the final demo. |
| **Team roles** | Prevents overlap and gaps (e.g., one person on NLP, another on UI). | Assign: Lead dev, AI/ML engineer, frontend/UI, documentation & testing. |

---

## 2️⃣ Environment & Tooling

### UV To handle virtual environment, package and dependancy handling.
> uv add {package name}

### Language Model
| Service | What you need | Notes |
|---------|---------------|-------|
| local running LLMs | lmstudio | Keeping things local (for LLMs) is one of the Goals. |


### Agent Framework
TBC, need to plan this
Think about agent LLMs and tool callers

### Development Tools
| Tool | Purpose |
|------|---------|
| VSCode / Zed | IDE with Python support. |
| ruff | Auto‑formatting & linting. |
| pytest | Quick unit tests for critical functions. |

### Data / Knowledge Base
- **Static docs**: Markdown/HTML files you want the agent to read.
- **Vector store**: Use FAISS, Pinecone, or Chroma for embeddings if you’ll do RAG.
- **Sample user intents**: Create a JSON file with example queries.

---

## 3️⃣ Project‑Specific Prep

### 1. Architecture Sketch
```
┌─────────────────────┐   ┌───────────────┐
│  Frontend UI / CLI  │   │  API Layer    │
├─────────────────────┤   ├───────────────┤
│  Request handler    │◄─►│  Agent core   │
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
- Sanitize user input before sending to LLM (avoid injection attacks).

---

## 4️⃣ Day‑of‑Hack Checklist

| Time | Task |
|------|------|
| **0–30 min** | Finalise repo, install deps, load env vars. |
| **30–60 min** | Build minimal UI (CLI or web). |
| **1–2 h** | Implement core agent loop & prompt templates. |
| **2–3 h** | Wire vector store / RAG if chosen. |
| **3–4 h** | Write unit tests for the most critical parts. |
| **4–5 h** | Run integration test, debug. |
| **5–6 h** | Prepare demo script; record or capture demo. |
| **6+ h** | Polish README, add usage instructions, commit final changes. |

---

## 5️⃣ Post‑Hack

1. **Documentation** – add a `docs/` folder with architecture and prompt design.
2. **License** – choose MIT / Apache-2.0 if you want to share.
3. **Deploy (optional)** – push to Render, Fly.io, or a Docker container on Heroku.
4. **Feedback loop** – ask friends for usability testing; iterate.

---

## 🎉 Final Tips

- **Keep it simple** – you can always extend later.
- **Version control** – commit often; tag a “ready‑to‑demo” commit.
- **Timeboxing** – set 15‑min timers for each feature to avoid over‑engineering.
- **Have fun** – the best hacks happen when the team is laughing and learning.

Good luck with your hack day! 🚀

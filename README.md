# Pet Let Agentic Logic Gateway 🚀

This is a **Senior-level Python Tool Server** designed for autonomous property management. Unlike simple chatbots, this system provides a **Structured Action Layer** for AI agents to interact with real business data.



## 🧠 Why this matters for Pet Let:
1. **Safety First:** Uses Pydantic for strict input validation. The AI cannot "hallucinate" an invalid date into your PMS.
2. **Complex Reasoning:** The `/verify-and-extend` tool doesn't just execute; it checks for conflicts first. This is "Agentic Closure."
3. **Infrastructure:** Fully Dockerized and tested on **Linux (Zorin OS)** to ensure 99.9% uptime in production.

## 🛠️ Tech Stack
- **Backend:** FastAPI (Async/Await)
- **Validation:** Pydantic v2
- **Environment:** Docker + Linux (CLI Focused)
- **Tooling:** Git Flow, REST API Architecture

## 🏃 How to Run
1. `pip install -r requirements.txt`
2. `uvicorn main:app --reload`

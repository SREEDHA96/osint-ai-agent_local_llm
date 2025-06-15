# 🛠️ Disclaimer

> **This project was developed as part of a technical interview assessment for [Elile.ai](https://elile.ai).**  

# 🕵️‍♂️ OSINT AI Agent

**LangGraph-based OSINT Intelligence Agent** for investigating public figures, organizations, or topics by retrieving and synthesizing information from multiple open sources using LLMs like Claude, GPT-4o, and Gemini.

---

## 📌 Features

- 🔎 **Query Analysis** — Breaks down natural language queries into structured OSINT tasks  
- 🧭 **Planning Agent** — Chooses relevant sources (news, social, academic, gov, etc.)  
- 📡 **Multi-source Retrieval** — From Google News, LinkedIn (stub), Twitter (stub), OpenCorporates, and more  
- 🔄 **Pivoting Agent** — Extracts related entities and builds a simple entity graph  
- 🧠 **LLM Synthesis** — Uses Gemini or GPT-4o to generate a professional intelligence report  
- 🧾 **Structured Output** — Final report with confidence scoring, retrieval logs, and source links  
- 🗃️ **Persistent Storage** — Saves each investigation with metadata and source traceability  
- 🧪 **Evaluation-ready** — Supports credibility scoring, follow-up queries, and entity mapping  

---

## 🚀 Quickstart

### 1. Clone the Repo

```bash
git clone https://github.com/SREEDHA96/osint-ai-agent_new.git
cd osint-ai-agent_new
```

### 2. Set Up Environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add a `.env` File

Create a `.env` file in the root with the following content:

```env
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GOOGLE_API_KEY=your-google-gemini-key
SERPAPI_KEY=your-serpapi-key
```

> ✅ You can use `.env.example` as a template.

### 4. Build the React Frontend
```bash
cd frontend
npm install
npm run build
```
### 5. Run the Backend Server
```bash
cd ..
uvicorn backend.main:app --reload
```
This launches the FastAPI backend at:
👉 http://127.0.0.1:8000

The backend will automatically serve the built frontend UI.


### 6. Run a Sample Investigation (CLI Mode)
To run the pipeline from the command line (no frontend):
```bash
python backend/graph.py
```
### 7. Optional: Run Frontend in Dev Mode
Use this during development if you want hot reloads:
```bash
cd frontend
npm run dev
```
Frontend: http://localhost:5173

Backend: http://127.0.0.1:8000

Make sure CORS is allowed for port 5173 (preconfigured).

Accessing the App
Once everything is set up and the backend is running:

🔹 Open in your browser:

http://127.0.0.1:8000


🔹 What You Can Do:

Enter an OSINT query
View the generated intelligence report
See evaluation scores
Download the report as a .txt file
View local history (stored in browser)

📌 Summary

| Component       | Command                             | URL                                            |
| --------------- | ----------------------------------- | ---------------------------------------------- |
| Backend (API)   | `uvicorn backend.main:app --reload` | [http://127.0.0.1:8000](http://127.0.0.1:8000) |
| Frontend (Dev)  | `npm run dev` (inside `/frontend`)  | [http://localhost:5173](http://localhost:5173) |
| Frontend (Prod) | `npm run build` → served by backend | [http://127.0.0.1:8000](http://127.0.0.1:8000) |
| CLI Run         | `python backend/graph.py`           | –                                              |


## 👨‍💻 Author

**Sreedha Bhakthavalsalan**  
GitHub: [@SREEDHA96](https://github.com/SREEDHA96)


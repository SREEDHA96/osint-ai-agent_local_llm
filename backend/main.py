from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import requests
import traceback
from backend.agents.evaluator import evaluate_report
from .llm_judge import call_claude_opus

from .graph import run_langgraph
from .database import insert_investigation, get_all_investigations 

app = FastAPI()

# ✅ History API
@app.get("/history")
def fetch_history():
    investigations = get_all_investigations()
    return [
        {
            "id": inv.id,
            "query": inv.query,
            "report": inv.final_report,
            "created_at": inv.created_at.isoformat()
        }
        for inv in investigations
    ]

# ✅ CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:5177",  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Query request model
class QueryRequest(BaseModel):
    query: str

# ✅ Main OSINT endpoint
@app.post("/query")
async def query_osint(req: QueryRequest):
    try:
        # Run LangGraph OSINT pipeline
        final_state = await run_langgraph(req.query)
        report = final_state.get("final_report", "No report generated.")

        # Call Claude Opus judge
        evaluation = await call_claude_opus(report)

        # Store in DB
        insert_investigation(
            query=req.query,
            final_report=report,
            evaluation=evaluation
        )

        return {"report": report, "evaluation": evaluation}

    except requests.RequestException as e:
        message = f"Network error: {e}".strip()
        print("❌", message)
        return {"error": {"message": message, "stage": "retrieval"}}
    except ValueError as e:
        message = f"Parsing error: {e}".strip()
        print("❌", message)
        return {"error": {"message": message, "stage": "parsing"}}
    except Exception as e:
        print("❌ Unexpected error:\n", traceback.format_exc())
        return {"error": {"message": str(e), "stage": "unknown"}}

# ✅ Serve frontend (React build)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

# ✅ Fallback to index.html for client-side routing
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = os.path.join(frontend_path, "index.html")
    return FileResponse(index_path)

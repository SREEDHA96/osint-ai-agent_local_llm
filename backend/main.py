from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .graph import build_langgraph
from .database import get_all_investigations

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
        final_state = await build_langgraph(req.query)
        return {"report": final_state.get("final_report", "No report generated.")}
    except Exception as e:
        return {"report": f"Error: {str(e)}"}

# ✅ Serve frontend (React build)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

# ✅ Fallback to index.html for client-side routing
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = os.path.join(frontend_path, "index.html")
    return FileResponse(index_path)
